import cv2

# カメラの初期化
cap = cv2.VideoCapture(0)

# 保存先ディレクトリ
save_directory = "python用/"
image_count = 0

while True:
    # フレームの取得
    ret, frame = cap.read()

    # 画像を保存
    image_filename = f"{save_directory}image_{image_count}.jpg"
    cv2.imwrite(image_filename, frame)

    print(f"Image saved: {image_filename}")

    image_count += 1

    # 終了条件
    # Qキーが押されると停止
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()
