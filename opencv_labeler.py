import cv2
import os

IMG_DIR = "lipbalm_dataset/images"
LBL_DIR = "lipbalm_dataset/labels"
CLASS_ID = 0  # lipbalm

os.makedirs(LBL_DIR, exist_ok=True)

drawing = False
ix, iy = -1, -1
boxes = []

def draw_rect(event, x, y, flags, param):
    global ix, iy, drawing, boxes
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        boxes.append((ix, iy, x, y))

for img_name in os.listdir(IMG_DIR):
    img_path = os.path.join(IMG_DIR, img_name)
    label_path = os.path.join(LBL_DIR, img_name.replace(".jpg", ".txt"))

    img = cv2.imread(img_path)
    h, w, _ = img.shape
    boxes = []

    cv2.namedWindow("label")
    cv2.setMouseCallback("label", draw_rect)

    while True:
        tmp = img.copy()
        for b in boxes:
            cv2.rectangle(tmp, (b[0], b[1]), (b[2], b[3]), (0,255,0), 2)
        cv2.imshow("label", tmp)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('n'):  # next image
            break
        elif key == ord('r'):  # reset boxes
            boxes = []

    cv2.destroyAllWindows()

    with open(label_path, "w") as f:
        for (x1, y1, x2, y2) in boxes:
            xc = ((x1 + x2) / 2) / w
            yc = ((y1 + y2) / 2) / h
            bw = abs(x2 - x1) / w
            bh = abs(y2 - y1) / h
            f.write(f"{CLASS_ID} {xc} {yc} {bw} {bh}\n")

print("라벨링 완료")
