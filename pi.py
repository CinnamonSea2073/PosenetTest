# ラズベリーパイのコード

import cv2
import requests
import base64

# カメラの初期化
# おまじない的なやつ
cap = cv2.VideoCapture(0)

while True:
    # フレームの取得
    # ここが実行された時点でのフレームをもらう
    ret, frame = cap.read()

    # 画像をBase64にエンコード
    # Base64という通信する際によく使うよう形式に変換
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

    # サーバーに画像を送信
    # URLは後で教える
    server_url = "https://strong-kentucky-con-notebooks.trycloudflare.com/analyze_image"
    data = {'file': img_base64}
    response = requests.post(server_url, json=data)

    # サーバーからの応答を処理
    # もらったデータの後処理　ここは有村さんがよしなにする場所
    result = response.json()
    print(result)  # ここでポーズの情報を取得

    # 処理など

    # 終了条件
    # Qキーが押されると停止
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()