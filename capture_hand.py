import cv2
import os
import time

save_dir = "datasets/hand_dataset/images"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

idx = len(os.listdir(save_dir))

print("SPACE: capture | Q: quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("hand_capture", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        fname = f"hand_{idx:04d}.jpg"
        cv2.imwrite(os.path.join(save_dir, fname), frame)
        print(f"saved {fname}")
        idx += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
