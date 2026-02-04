import cv2
import numpy as np
import mss

tracker = cv2.TrackerCSRT_create()
sct = mss.mss()

monitor = sct.monitors[1]  # 전체 화면
initBB = None

while True:
    img = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    if initBB is not None:
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = map(int, box)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow("Tracking", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initBB = cv2.selectROI("Tracking", frame, False)
        tracker.init(frame, initBB)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
