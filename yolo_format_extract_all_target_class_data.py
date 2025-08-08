import os
import shutil
import glob
import argparse

def main(args):
    os.makedirs(args.output_image_dir, exist_ok=True)
    os.makedirs(args.output_label_dir, exist_ok=True)

    # 모든 확장자 지원
    image_paths = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tif', '*.tiff', '*.webp'):
        image_paths.extend(glob.glob(os.path.join(args.image_dir, ext)))

    for img_path in image_paths:
        file_name = os.path.basename(img_path)
        label_path = os.path.join(args.label_dir, os.path.splitext(file_name)[0] + '.txt')

        if not os.path.exists(label_path):
            continue

        with open(label_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            continue

        # 모든 클래스가 target_classes 안에만 있으면 복사
        valid = all(int(line.strip().split()[0]) in args.target_classes for line in lines if line.strip())

        if valid:
            shutil.copy(img_path, os.path.join(args.output_image_dir, file_name))
            shutil.copy(label_path, os.path.join(args.output_label_dir, os.path.splitext(file_name)[0] + '.txt'))

    print(f"[INFO] 완료! {args.output_image_dir} 와 {args.output_label_dir}에 타겟 클래스만 있는 데이터가 저장되었습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract YOLO-format dataset only in target classes')
    parser.add_argument('--image_dir', type=str, required=True, help="Origin image directory")
    parser.add_argument('--label_dir', type=str, required=True, help="Origin label directory")
    parser.add_argument('--target_classes', nargs='+', type=int, required=True,
                        help='Target class IDs (e.g., 0 8 9 10 11 12)')
    parser.add_argument('--output_image_dir', type=str, required=True, help="Output image directory")
    parser.add_argument('--output_label_dir', type=str, required=True, help="Output label directory")
    args = parser.parse_args()

    main(args)
