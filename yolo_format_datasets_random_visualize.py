import cv2
import glob
import os
import random

# === 설정 ===
image_dir = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge_bbox_refined/train/images'
label_dir = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge_bbox_refined/train/labels'
output_dir = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge_bbox_refined/train/visualized'

os.makedirs(output_dir, exist_ok=True)

# 이미지 + 라벨 읽기
image_paths = glob.glob(os.path.join(image_dir, '*.jpg'))
# 전체 이미지 중 30%를 무작위로 선택
selected_image_paths = random.sample(image_paths, int(len(image_paths) * 0.05))

for img_path in selected_image_paths:
    file_name = os.path.basename(img_path)
    label_path = os.path.join(label_dir, file_name.replace('.jpg', '.txt'))

    # 이미지 로드
    img = cv2.imread(img_path)
    h, w, _ = img.shape

    # 라벨이 존재하면 읽어서 박스 그리기
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if not line.strip():  # 공백 줄 무시
                continue
            parts = line.strip().split()
            cls_id = int(parts[0])                 # 맨 앞은 클래스 인덱스
            cx, cy, bw, bh = map(float, parts[1:5])  # 그 다음 4개는 중심 좌표와 너비, 높이

            # YOLO 좌표 → x1, y1, x2, y2 변환
            x1 = int((cx - bw / 2) * w)
            y1 = int((cy - bh / 2) * h)
            x2 = int((cx + bw / 2) * w)
            y2 = int((cy + bh / 2) * h)

            # 박스와 클래스 인덱스 그리기
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, str(cls_id), (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 결과 저장
    cv2.imwrite(os.path.join(output_dir, file_name), img)

print(f"[INFO] 30%로 선택된 이미지에 대해 시각화된 이미지가 {output_dir} 폴더에 저장되었습니다.")
