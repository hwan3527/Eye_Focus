import cv2
import socket
import threading
import keyboard

# UDP 설정
UDP_IP = "127.0.0.1"
UDP_PORT = 5005  # 왼쪽 눈 전송용 포트
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 종료 플래그
is_running = True

# 얼굴 및 눈 검출기 초기화
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# 고정된 눈 박스 크기 설정
EYE_BOX_WIDTH = 40
EYE_BOX_HEIGHT = 20

# 왼쪽 눈 추적 함수
def track_left_eye():
    global is_running
    cap = cv2.VideoCapture(0)  # 웹캠 사용

    while is_running:
        ret, frame = cap.read()
        if not ret:
            print("카메라를 읽을 수 없습니다.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        # 얼굴 검출
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)

            # 왼쪽 눈 감지
            if len(eyes) >= 2:
                ex, ey, ew, eh = sorted(eyes, key=lambda e: e[0])[0]  # 왼쪽 눈
                ex = max(0, ex + (ew - EYE_BOX_WIDTH) // 2)  # 눈 영역 중앙 정렬
                ey = max(0, ey + (eh - EYE_BOX_HEIGHT) // 2)
                ew, eh = EYE_BOX_WIDTH, EYE_BOX_HEIGHT  # 고정된 크기 설정

                # 눈 영역에서 동공 감지
                eye_gray = roi_gray[ey:ey + eh, ex:ex + ew]
                _, threshold = cv2.threshold(eye_gray, 50, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    max_contour = max(contours, key=cv2.contourArea)
                    (cx, cy), _ = cv2.minEnclosingCircle(max_contour)
                    cx, cy = int(cx), int(cy)

                    # 동공 위치에 따라 위/아래 판별
                    if cy < eh * 0.33:
                        value = 3  # 위쪽
                    elif cy > eh * 0.66:
                        value = 4  # 아래쪽
                    else:
                        value = 0  # 중앙

                    # UDP 데이터 전송
                    sock.sendto(str(value).encode(), (UDP_IP, UDP_PORT))
                    print(f"Sent: {value}")

                    # 시각화
                    cv2.circle(roi_color, (ex + cx, ey + cy), 3, (0, 255, 0), -1)
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # 화면 출력
        cv2.imshow("Left Eye Tracking (Up/Down)", frame)

        # 'q' 키로 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# 아이트래킹 스레드 실행
track_eye_thread = threading.Thread(target=track_left_eye)
track_eye_thread.start()

# 종료 키 확인
while True:
    if keyboard.is_pressed('ctrl+q'):  # Ctrl + Q로 종료
        is_running = False
        break

track_eye_thread.join()
sock.close()
print("UDP server stopped.")
