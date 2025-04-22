#!/usr/bin/env python3
import os
import glob
import shutil
from PIL import Image

# === 설정 (global variables) ===
DATA_ROOT = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge'           # 데이터 폴더 (하위에 train/val/test)
DST_ROOT  = '/home/oms/leesh/raw_data/roboflow_datasets/furniture_huge_bbox'       # 변환된 데이터셋을 저장할 루트
SPLITS    = ['train', 'valid', 'test']
EXTS      = ['.jpg', '.png', '.jpeg']

def convert_seg_to_det(split):
    """
    YOLOv5-seg 포맷 라벨(.txt)에서 클래스 인덱스를 제외한
    모든 세그멘테이션 포인트를 사용해 bbox를 재계산 후
    YOLOv5 object detection 포맷으로 저장.
    """
    src_lbl = os.path.join(DATA_ROOT, split, 'labels')
    dst_lbl = os.path.join(DST_ROOT, split, 'labels')
    src_img = os.path.join(DATA_ROOT, split, 'images')
    os.makedirs(dst_lbl, exist_ok=True)

    for lbl_path in glob.glob(os.path.join(src_lbl, '*.txt')):
        base = os.path.splitext(os.path.basename(lbl_path))[0]
        # 대응 이미지
        img_path = None
        for ext in EXTS:
            p = os.path.join(src_img, base + ext)
            if os.path.exists(p):
                img_path = p
                break
        if img_path is None:
            print(f"[WARN] 이미지 없음: {base} (skipped)")
            continue

        # 실제 이미지 크기
        W, H = Image.open(img_path).size
        out_lines = []

        with open(lbl_path, 'r') as f:
            for line in f:
                tokens = line.strip().split()
                if len(tokens) < 7:
                    # 최소 class + x_c,y_c,w,h + 한 점 필요
                    continue
                cls = tokens[0]
                # segmentation 포인트 (normalized relative coords) 추출
                seg_vals = list(map(float, tokens[5:]))
                xs_norm = seg_vals[0::2]
                ys_norm = seg_vals[1::2]
                # pixel coords 계산
                xs = [x * W for x in xs_norm]
                ys = [y * H for y in ys_norm]
                xmin, xmax = min(xs), max(xs)
                ymin, ymax = min(ys), max(ys)
                # 다시 normalized center, width, height
                x_c = (xmin + xmax) / 2 / W
                y_c = (ymin + ymax) / 2 / H
                bw  = (xmax - xmin) / W
                bh  = (ymax - ymin) / H
                out_lines.append(f"{cls} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}")

        # 저장
        dst_path = os.path.join(dst_lbl, base + '.txt')
        with open(dst_path, 'w') as f:
            f.write('\n'.join(out_lines))


def copy_images(split):
    """images 폴더를 그대로 복사"""
    src = os.path.join(DATA_ROOT, split, 'images')
    dst = os.path.join(DST_ROOT, split, 'images')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


# === 실행 ===
if __name__ == '__main__':
    for sp in SPLITS:
        print(f"[{sp}] 변환 시작: labels & images")
        convert_seg_to_det(sp)
        copy_images(sp)
    print("모든 split 변환 완료! det_dataset/ 폴더를 확인하세요.")
