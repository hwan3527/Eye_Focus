import os  # 폴더 생성에 필요한 모듈 추가
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# MySQL 연결 설정
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="eye_focus"
    )

# 폴더 생성 함수
def create_user_folder(user_name):
    user_folder_path = os.path.join("user", user_name)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

# 회원가입 기능
def register_user(name, age, user_id, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO users (name, age, user_id, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, age, user_id, password))
        conn.commit()

        # 회원가입 성공 시 사용자 이름으로 폴더 생성
        create_user_folder(user_id)  # user_id 또는 name으로 폴더 생성 가능

        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# 회원가입 창
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12), padding=5)

        tk.Label(self, text="Name:").pack(pady=(20, 5))
        self.name_input = ttk.Entry(self)
        self.name_input.pack(pady=(0, 10))

        tk.Label(self, text="Age:").pack(pady=(10, 5))
        self.age_input = ttk.Entry(self)
        self.age_input.pack(pady=(0, 10))

        tk.Label(self, text="User ID:").pack(pady=(10, 5))
        self.user_id_input = ttk.Entry(self)
        self.user_id_input.pack(pady=(0, 10))

        tk.Label(self, text="Password:").pack(pady=(10, 5))
        self.password_input = ttk.Entry(self, show='*')
        self.password_input.pack(pady=(0, 20))

        ttk.Button(self, text="Register", command=self.register).pack(pady=(0, 10))
        ttk.Button(self, text="Back", command=self.destroy).pack()

    # 회원가입 로직
    def register(self):
        name = self.name_input.get()
        age = self.age_input.get()
        user_id = self.user_id_input.get()
        password = self.password_input.get()

        if register_user(name, age, user_id, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.destroy()
        else:
            messagebox.showwarning("Error", "Registration failed. User ID might already exist.")
