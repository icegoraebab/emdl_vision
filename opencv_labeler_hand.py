import cv2
import os

IMG_DIR = "datasets/hand_dataset/images"
LBL_DIR = "datasets/hand_dataset/labels"
os.makedirs(LBL_DIR, exist_ok=True)

images = sorted([f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")])
idx = 0
bbox = None
drawing = False
ix, iy = -1, -1

def draw_rect(event, x, y, flags, param):
    global ix, iy, drawing, bbox
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        bbox = (ix, iy, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox = (ix, iy, x, y)

while idx < len(images):
    img_path = os.path.join(IMG_DIR, images[idx])
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    bbox = None

    cv2.namedWindow("label_hand")
    cv2.setMouseCallback("label_hand", draw_rect)

    while True:
        disp = img.copy()
        if bbox:
            cv2.rectangle(disp, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0,255,0), 2)
        cv2.imshow("label_hand", disp)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and bbox:
            x1, y1, x2, y2 = bbox
            xc = ((x1 + x2) / 2) / w
            yc = ((y1 + y2) / 2) / h
            bw = abs(x2 - x1) / w
            bh = abs(y2 - y1) / h

            label_path = os.path.join(LBL_DIR, images[idx].replace(".jpg", ".txt"))
            with open(label_path, "w") as f:
                f.write(f"0 {xc} {yc} {bw} {bh}\n")

            print(f"saved label for {images[idx]}")
            idx += 1
            break

        elif key == ord('d'):
            print("skip")
            idx += 1
            break

        elif key == ord('q'):
            exit()

cv2.destroyAllWindows()
