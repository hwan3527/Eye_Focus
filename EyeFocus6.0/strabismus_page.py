import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import cv2
import mysql.connector
from PIL import Image, ImageTk
import session_manager
import time

# 데이터베이스 연결 설정
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="eye_focus"
    )

# 캡처한 이미지를 데이터베이스에 저장
def save_image_to_db(user_id, image_path):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        with open(image_path, 'rb') as file:
            binary_data = file.read()
        
        query = "INSERT INTO strabismus_images (user_id, image, image_path) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, binary_data, image_path))
        conn.commit()
        messagebox.showinfo("Success", "이미지가 데이터베이스와 폴더에 저장되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showwarning("Error", "이미지 저장에 실패했습니다.")
    finally:
        cursor.close()
        conn.close()

# 소아사시 구별 페이지 클래스
class StrabismusPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("소아사시 구별")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")
        
        self.user_id = session_manager.get_current_user()

        ttk.Label(self, text="소아사시 구별 이미지 캡처", font=("Arial", 14)).pack(pady=20)
        
        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=10)

        ttk.Button(self, text="캡처 시작", command=self.capture_image).pack(pady=10)
        ttk.Button(self, text="뒤로가기", command=self.back_to_content_page).pack(pady=10)

    # 이미지 캡처 함수
    def capture_image(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            messagebox.showwarning("Error", "카메라를 열 수 없습니다.")
            return
        
        countdown_start = time.time()  # 카운트다운 시작 시간
        countdown = 5
        while countdown > 0:
            ret, frame = cap.read()
            if not ret:
                messagebox.showwarning("Error", "카메라에서 프레임을 가져올 수 없습니다.")
                cap.release()
                cv2.destroyAllWindows()
                return
            
            # 카운트다운 텍스트 표시
            cv2.putText(frame, str(countdown), (frame.shape[1] - 100, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
            cv2.imshow("Camera Feed", frame)
            
            # 매 프레임마다 카운트다운 갱신
            if time.time() - countdown_start >= 1:
                countdown -= 1
                countdown_start = time.time()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 중지 가능
                break
        
        # 마지막 캡처 이미지 저장
        ret, frame = cap.read()
        if ret:
            # 유저 폴더 경로 설정
            user_folder = os.path.join("user", self.user_id)
            images_folder = os.path.join(user_folder, "images")
            os.makedirs(images_folder, exist_ok=True)

            # 이미지 파일 경로 설정 (타임스탬프를 추가하여 고유한 파일 이름 사용)
            timestamp = int(time.time())  # 타임스탬프 생성
            image_path = os.path.join(images_folder, f"captured_image_{timestamp}.jpg")
            cv2.imwrite(image_path, frame)

            # 데이터베이스에 이미지와 경로 저장
            save_image_to_db(self.user_id, image_path)

            # 캡처된 이미지 미리보기
            img = Image.open(image_path)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            messagebox.showinfo("캡처 완료", "캡처된 이미지가 저장되었습니다.")
        else:
            messagebox.showwarning("Error", "이미지를 캡처할 수 없습니다.")
        
        cap.release()
        cv2.destroyAllWindows()

    def back_to_content_page(self):
        self.destroy()  # 현재 페이지 닫기
