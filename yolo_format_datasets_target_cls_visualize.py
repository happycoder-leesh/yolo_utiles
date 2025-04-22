import os
import cv2

# 1. 설정: 정수 하나 또는 리스트로 지정 가능
#    예: target_classes = 2          -> 클래스 2만
#        target_classes = [0, 2, 5]  -> 클래스 0, 2, 5
target_classes = [9, 10]  # 또는 target_classes = 2

# int로 들어왔으면 리스트로 래핑
if isinstance(target_classes, int):
    target_classes = [target_classes]

input_image_dir = '/home/oms/leesh/raw_data/yolo_final_datasets/abandonment_v3/val/images'      
input_label_dir = '/home/oms/leesh/raw_data/yolo_final_datasets/abandonment_v3/val/labels'      
output_dir      = '/home/oms/leesh/raw_data/yolo_datasets_visualize/abandonment_v3'      

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_image_dir):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img_path   = os.path.join(input_image_dir, filename)
    lbl_path   = os.path.join(input_label_dir, os.path.splitext(filename)[0] + '.txt')
    if not os.path.isfile(lbl_path):
        continue

    # 레이블 읽고, 클래스가 target_classes에 포함된 라인만 필터
    with open(lbl_path, 'r') as f:
        lines = [line.strip().split() for line in f]
    filtered = [ln for ln in lines if int(ln[0]) in target_classes]
    if not filtered:
        continue  # 대상 클래스가 없으면 저장하지 않음

    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # BBox 그리기
    for ln in filtered:
        _, xc, yc, bw, bh = map(float, ln)
        x1 = int((xc - bw/2) * w)
        y1 = int((yc - bh/2) * h)
        x2 = int((xc + bw/2) * w)
        y2 = int((yc + bh/2) * h)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 저장
    save_path = os.path.join(output_dir, filename)
    cv2.imwrite(save_path, img)