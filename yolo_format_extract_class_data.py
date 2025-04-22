import os
import shutil
import glob

# === 설정 ===
image_dir = '/home/oms/leesh/raw_data/HTS_abandonment/train/coco/coco/images'   # 원본 이미지 폴더
label_dir = '/home/oms/leesh/raw_data/HTS_abandonment/train/coco/coco/labels'   # 원본 레이블 폴더

target_cls_ids = {1, 2}      # 추출할 클래스 인덱스 집합 (예: 0, 2, 5번 클래스만)

output_image_dir = '/home/oms/leesh/raw_data/HTS_abandonment/train/coco/coco_extract/images'
output_label_dir = '/home/oms/leesh/raw_data/HTS_abandonment/train/coco/coco_extract/labels'

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

# === 이미지 + 라벨 경로 ===
image_paths = glob.glob(os.path.join(image_dir, '*.jpg'))  # 필요하면 .png 등으로 수정

for img_path in image_paths:
    file_name = os.path.basename(img_path)
    label_path = os.path.join(label_dir, file_name.replace('.jpg', '.txt'))  # .png면 수정 필요

    if not os.path.exists(label_path):
        continue  # 라벨 파일 없으면 스킵

    with open(label_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        continue  # 빈 파일은 스킵

    valid = True
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        cls_id = int(parts[0])
        if cls_id not in target_cls_ids:
            valid = False
            break

    # 만약 모든 클래스가 target_cls_ids 안에만 있으면
    if valid:
        # 이미지 복사
        shutil.copy(img_path, os.path.join(output_image_dir, file_name))
        # 라벨 복사 (필터링 없이 전체 저장)
        shutil.copy(label_path, os.path.join(output_label_dir, file_name.replace('.jpg', '.txt')))

print(f"[INFO] 완료! {output_image_dir} 와 {output_label_dir}에 타겟 클래스만 있는 데이터가 저장되었습니다.")
