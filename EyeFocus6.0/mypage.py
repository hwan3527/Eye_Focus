import tkinter as tk
from tkinter import ttk
import random
import session_manager

class MyPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("마이페이지")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")

        self.user_id = session_manager.get_current_user()

        # 사용자 정보 제목
        ttk.Label(self, text=f"{self.user_id}님의 마이페이지", font=("Arial", 16)).pack(pady=10)

        # 사용자 상세 정보 섹션 추가
        self.create_user_info_section()

        # 성별 선택 버튼 추가
        self.create_gender_selection()

        # 사시 종류 드롭다운 추가
        self.create_eye_type_dropdown()

        # 오늘의 목표 설정 추가
        self.create_goal_section()

        # 맞춤 팁 또는 메시지 표시
        self.display_all_tips()

    def create_user_info_section(self):
        """사용자 정보 표시 섹션"""
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=10, fill="x")

        # 이름 (아이디와 동일하게 설정)
        ttk.Label(info_frame, text="이름:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(info_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, self.user_id)  # 아이디로 기본값 설정
        self.name_entry.config(state="readonly")  # 읽기 전용으로 설정

        # 나이 선택 (드롭다운 메뉴)
        ttk.Label(info_frame, text="나이:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.age_var = tk.StringVar()
        age_dropdown = ttk.Combobox(info_frame, textvariable=self.age_var, state="readonly", width=17)
        age_dropdown["values"] = [str(i) for i in range(10, 101)]  # 10세부터 100세까지 선택 가능
        age_dropdown.grid(row=1, column=1, padx=5, pady=2)
        age_dropdown.current(0)  # 기본값 설정

        # 연락처 (기본값 자동 입력 및 번호만 입력 가능)
        ttk.Label(info_frame, text="연락처:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.phone_entry = ttk.Entry(info_frame, width=20)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=2)
        self.phone_entry.insert(0, "010-____-____")  # 기본값 설정
        self.phone_entry.bind("<KeyRelease>", self.enforce_phone_format)  # 이벤트 바인딩

    def enforce_phone_format(self, event):
        """연락처 입력 시 형식을 유지하고 숫자만 입력 가능"""
        phone = self.phone_entry.get()
        digits = ''.join(filter(str.isdigit, phone))  # 숫자만 남기기

        # 기본 형식: 010-0000-0000
        formatted = "010-____-____"
        if len(digits) >= 11:
            formatted = f"{digits[:3]}-{digits[3:7]}-{digits[7:11]}"
        elif len(digits) >= 7:
            formatted = f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        elif len(digits) >= 3:
            formatted = f"{digits[:3]}-{digits[3:]}"
        elif len(digits) > 0:
            formatted = f"{digits}"

        # 입력 필드 업데이트
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, formatted)

    def create_gender_selection(self):
        """성별 선택 섹션"""
        ttk.Label(self, text="성별:").pack(pady=5, anchor="w", padx=20)

        gender_frame = ttk.Frame(self)
        gender_frame.pack(anchor="w", padx=20)
       
        self.gender_var = tk.StringVar(value="남성")
        ttk.Radiobutton(gender_frame, text="남성", variable=self.gender_var, value="남성").pack(side="left", padx=5)
        ttk.Radiobutton(gender_frame, text="여성", variable=self.gender_var, value="여성").pack(side="left", padx=5)

    def create_eye_type_dropdown(self):
        """사시 종류 선택 섹션"""
        ttk.Label(self, text="사시 종류:").pack(pady=5, anchor="w", padx=20)

        self.eye_type_var = tk.StringVar()
        eye_type_dropdown = ttk.Combobox(self, textvariable=self.eye_type_var, state="readonly")
        eye_type_dropdown["values"] = ["안외사시", "안내사시", "수평사시", "혼합사시"]
        eye_type_dropdown.pack(padx=20, pady=5, fill="x")
        eye_type_dropdown.current(0)

    def create_goal_section(self):
        """오늘의 목표 설정 섹션"""
        goal_frame = ttk.Frame(self)
        goal_frame.pack(pady=5, anchor="w", padx=20)

        ttk.Label(goal_frame, text="오늘의 목표:").grid(row=0, column=0, sticky="w")
        self.goal_entry = ttk.Entry(goal_frame, width=30)
        self.goal_entry.grid(row=0, column=1, padx=5)

        self.goal_check_var = tk.BooleanVar()
        self.goal_checkbox = ttk.Checkbutton(goal_frame, variable=self.goal_check_var)
        self.goal_checkbox.grid(row=0, column=2, padx=5)

    def display_all_tips(self):
        """모든 맞춤 팁 또는 메시지 표시"""
        tips = [
            "규칙적인 훈련이 시력 개선에 도움이 됩니다!",
            "쉬는 시간도 중요해요. 20분 훈련 후 5분 휴식!",
            "양쪽 눈을 골고루 훈련하는 것을 잊지 마세요!"
        ]
       
        for tip in tips:
            tk.Label(self, text=tip, font=("Arial", 12), wraplength=400).pack(pady=5)