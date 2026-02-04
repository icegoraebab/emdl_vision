import cv2
import os

# 저장 경로
save_dir = "lipbalm_data/images"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라 열기 실패")
    exit()

idx = 0
print("s: 이미지 저장 | q: 종료")

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    cv2.imshow("Capture Lipbalm", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"{save_dir}/lipbalm_{idx}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        idx += 1

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

