import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import session_manager  # 세션 관리 모듈 추가
from strabismus_page import StrabismusPage  # strabismus_page 모듈 임포트
from game import GamePage  # game.py 모듈 임포트 추가
from mypage import MyPage  # mypage 모듈 임포트 추가
from result import ResultPage  # result.py 모듈 임포트 추가

class ContentPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("컨텐츠 페이지")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")
        self.parent = parent

        # 아이콘 설정
        self.iconphoto(False, ImageTk.PhotoImage(Image.open("imagefile/icon.png")))

        # 로그인 상태 확인
        if not session_manager.is_logged_in():
            messagebox.showwarning("Error", "로그인이 필요합니다.")
            self.destroy()
            return

        # 창 닫기 이벤트 처리
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        user_id = session_manager.get_current_user()
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))

        tk.Label(self, text=f"환영합니다, {user_id}님!", font=("Arial", 14)).pack(pady=(10, 20))

        # 기능 버튼들 추가
        ttk.Button(self, text="소아사시 종류 구별", command=self.strabismus_identification).pack(pady=(10, 10))
        ttk.Button(self, text="마이페이지", command=self.open_my_page).pack(pady=(10, 10))
        ttk.Button(self, text="게임", command=self.open_game_page).pack(pady=(10, 10))
        ttk.Button(self, text="결과", command=self.results).pack(pady=(10, 10))
        ttk.Button(self, text="로그아웃", command=self.logout).pack(pady=(10, 20))

    def on_close(self):
        self.destroy()  # 현재 창 닫기
        self.parent.deiconify()  # 메인 애플리케이션 창 보이기

    def strabismus_identification(self):
        StrabismusPage(self)  # 새 strabismus 페이지 열기

    def open_game_page(self):
        GamePage(self)  # game.py의 GamePage 열기

    def open_my_page(self):
        MyPage(self)  # MyPage 클래스를 열어 프로필 정보와 이미지를 보여주기

    def results(self):
        """결과 버튼 클릭 시 ResultPage 열기"""
        self.withdraw()  # 현재 창 숨기기
        result_page = ResultPage(self)
        self.center_window(result_page)  # 창 중앙 배치

    def center_window(self, window):
        """지정된 창을 화면의 중앙에 배치"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def logout(self):
        session_manager.logout()  # 세션 로그아웃
        messagebox.showinfo("로그아웃", "로그아웃되었습니다.")
        self.destroy()  # 현재 페이지 닫기
        self.parent.deiconify()  # MainApp 다시 보이기 (로그인 페이지로 돌아가기)
