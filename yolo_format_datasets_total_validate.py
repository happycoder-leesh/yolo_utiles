#!/usr/bin/env python3
"""
YOLO Dataset Checker

This script performs integrity checks and statistics on a YOLO-format dataset, supporting both directory layouts:
A) root/train/images, root/train/labels, root/val/images, root/val/labels[, root/test/images, root/test/labels]
B) root/images/train, root/labels/train, root/images/val, root/labels/val[, root/images/test, root/labels/test]

Checks performed:
1. Verifies that the number of images and labels match for each subset (train, val[, test]).
2. Reports unexpected file types in image/label folders.
3. Displays the ratio of train vs. val[, vs. test] images.
4. Counts instances per class ID for each subset separately.

Usage:
    python yolo_dataset_checker.py <root> [--check-test]

Options:
    --check-test    Include 'test' subset in checks if its folders are present.
"""
import os
import argparse
from collections import Counter

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
LABEL_EXTENSION = '.txt'


def detect_structure(root, include_test=False):
    # Scheme A: root/{train,val[,test]}/images & labels
    subsets = ['train', 'val'] + (['test'] if include_test else [])
    paths = {}
    for subset in subsets:
        img_dir = os.path.join(root, subset, 'images')
        lbl_dir = os.path.join(root, subset, 'labels')
        if os.path.isdir(img_dir) and os.path.isdir(lbl_dir):
            paths[subset] = {'images': img_dir, 'labels': lbl_dir}
        elif include_test and subset == 'test':
            # If test not present under scheme A, skip
            continue
        else:
            # Try scheme B only if checking train/val; test handled above
            if subset in ['train', 'val']:
                img_dir = os.path.join(root, 'images', subset)
                lbl_dir = os.path.join(root, 'labels', subset)
                if os.path.isdir(img_dir) and os.path.isdir(lbl_dir):
                    paths[subset] = {'images': img_dir, 'labels': lbl_dir}
                else:
                    raise FileNotFoundError(f"Could not locate '{subset}' folders under either supported structure.")
    return paths


def list_files(folder):
    try:
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except FileNotFoundError:
        return []


def main(root, check_test):
    paths = detect_structure(root, include_test=check_test)
    total_images = 0
    subset_counts = {}
    class_counters = {subset: Counter() for subset in paths}

    print(f"Dataset root: {root}\n")

    # Per-subset checks
    for subset, dirs in paths.items():
        img_folder = dirs['images']
        lbl_folder = dirs['labels']

        files_img = list_files(img_folder)
        files_lbl = list_files(lbl_folder)

        valid_images = [f for f in files_img if f.lower().endswith(IMAGE_EXTENSIONS)]
        valid_labels = [f for f in files_lbl if f.lower().endswith(LABEL_EXTENSION)]
        other_images = [f for f in files_img if f not in valid_images]
        other_labels = [f for f in files_lbl if f not in valid_labels]

        image_bases = set(os.path.splitext(f)[0] for f in valid_images)
        label_bases = set(os.path.splitext(f)[0] for f in valid_labels)
        missing_labels = image_bases - label_bases
        missing_images = label_bases - image_bases

        print(f"[{subset.upper()}] Images: {len(valid_images)}, Labels: {len(valid_labels)}")
        if missing_labels:
            print(f"  {len(missing_labels)} images missing labels: {sorted(missing_labels)[:5]}{'...' if len(missing_labels)>5 else ''}")
        if missing_images:
            print(f"  {len(missing_images)} labels missing images: {sorted(missing_images)[:5]}{'...' if len(missing_images)>5 else ''}")
        if other_images:
            print(f"  {len(other_images)} unexpected files in images: {other_images[:3]}{'...' if len(other_images)>3 else ''}")
        if other_labels:
            print(f"  {len(other_labels)} unexpected files in labels: {other_labels[:3]}{'...' if len(other_labels)>3 else ''}")

        subset_counts[subset] = len(valid_images)
        total_images += len(valid_images)

        # Count class instances per subset
        for lbl_file in valid_labels:
            path = os.path.join(lbl_folder, lbl_file)
            with open(path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        class_id = parts[0]
                        class_counters[subset][class_id] += 1

    # Train/Val[/Test] split ratios
    print("\nData split ratios:")
    for subset in paths:
        cnt = subset_counts.get(subset, 0)
        pct = (cnt / total_images * 100) if total_images else 0
        print(f"  {subset.capitalize()}: {cnt} images ({pct:.2f}%)")

    # Class distribution per subset
    print("\nClass instance counts per subset:")
    for subset, counter in class_counters.items():
        print(f"\n  {subset.capitalize()}: {sum(counter.values())} instances")
        for cls_id, cnt in sorted(counter.items(), key=lambda x: int(x[0])):
            print(f"    Class {cls_id}: {cnt}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check YOLO-format dataset integrity and statistics.')
    parser.add_argument('--root', help='Root directory of the dataset')
    parser.add_argument('--check-test', action='store_true', help='Include test subset if present')
    args = parser.parse_args()
    main(args.root, args.check_test)
