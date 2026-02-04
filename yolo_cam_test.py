from ultralytics import YOLO
import cv2

# YOLO 기본 모델 (COCO pretrained)
model = YOLO("yolov8n.pt")

# 웹캠 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라 열기 실패")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    # YOLO 추론
    results = model(frame, conf=0.5, verbose=False)

    # 결과 시각화
    annotated = results[0].plot()

    cv2.imshow("YOLO Webcam Test", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
