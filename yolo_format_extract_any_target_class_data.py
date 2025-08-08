import os
import shutil
import glob
import argparse


def main(args):
    os.makedirs(args.output_image_dir, exist_ok=True)
    os.makedirs(args.output_label_dir, exist_ok=True)

    # 지원할 이미지 확장자 리스트
    image_exts = ['.jpg', '.jpeg', '.png']

    for ext in image_exts:
        pattern = os.path.join(args.image_dir, f'*{ext}')
        for img_path in glob.glob(pattern):
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            label_path = os.path.join(args.label_dir, base_name + '.txt')

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
                if cls_id in args.target_classes:
                    filtered.append(line)

            # 필터된 결과가 있으면 복사/저장
            if filtered:
                # 이미지 복사
                shutil.copy(img_path, os.path.join(args.output_image_dir, os.path.basename(img_path)))
                # 필터된 레이블 쓰기
                with open(os.path.join(args.output_label_dir, base_name + '.txt'), 'w') as fw:
                    fw.writelines(filtered)

    print(f"[INFO] 완료! {args.output_image_dir} 및 {args.output_label_dir}에 필터링된 데이터셋이 저장되었습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract YOLO-format dataset any in target classes')
    parser.add_argument('--image_dir', type=str, required=True, help="Origin image directory")
    parser.add_argument('--label_dir', type=str, required=True, help="Origin label directory")
    parser.add_argument('--target_classes', nargs='+', type=int, required=True,
                        help='Target class IDs (e.g., 0 8 9 10 11 12)')
    parser.add_argument('--output_image_dir', type=str, required=True, help="Output image directory")
    parser.add_argument('--output_label_dir', type=str, required=True, help="Output label directory")
    args = parser.parse_args()

    main(args)