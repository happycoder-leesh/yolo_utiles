import os
import json
import argparse


def parse_pairs(mapping_list):
    """
    ['3=4', '4=3'] 같은 리스트를 받아 {3:4,4:3} 으로 변환
    """
    mapping = {}
    for item in mapping_list:
        try:
            key_str, val_str = item.split("=")
            key = int(key_str)
            val = int(val_str)
            mapping[key] = val
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"올바른 형식의 매핑이 아닙니다: '{item}'. 예: 3=4"
            )
    return mapping

def main():
    
    parser = argparse.ArgumentParser(
        description=""
    )
    
    parser.add_argument(
        "-l", "--label_path",
        default="",
        required=True
    )
    
    parser.add_argument(
        "--class-mapping-json",
        type=str,
        help="클래스 매핑을 JSON 문자열로 전달 (예: --class-mapping-json '{\"3\":4,\"4\":3}')",
    )
    
    args = parser.parse_args()
    
    
    try:
        class_mapping = {int(k): int(v) for k, v in json.loads(args.class_mapping_json).items()}
    except (ValueError, json.JSONDecodeError) as e:
        parser.error(f"JSON 매핑 파싱 오류: {e}")
    
     # 변수 사용 예시
    if args.verbose:
        print("=== 파싱된 매개변수 ===")
        print(f"Input file      : {args.input_file}")
        print(f"class_mapping   : {class_mapping}")
        print("=======================")
    
    
    label_files = [f for f in os.listdir(args.label_path) if f.endswith('.txt')]
    
    for label_file in label_files:
        label_path = os.path.join(args.label_path, label_file)

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
    
if __name__ == "__main__":
    main()