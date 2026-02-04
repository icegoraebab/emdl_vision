import cv2
import time
import numpy as np

# ---------- Camera ----------
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# ---------- Tracker ----------
tracker = cv2.TrackerCSRT_create()
initBB = None

# ---------- TTC variables ----------
prev_area = None
prev_time = None
ttc = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()

    if initBB is not None:
        success, box = tracker.update(frame)

        if success:
            x, y, w, h = map(int, box)
            area = w * h

            # Draw bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

            if prev_area is not None:
                dt = now - prev_time
                dA = area - prev_area

                if dA > 0 and dt > 0:
                    ttc = area / (dA / dt)
                else:
                    ttc = None

            prev_area = area
            prev_time = now

            # Display area
            cv2.putText(frame, f"Area: {area}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

            # Display TTC
            if ttc is not None and ttc < 5.0:
                cv2.putText(frame, f"TTC: {ttc:.2f} s",
                            (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "TTC: inf",
                            (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 2)

    cv2.imshow("Tracking + TTC", frame)
    key = cv2.waitKey(1) & 0xFF

    # s 키로 ROI 선택
    if key == ord('s'):
        initBB = cv2.selectROI("Tracking + TTC", frame, False)
        tracker.init(frame, initBB)
        prev_area = None
        prev_time = None
        ttc = None

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
