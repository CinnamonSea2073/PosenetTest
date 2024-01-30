# ラズベリーパイのコード

import cv2
import requests
import base64
import io
import time
import pyautogui

API_BACKEND = "https://strong-kentucky-con-notebooks.trycloudflare.com/analyze_image"

# カメラの初期化
# おまじない的なやつ
cap = cv2.VideoCapture(0)
before_hand_xy = ["0.0", "0.0"]
start_time = time.time()

while True:
    ret, frame = cap.read()
    _, img_encoded = cv2.imencode('.jpg', frame)
    data = {'file': img_encoded.tobytes()}
    response = requests.post(API_BACKEND, files=data)
    result = response.json()

    height, width, _ = frame.shape
    for index, i in enumerate(eval(result)["result"]):
        y, x = int(256*(height/256)*float(i["keypoint"][0])), int(256*(width/256)*float(i["keypoint"][1]))
        if index == 10:
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
        else:
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
    cv2.imshow('preview', frame)

    if float(eval(result)["result"][10]["score"]) > 0.6:
        now_hand_xy = eval(result)["result"][10]["keypoint"]
        print(time.time() - start_time > 3)
        if time.time() - start_time > 3:
            if abs(float(now_hand_xy[1]) - float(before_hand_xy[1])) > 0.6:
                print("too meny hand move")
            elif float(now_hand_xy[1]) - float(before_hand_xy[1]) < -0.1:
                print("right slide!============================================")
                pyautogui.press('right')
                start_time = time.time()
            elif float(now_hand_xy[1]) - float(before_hand_xy[1]) > 0.1:
                print("left slide!============================================")
                pyautogui.press('left')
                start_time = time.time()
        else:
            print(abs(float(now_hand_xy[1])))
        before_hand_xy = now_hand_xy

# 終了条件
    # Qキーが押されると停止
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()
