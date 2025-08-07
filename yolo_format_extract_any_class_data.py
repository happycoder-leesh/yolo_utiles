import os
import shutil
import glob

# === 설정 ===
image_dir = '/home/omeye/leesh/yolo_datasets/abandonment_v7_non_coco/test/images'
label_dir = '/home/omeye/leesh/yolo_datasets/abandonment_v7_non_coco/test/labels'

# 추출할 클래스 인덱스 집합
target_cls_ids = {0, 8, 9, 10, 11, 12, 13, 14}

# 출력 디렉터리
output_image_dir = '/home/omeye/leesh/yolo_datasets/abandonment_kisa_v4/test/images'
output_label_dir = '/home/omeye/leesh/yolo_datasets/abandonment_kisa_v4/test/labels'

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

# 지원할 이미지 확장자 리스트
image_exts = ['.jpg', '.jpeg', '.png']

for ext in image_exts:
    pattern = os.path.join(image_dir, f'*{ext}')
    for img_path in glob.glob(pattern):
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(label_dir, base_name + '.txt')

        if not os.path.exists(label_path):
            continue

        # 레이블 파일 읽기
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # target_cls_ids에 속한 라인만 필터링
        filtered = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            cls_id = int(parts[0])
            if cls_id in target_cls_ids:
                filtered.append(line)

        # 필터된 결과가 있으면 복사/저장
        if filtered:
            # 이미지 복사
            shutil.copy(img_path, os.path.join(output_image_dir, os.path.basename(img_path)))
            # 필터된 레이블 쓰기
            with open(os.path.join(output_label_dir, base_name + '.txt'), 'w') as fw:
                fw.writelines(filtered)

print(f"[INFO] 완료! {output_image_dir} 및 {output_label_dir}에 필터링된 데이터셋이 저장되었습니다.")
