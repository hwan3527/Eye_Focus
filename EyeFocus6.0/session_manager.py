current_user = None  # 현재 로그인한 사용자 ID를 저장

def login(user_id):
    global current_user
    current_user = user_id

def logout():
    global current_user
    current_user = None

def get_current_user():
    return current_user

def is_logged_in():
    return current_user is not None
