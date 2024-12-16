import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from register_page import RegisterWindow
from content_page import ContentPage
import session_manager  # 세션 관리 모듈 추가
from PIL import Image, ImageTk

# MySQL 연결 설정
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="eye_focus"
    )

# 로그인 기능
def login_user(user_id, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
        cursor.execute(query, (user_id, password))
        result = cursor.fetchone()
        if result:
            session_manager.login(user_id)  # 로그인 성공 시 세션에 사용자 저장
        return result is not None
    finally:
        cursor.close()
        conn.close()

# 메인 로그인 및 회원가입 창
class LoginRegisterApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("EyeFocus Login & Register")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        # 아이콘 설정
        self.iconphoto(False, ImageTk.PhotoImage(Image.open("imagefile/icon.png")))
        
        # 창 닫기 이벤트 처리
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12), padding=5)

        ttk.Label(self, text="User ID:").pack(pady=(20, 5))
        self.user_id_input = ttk.Entry(self)
        self.user_id_input.pack(pady=(0, 10))

        ttk.Label(self, text="Password:").pack(pady=(10, 5))
        self.password_input = ttk.Entry(self, show='*')
        self.password_input.pack(pady=(0, 20))

        ttk.Button(self, text="Login", command=self.login).pack(pady=(0, 10))
        ttk.Button(self, text="Register", command=self.show_register).pack()

    def login(self):
        user_id = self.user_id_input.get()
        password = self.password_input.get()

        if login_user(user_id, password):
            messagebox.showinfo("Success", f"환영합니다, {session_manager.get_current_user()}님!")
            self.open_content_page()  # 컨텐츠 페이지 열기
        else:
            messagebox.showwarning("Error", "Login failed. Check your credentials.")

    def open_content_page(self):
        self.withdraw()  # 로그인 창 숨기기
        content_page = ContentPage(self.master)  # ContentPage 생성 시 MainApp 전달
        content_page.grab_set()  # ContentPage가 활성화되도록 설정

    def show_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.grab_set()

    def on_close(self):
        self.destroy()  # 현재 창 닫기
        self.master.deiconify()  # 메인 애플리케이션 창 보이기
