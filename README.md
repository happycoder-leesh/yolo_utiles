<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6%2B-blue" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

# 🦾 YOLO Dataset Utilities

YOLO 포맷 데이터셋 전처리 및 시각화 스크립트 모음입니다.  
클래스 인덱스 리매핑, 데이터 통계, 샘플 시각화, 클래스별 데이터 추출, train/val 분할, Segmentation → Detection 변환 등 다양한 유틸리티를 제공합니다.

## 📖 목차
- 🌟 주요 기능  
- 📦 설치  
- ⚙️ 사용 예시  
- 🛠️ 옵션 및 설정  
- 🤝 기여하기  
- 📝 라이선스  

## 🌟 주요 기능
- 🔄 **클래스 인덱스 리매핑**  
  `yolo_format_cls_index_reset.py`  
- 📊 **이미지/인스턴스 통계 계산**  
  `yolo_format_datasets_count_images_and_instance.py`  
- 🎲 **무작위 샘플 시각화**  
  `yolo_format_datasets_random_visualize.py`  
- 🎯 **타겟 클래스 시각화**  
  `yolo_format_datasets_target_cls_visualize.py`  
- 🗂️ **클래스별 데이터 추출**  
  `yolo_format_extract_class_data.py`  
- ✂️ **Train/Val 데이터 분할**  
  `yolo_format_split_train_val.py`  
- 🔄 **YOLOv5-seg → BBox 변환**  
  `yolov5_format_seg_to_bbox.py`  

## 📦 설치

```bash
git clone https://github.com/<your_username>/<repo_name>.git
pip install -r requirements.txt
```

> **requirements.txt 예시**  
> ```
> opencv-python
> Pillow
> ```

## ⚙️ 사용 예시

### 1. 클래스 인덱스 리매핑
```bash
python yolo_format_cls_index_reset.py   --label_path /path/to/labels   --class-mapping-json "{origin_cls_idx:mapping_cls_idx, origin_cls_idx:mapping_cls_idx, ...}"
```

### 2. 데이터 통계 계산
```bash
python yolo_format_datasets_count_images_and_instance.py   --labels_path /path/to/labels
```

### 3. 무작위 샘플 시각화
```bash
python yolo_format_datasets_random_visualize.py   --image_dir /path/to/images   --label_dir /path/to/labels   --output_dir /path/to/output
```

### 4. 타겟 클래스 시각화
```bash
python yolo_format_datasets_target_cls_visualize.py   --target_classes 2,5   --input_image_dir /path/to/images   --input_label_dir /path/to/labels   --output_dir /path/to/output
```

### 5. 클래스별 데이터 추출
```bash
python yolo_format_extract_class_data.py   --image_dir /path/to/images   --label_dir /path/to/labels   --target_cls_ids 1,2   --output_image_dir /path/to/output/images   --output_label_dir /path/to/output/labels
```

### 6. Train/Val 분할
```bash
python yolo_format_split_train_val.py   --source_image_dir /path/to/images   --source_label_dir /path/to/labels   --output_base_dir /path/to/output   --train_ratio 0.8
```

### 7. Segmentation → Detection 변환
```bash
python yolov5_format_seg_to_bbox.py   --data_root /path/to/data   --dst_root /path/to/output   --splits train valid test
```

## 🛠️ 옵션 및 설정
- 각 스크립트 상단의 **Global 변수**를 직접 수정하거나, 필요 시 `argparse`를 추가해 CLI 환경에서 인자를 받을 수 있도록 확장 가능합니다.
- 출력 디렉토리, 비율, 클래스 매핑 등은 모두 설정 가능한 변수로 분리되어 있어 유연한 활용이 가능합니다။





**Happy Coding!** 🎉
