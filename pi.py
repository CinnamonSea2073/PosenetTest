# ラズベリーパイのコード

import cv2
import requests
import base64
import io

API_BACKEND = "https://strong-kentucky-con-notebooks.trycloudflare.com/analyze_image"

# カメラの初期化
# おまじない的なやつ
cap = cv2.VideoCapture(0)
before_hand_xy = ["0.0", "0.0"]

while True:
    # フレームの取得
    # ここが実行された時点でのフレームをもらう
    ret, frame = cap.read()
    

    # 画像をBase64にエンコード
    # Base64という通信する際によく使うよう形式に変換
    _, img_encoded = cv2.imencode('.jpg', frame)

    # サーバーに画像を送信
    # URLは後で教える
    data = {'file': img_encoded.tobytes()}
    response = requests.post(API_BACKEND, files=data)

    # サーバーからの応答を処理
    # もらったデータの後処理　ここは有村さんがよしなにする場所
    result = response.json()
    # print(result)  # ここでポーズの情報を取得

    # 処理など
    # {"result": [{"keypoint": ["0.78029966", "0.5728703"], "score": "0.08736164"}, {"keypoint": ["0.78356224", "0.59705037"], "score": "0.050445005"}, {"keypoint": ["0.7785975", "0.55700916"], "score": "0.10149876"}, {"keypoint": ["0.75297713", "0.6492638"], "score": "0.052804213"}, {"keypoint": ["0.71502644", "0.54231167"], "score": "0.12934819"}, {"keypoint": ["0.6762762", "0.70831716"], "score": "0.11155443"}, {"keypoint": ["0.6733827", "0.50115085"], "score": "0.06694978"}, {"keypoint": ["0.81954867", "0.73362607"], "score": "0.043085728"}, {"keypoint": ["0.7464619", "0.48400852"], "score": "0.046659775"}, {"keypoint": ["0.79072315", "0.6747813"], "score": "0.1017642"}, {"keypoint": ["0.7362591", "0.5509906"], "score": "0.08165453"}, {"keypoint": ["0.6607163", "0.5889795"], "score": "0.017532267"}, {"keypoint": ["0.6535227", "0.47141823"], "score": "0.036361642"}, {"keypoint": ["0.8305186", "0.6035999"], "score": "0.010516134"}, {"keypoint": ["0.7838333", "0.46694455"], "score": "0.02315922"}, {"keypoint": ["0.7818023", "0.597459"], "score": "0.04455198"}, {"keypoint": ["0.67810047", "0.43701896"], "score": "0.023499884"}], "time": "0.09754014015197754", "fps": "10.252189492878495"}
    
    now_hand_xy = eval(result)["result"][10]["keypoint"]
    if abs(float(now_hand_xy[1]) - float(before_hand_xy[1])) > 0.03:
        print("slide!============================================")
    print(abs(float(now_hand_xy[1])))
    before_hand_xy = now_hand_xy
    
    height, width, _ = frame.shape
    for i in eval(result)["result"]:
        y, x = int(256*(height/256)*float(i["keypoint"][0])), int(256*(width/256)*float(i["keypoint"][1]))
        cv2.circle(frame, (x, y), 40, (0, 255, 0), -1)
    cv2.imshow('preview', frame)
    # print("reloading...")

# 終了条件
    # Qキーが押されると停止
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()