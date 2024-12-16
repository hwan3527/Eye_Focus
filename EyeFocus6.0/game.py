import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


class GamePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("게임 선택")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")
        self.parent = parent

        # 아이콘 설정
        self.iconphoto(False, tk.PhotoImage(file="imagefile/icon.png"))

        # 제목 라벨
        self.title_label = tk.Label(self, text="게임 선택", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=(10, 10))

        # Combobox로 눈 선택
        self.eye_label = tk.Label(self, text="눈 선택", font=("Arial", 12), bg="#f0f0f0")
        self.eye_label.pack(pady=(10, 5))

        self.eye_var = tk.StringVar()
        self.eye_combobox = ttk.Combobox(
            self,
            textvariable=self.eye_var,
            state="readonly",
            values=[
                "좌/우 오른쪽 눈", 
                "좌/우 왼쪽 눈", 
                "상/하 오른쪽 눈", 
                "상/하 왼쪽 눈"
            ]
        )
        self.eye_combobox.pack(pady=(0, 5))
        self.eye_combobox.set("좌/우 오른쪽 눈")  # 기본값 설정

        # 아이트래킹 시작 버튼
        self.eyetracking_button = ttk.Button(self, text="아이트래킹 시작", command=self.start_eyetracking)
        self.eyetracking_button.pack(pady=(5, 20))

        # 게임 목록 표시
        self.game_list_label = tk.Label(self, text="게임 선택", font=("Arial", 12), bg="#f0f0f0")
        self.game_list_label.pack(pady=(10, 5))

        self.game_listbox = tk.Listbox(self, height=5)
        self.game_listbox.pack(pady=(10, 20))
        self.show_game_list()

        # 게임 시작 버튼
        self.start_button = ttk.Button(self, text="게임 시작", command=self.start_game)
        self.start_button.pack(pady=(10, 10))

        # 뒤로가기 버튼
        self.back_button = ttk.Button(self, text="뒤로가기", command=self.back_to_content)
        self.back_button.pack(pady=(10, 10))

    def show_game_list(self):
        """게임 목록을 표시합니다."""
        self.clear_game_list()
        self.game_listbox.insert(tk.END, "좌/우 교정 게임")
        self.game_listbox.insert(tk.END, "상/하 교정 게임")

    def clear_game_list(self):
        """게임 목록을 초기화합니다."""
        self.game_listbox.delete(0, tk.END)

    def start_eyetracking(self):
        """선택한 눈에 따라 다른 아이트래킹 스크립트를 실행합니다."""
        selected_eye = self.eye_var.get()

        try:
            if selected_eye == "좌/우 오른쪽 눈":
                subprocess.Popen(["python", "R_eyetracking.py"], shell=True)
                messagebox.showinfo("아이트래킹 시작", "좌/우 오른쪽 눈 아이트래킹을 시작합니다!")
            elif selected_eye == "좌/우 왼쪽 눈":
                subprocess.Popen(["python", "L_eyetracking.py"], shell=True)
                messagebox.showinfo("아이트래킹 시작", "좌/우 왼쪽 눈 아이트래킹을 시작합니다!")
            elif selected_eye == "상/하 오른쪽 눈":
                subprocess.Popen(["python", "R2_eyetracking.py"], shell=True)
                messagebox.showinfo("아이트래킹 시작", "상/하 오른쪽 눈 아이트래킹을 시작합니다!")
            elif selected_eye == "상/하 왼쪽 눈":
                subprocess.Popen(["python", "L2_eyetracking.py"], shell=True)
                messagebox.showinfo("아이트래킹 시작", "상/하 왼쪽 눈 아이트래킹을 시작합니다!")
        except Exception as e:
            messagebox.showerror("오류", f"아이트래킹 실행 중 오류가 발생했습니다: {e}")

    def start_game(self):
        """선택한 게임을 시작합니다."""
        selected_game = self.game_listbox.get(tk.ACTIVE)

        if selected_game:
            if selected_game == "좌/우 교정 게임":
                try:
                    exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shooting_game", "shooting_game.exe")
                    subprocess.Popen([exe_path], shell=True)
                    messagebox.showinfo("게임 시작", "좌/우 교정 게임을 시작합니다!")
                except Exception as e:
                    messagebox.showerror("오류", f"Unity 게임 실행 중 오류가 발생했습니다: {e}")
            elif selected_game == "상/하 교정 게임":
                try:
                    exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DinoRun_game", "Dino__.exe")
                    subprocess.Popen([exe_path], shell=True)
                    messagebox.showinfo("게임 시작", "상/하 교정 게임을 시작합니다!")
                except Exception as e:
                    messagebox.showerror("오류", f"DinoRun 게임 실행 중 오류가 발생했습니다: {e}")
        else:
            messagebox.showwarning("선택 오류", "게임을 선택해주세요.")

    def back_to_content(self):
        """컨텐츠 페이지로 돌아갑니다."""
        self.destroy()
        self.parent.deiconify()  # 컨텐츠 페이지 다시 보이기


# 메인 테스트 실행
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    game_page = GamePage(root)
    game_page.mainloop()