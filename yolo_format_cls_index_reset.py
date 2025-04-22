import os

# YOLO 라벨 파일이 있는 폴더
label_dir = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge_bbox_refined/test/labels'  # 예시: 'labels/' 폴더

# class id 매핑 규칙
class_mapping = {
    3:4,
    4:3
}

# 라벨 파일 리스트 가져오기
label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

for label_file in label_files:
    label_path = os.path.join(label_dir, label_file)

    with open(label_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue  # 빈 줄은 스킵

        old_class_id = int(parts[0])
        rest = parts[1:]

        # 매핑된 class id로 변경
        new_class_id = class_mapping.get(old_class_id, old_class_id)  # 없는 경우는 그대로
        new_line = f"{new_class_id} " + " ".join(rest)
        new_lines.append(new_line)

    # 파일 덮어쓰기 (주의: 원본을 수정합니다)
    with open(label_path, 'w') as f:
        f.write("\n".join(new_lines) + "\n")

print("✅ 모든 라벨 파일 class id 재매핑 완료!")
