# ラズベリーパイのコード

import cv2
import requests
import base64
import io
import asyncio
import aiohttp

API_BACKEND = "https://strong-kentucky-con-notebooks.trycloudflare.com/analyze_image"

async def capture_and_send_frames(frame):
    async with aiohttp.ClientSession() as session:
        _, img_encoded = cv2.imencode('.jpg', frame)
        data = {'file': img_encoded.tobytes()}
        async with session.post(API_BACKEND, data=data) as response:
            result = await response.json(content_type='application/json')
    
        height, width, _ = frame.shape
        for i in eval(result)["result"]:
            y, x = int(256*(height/256)*float(i["keypoint"][0])), int(256*(width/256)*float(i["keypoint"][1]))
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
        cv2.imshow('preview', frame)

        return eval(result)["result"][10]

async def main():
    cap = cv2.VideoCapture(0)
    before_hand_xy = ["0.0", "0.0"]
    while True:
        ret, frame = cap.read()
        now_hand_xy = await capture_and_send_frames(frame)
        if float(now_hand_xy["score"]) < 0.5:
            continue
        if abs(float(now_hand_xy["keypoint"][1]) - float(before_hand_xy["keypoint"][1])) > 0.04:
            print("slide!============================================")
        else:
            print(abs(float(now_hand_xy["keypoint"][1])), abs(float(before_hand_xy["score"])))
        before_hand_xy = now_hand_xy["keypoint"]
    # リソースの解放
    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())

