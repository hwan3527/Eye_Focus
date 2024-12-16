import tkinter as tk
from PIL import Image, ImageTk
from login_page import LoginRegisterApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 아이콘 설정
        self.iconphoto(False, ImageTk.PhotoImage(Image.open("imagefile/icon.png")))

        # 배경 이미지 설정
        self.background_image = Image.open("imagefile/EyeFocus.jpg")
        self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # 배경 레이블 추가
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # 시작 버튼 추가
        self.start_button = tk.Button(self, text="Start", command=self.open_login_page, font=("Arial", 16), bg="#4CAF50", fg="white", borderwidth=0, relief="flat")
        self.start_button.place(relx=0.5, rely=0.85, anchor="center")  # 중앙 하단에 버튼 배치, 약간 위로 이동

    def open_login_page(self):
        self.withdraw()  # 메인 창 숨기기
        app = LoginRegisterApp(self)  # 로그인 페이지 열기
        app.mainloop()  # 로그인 페이지의 이벤트 루프 실행

if __name__ == "__main__":
    app = MainApp()
    app.geometry("800x600")
    app.title("EyeFocus")

    # 창을 화면 중앙에서 약간 위로 배치
    app.update_idletasks()  # 창 크기 정보를 갱신
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 800
    window_height = 600

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2 - 30  # 화면 중앙에서 30픽셀 위로 이동

    app.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app.mainloop()
