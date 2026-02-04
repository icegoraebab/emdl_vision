### 카메라 세팅 설치 파일
```
sudo apt update
sudo apt install v4l-utils -y
```
```
# 웹캠 인식 확인
v4l2-ctl --list-devices
```
USB Camera (usb-0000:00:14.0-5):
    /dev/video0 식으로 나오면 성공

```
# OpenCV 테스트
cd ~/emdl_vision
python3 cam_test.py
```
화면 잘 뜨면 ok

---
### 사진 데이터 수집(이미 있으면 스킵)
```
# s키로 촬영
python3 capture_lipbalm.py
```
##### 다양한 각도, 높이, 깊이, 밝기, 다양한 장애물 배경 유/무 포함해서 약70장 이상 촬영하기.

### 데이터셋 폴더 준비
```
mkdir -p lipbalm_dataset/images
mkdir -p lipbalm_dataset/labels
cp lipbalm_data/*.jpg lipbalm_dataset/images/
```

### OpenCV 기반 라벨링
```
python3 opencv_labeler.py
```
##### 마우스 드래그: 박스생성, r: 박스 리셋, n: 다음이미지
이러면 
/emdl_vision/lipbalm_dataset_labels에 좌표변환으로 .txt로 저장됨

---

#### YOLO 설치
```
# YOLO 전용 venv 만들기(서버 꼬이지 않게 하기 위함)
cd ~
python3 -m venv yolo_env
source yolo_env/bin/activate
```
이제 좌측에 (yolo_env) 뜨면 성공

```
# 필수 패키지 설치

pip install --upgrade pip
pip install ultralytics opencv-python numpy

# 설치 확인
yolo version

```


### YOLOv8 학습, 충돌을 피하기 위해 가상환경 env 활성화 해야함.
```
source ~/yolo_env/bin/activate

yolo train \
  data=lipbalm_dataset/data.yaml \
  model=yolov8n.pt \
  epochs=50 \
  imgsz=640 \
  batch=8 \
  device=0

```
#### YOLO 결과 확인(웹캠 같이 켜짐)
```
yolo predict \
  model=runs/detect/train/weights/best.pt \
  source=0 \
  conf=0.4 \
  show=True
```



### 목표:
##### 카메라 -> YOLO Detector -> 각 bbox -> TTC 계산(객체선정) -> Tracker -> Allegrohand 잡기


~/emdl_vision/lipbalm_data/labels

(없으면 자동 생성됨)


---
일단 yolo 패스, 대기
