import os
import cv2
import argparse

# 1. 설정: 정수 하나 또는 리스트로 지정 가능
#    예: target_classes = 2          -> 클래스 2만
#        target_classes = [0, 2, 5]  -> 클래스 0, 2, 5

# int로 들어왔으면 리스트로 래핑

def main(args):
    
    if isinstance(args.target_classes, int):
        target_classes = [args.target_classes]
    
    os.makedirs(args.output_dir, exist_ok=True)

    for filename in os.listdir(args.image_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path   = os.path.join(args.image_dir, filename)
        lbl_path   = os.path.join(args.label_dir, os.path.splitext(filename)[0] + '.txt')
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
        save_path = os.path.join(args.output_dir, filename)
        cv2.imwrite(save_path, img)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize YOLO-format dataset in target classes')
    parser.add_argument('--image_dir', type=str, required=True, help="Input image directory")
    parser.add_argument('--label_dir', type=str, required=True, help="Input label directory")
    parser.add_argument('--target_classes', nargs='+', type=int, required=True,
                        help='Target class IDs (e.g., 0 8 9 10 11 12)')
    parser.add_argument('--output_dir', type=str, required=True, help="Output Visualize directory")
    args = parser.parse_args()

    main(args)
