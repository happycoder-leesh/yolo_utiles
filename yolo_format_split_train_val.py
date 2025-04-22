import os
import glob
import random
import shutil

# === 설정 ===
source_image_dir = '/home/oms/leesh/raw_data/HTS_abandonment_final/refined_250418/images'  # 원본 이미지 폴더
source_label_dir = '/home/oms/leesh/raw_data/HTS_abandonment_final/refined_250418/labels'  # 원본 라벨 폴더

output_base_dir = '/home/oms/leesh/raw_data/HTS_abandonment_final/refined_250418_split'   # 나눌 output base 폴더
train_ratio = 0.8                     # 8:2 train/val 비율

# output 디렉토리 구조 만들기
train_image_dir = os.path.join(output_base_dir, 'train', 'images')
train_label_dir = os.path.join(output_base_dir, 'train', 'labels')
val_image_dir = os.path.join(output_base_dir, 'val', 'images')
val_label_dir = os.path.join(output_base_dir, 'val', 'labels')

for d in [train_image_dir, train_label_dir, val_image_dir, val_label_dir]:
    os.makedirs(d, exist_ok=True)

# === 이미지 파일 리스트 ===
image_paths = glob.glob(os.path.join(source_image_dir, '*.jpg')) + glob.glob(os.path.join(source_image_dir, '*.png'))

# === 섞기 ===
random.shuffle(image_paths)

# === 나누기 ===
split_idx = int(len(image_paths) * train_ratio)
train_images = image_paths[:split_idx]
val_images = image_paths[split_idx:]

def copy_data(image_list, img_dst_dir, lbl_dst_dir):
    for img_path in image_list:
        file_name = os.path.basename(img_path)
        name_wo_ext = os.path.splitext(file_name)[0]
        label_path = os.path.join(source_label_dir, name_wo_ext + '.txt')

        # 이미지 복사
        shutil.copy(img_path, os.path.join(img_dst_dir, file_name))

        # 레이블 복사
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(lbl_dst_dir, name_wo_ext + '.txt'))
        else:
            print(f"[경고] 라벨 파일 없음: {label_path}")

# === 복사 수행 ===
copy_data(train_images, train_image_dir, train_label_dir)
copy_data(val_images, val_image_dir, val_label_dir)

print(f"[INFO] 완료! 총 {len(train_images)}개 train, {len(val_images)}개 val 데이터가 저장되었습니다.")
