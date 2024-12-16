import cv2
import socket
import threading
import time
import keyboard

# UDP 서버 설정
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 종료 플래그
is_running = True

# 얼굴 및 눈 검출기 초기화
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# 아이트래킹 함수
def track_eye():
    global is_running
    cap = cv2.VideoCapture(0)  # 웹캠 사용

    while is_running:
        ret, frame = cap.read()
        if not ret:
            print("카메라를 읽을 수 없습니다.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        # 얼굴 검출 및 표시
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 얼굴 영역 표시
            roi_gray = gray[y:y + h, x:x + w]  # 얼굴 영역 추출
            roi_color = frame[y:y + h, x:y + w]  # 컬러 영역 추출
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # 눈 검출
            if len(eyes) > 0:
                # 오른쪽 눈만 선택하도록 범위 제한
                right_eye = None
                for (ex, ey, ew, eh) in eyes:
                    # 오른쪽 눈을 선택하는 조건: x 좌표가 얼굴의 오른쪽 절반에 위치하는 눈
                    if ex > w / 2:  # 얼굴의 오른쪽 절반에 위치한 눈만 선택
                        right_eye = (ex, ey, ew, eh)
                        break
                
                if right_eye:
                    ex, ey, ew, eh = right_eye

                    # 눈 박스를 더 좁게 하기 위해 크기를 조정
                    padding = 10  # 박스의 크기를 줄이는 패딩 값 (조정 가능)
                    ex += padding
                    ew -= padding * 2
                    ey += padding
                    eh -= padding * 2

                    eye_gray = roi_gray[ey:ey + eh, ex:ex + ew]
                    eye_color = roi_color[ey:ey + eh, ex:ex + ew]

                    # 동공 검출
                    _, threshold = cv2.threshold(eye_gray, 50, 255, cv2.THRESH_BINARY_INV)
                    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        max_contour = max(contours, key=cv2.contourArea)
                        (cx, cy), radius = cv2.minEnclosingCircle(max_contour)
                        cx, cy = int(cx), int(cy)

                        # 좌우 반전 처리 (사용자 관점에 맞춤)
                        flipped_cx = ew - cx

                        # 동공 위치에 따라 값 결정
                        if flipped_cx < ew * 0.33:
                            value = 1  # 왼쪽
                        elif flipped_cx > ew * 0.66:
                            value = 2  # 오른쪽
                        else:
                            value = 0  # 중앙

                        # 유니티로 값 전송
                        sock.sendto(str(value).encode(), (UDP_IP, UDP_PORT))
                        print(f"Sent: {value}")

                        # 시각화 - 동공 중심과 박스 그리기
                        cv2.circle(frame, (x + ex + cx, y + ey + cy), 5, (0, 255, 0), -1)  # 동공 표시
                        cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)  # 좁혀진 눈 박스

        # 전체 화면 표시
        cv2.imshow("Full Face with Eye Tracking", frame)

        # 'q' 키로 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            break

    cap.release()
    cv2.destroyAllWindows()


# 아이트래킹 스레드 실행
track_eye_thread = threading.Thread(target=track_eye)
track_eye_thread.start()

# 종료 키 확인
while True:
    if keyboard.is_pressed('ctrl+q'):  # Ctrl + Q가 눌리면 종료
        is_running = False
        break

track_eye_thread.join()

sock.close()
print("UDP server stopped.")
