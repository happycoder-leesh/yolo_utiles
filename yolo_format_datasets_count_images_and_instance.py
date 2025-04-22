import os
import glob
from collections import Counter

def count_yolo_labels(labels_dir):
    """
    labels_dir 경로 내의 모든 .txt 레이블 파일을 읽어
    이미지 수와 클래스별 인스턴스 수를 반환합니다.
    
    Args:
        labels_dir (str): YOLO 레이블(.txt) 파일들이 모여 있는 디렉토리 경로.
        
    Returns:
        total_images (int): 레이블 파일(.txt) 개수 = 이미지 수
        class_counts (Counter): {class_index: instance_count, ...}
    """
    # 1) 레이블 파일 목록 가져오기
    pattern = os.path.join(labels_dir, '*.txt')
    label_files = glob.glob(pattern)
    
    total_images = len(label_files)
    class_counts = Counter()
    
    # 2) 각 파일 파싱
    for file_path in label_files:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                cls_idx = int(parts[0])  # YOLO 포맷에서 첫 번째 값이 클래스 인덱스
                class_counts[cls_idx] += 1
    
    return total_images, class_counts

if __name__ == '__main__':
    labels_directory = '/home/oms/leesh/raw_data/yolo_final_datasets/abandonment_v3/train/labels'  # 여기를 실제 경로로 수정
    total_imgs, counts = count_yolo_labels(labels_directory)
    
    print(f"전체 이미지(레이블) 수: {total_imgs}")
    print("클래스별 인스턴스 수:")
    for cls, cnt in sorted(counts.items()):
        print(f"  클래스 {cls}: {cnt}개")
