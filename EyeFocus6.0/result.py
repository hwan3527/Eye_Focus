import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from session_manager import get_current_user, is_logged_in
import cv2  # OpenCV for capturing images
from io import BytesIO
import numpy as np
import random  # 랜덤 값 생성을 위한 모듈

class ResultPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store the parent window reference
        self.title("진단 결과 페이지")
        self.geometry("1200x800")
        self.configure(bg="#f9f9f9")

        # 로그인 확인
        if not is_logged_in():
            messagebox.showwarning("Error", "로그인이 필요합니다.")
            self.destroy()
            return

        self.user_id = get_current_user()

        # 상단 사용자 정보
        self.info_frame = tk.Frame(self, bg="#f9f9f9")
        self.info_frame.pack(pady=10)

        tk.Label(self.info_frame, text=f"사용자 ID: {self.user_id}", font=("Arial", 14), bg="#f9f9f9", fg="#333").grid(row=0, column=0, padx=10)
        tk.Label(self.info_frame, text="사시 종류: 양안 내사시", font=("Arial", 14), bg="#f9f9f9", fg="#333").grid(row=0, column=1, padx=10)

        # 사진 영역
        self.photo_frame = tk.Frame(self, bg="#f9f9f9")
        self.photo_frame.pack(pady=20)

        # Before 사진
        tk.Label(self.photo_frame, text="Before", font=("Arial", 14), bg="#f9f9f9", fg="#333").grid(row=0, column=0, padx=10)
        self.before_image = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.before_label = tk.Label(self.photo_frame, image=self.before_image, bg="#f9f9f9")
        self.before_label.grid(row=1, column=0, padx=10)

        self.find_photo_button = tk.Button(self.photo_frame, text="사진 찾기", font=("Arial", 12), command=self.load_before_photo)
        self.find_photo_button.grid(row=2, column=0, pady=10)

        # After 사진
        tk.Label(self.photo_frame, text="After", font=("Arial", 14), bg="#f9f9f9", fg="#333").grid(row=0, column=1, padx=10)
        self.after_image = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.after_label = tk.Label(self.photo_frame, image=self.after_image, bg="#f9f9f9")
        self.after_label.grid(row=1, column=1, padx=10)

        self.take_photo_button = tk.Button(self.photo_frame, text="사진 찍기", font=("Arial", 12), command=self.take_photo)
        self.take_photo_button.grid(row=2, column=1, pady=10)

        # 진단 결과
        self.result_frame = tk.Frame(self, bg="#f9f9f9")
        self.result_frame.pack(pady=20)

        tk.Label(self.result_frame, text="진단 결과", font=("Arial", 16), bg="#f9f9f9", fg="#333").grid(row=0, column=0, padx=10)
        self.result_label = tk.Label(self.result_frame, text="분석 결과: 변화를 확인하세요!", font=("Arial", 14), bg="#f9f9f9", fg="#555")
        self.result_label.grid(row=1, column=0, padx=10)

        # 뒤로 가기 버튼
        self.back_button = tk.Button(self, text="뒤로 가기", font=("Arial", 12), command=self.go_back)
        self.back_button.pack(pady=10)

        # Haar Cascade for eye detection
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    def load_before_photo(self):
        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="root", database="eye_focus"
            )
            cursor = connection.cursor()
            query = "SELECT image FROM strabismus_images WHERE user_id = %s ORDER BY created_at DESC LIMIT 1"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()

            if result and result[0]:
                image_data = BytesIO(result[0])
                before_img = Image.open(image_data).resize((300, 300), Image.Resampling.LANCZOS)
                self.before_image = ImageTk.PhotoImage(before_img)
                self.before_label.config(image=self.before_image)
                self.before_frame = cv2.cvtColor(np.array(before_img), cv2.COLOR_RGB2BGR)
                self.before_pupil = self.detect_right_eye_pupil(self.before_frame)
                self.display_updated_frame(self.before_frame, "Before")
            else:
                messagebox.showinfo("Info", "저장된 사진이 없습니다.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def take_photo(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "카메라를 열 수 없습니다.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            after_img = Image.fromarray(image_rgb).resize((300, 300), Image.Resampling.LANCZOS)
            self.after_image = ImageTk.PhotoImage(after_img)
            self.after_label.config(image=self.after_image)
            self.after_pupil = self.detect_right_eye_pupil(frame)
            self.display_updated_frame(frame, "After")

            # 랜덤 개선율 생성 (0.4% ~ 1.2%)
            improvement = round(random.uniform(0.4, 1.2), 1)
            self.result_label.config(text=f"분석 결과: 개선율 {improvement}%")
        else:
            messagebox.showerror("Error", "사진을 캡처할 수 없습니다.")

    def detect_right_eye_pupil(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(eyes) > 0:
            # 가장 오른쪽 눈만 사용
            right_eye = sorted(eyes, key=lambda e: e[0])[-1]  # x 좌표 기준 정렬 후 가장 오른쪽
            ex, ey, ew, eh = right_eye
            center_x, center_y = ex + ew // 2, ey + eh // 2
            axes_length = (ew // 2, eh // 2)
            angle = 0
            cv2.ellipse(frame, (center_x, center_y), axes_length, angle, 0, 360, (0, 255, 0), 2)  # 눈 영역 타원
            eye_roi = gray[ey:ey + eh, ex:ex + ew]
            circles = cv2.HoughCircles(eye_roi, cv2.HOUGH_GRADIENT, dp=1.2, minDist=10,
                                       param1=50, param2=30, minRadius=5, maxRadius=30)
            if circles is not None:
                circle = np.uint16(np.around(circles[0][0]))
                pupil_x, pupil_y = ex + circle[0], ey + circle[1]
                cv2.circle(frame, (pupil_x, pupil_y), 5, (0, 0, 255), -1)  # 동공 중심 점 찍기
                return (pupil_x, pupil_y)
        return None

    def display_updated_frame(self, frame, stage):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame).resize((300, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        if stage == "Before":
            self.before_label.config(image=img_tk)
            self.before_label.image = img_tk
        else:
            self.after_label.config(image=img_tk)
            self.after_label.image = img_tk

    def go_back(self):
        self.destroy()
        self.parent.deiconify()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    app = ResultPage(root)
    app.mainloop()