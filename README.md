# SEE-Net
Learning a Deep Ensemble Network with Band Importance for Hyperspectral Object Tracking

1. The results of all compared tracker are available in the folder "detection-res".
2. The tools for evaluating the compared trackers can be found in the folder "plot-tools".
3. The source code can be found in the folder "code".

# Quick Start
## 1. Requirements
Please install the environment following https://github.com/hqucv/siamban.

## 2. Dataset
Download training and testing datasets in https://www.hsitracking.com/.

## 3. Train
(a) Download pretrained model in https://pan.baidu.com/s/1xUNW1wnyN7_Fo7Gcl1GaKQ   Access code: 1234 
(b) Change the path of training data in siamese/dataset/dataset.py
(c) Run:
```python
cd experiments/siamban_r50_l234
CUDA_VISIBLE_DEVICES=0,1,2
python -m torch.distributed.launch \
    --nproc_per_node=3 \
    --master_port=2333 \
    ../../tools/train.py --cfg config.yaml
```

## 4. Test
Download testing model in https://pan.baidu.com/s/1xUNW1wnyN7_Fo7Gcl1GaKQ   Access code: 1234 
```python
python tools/demo.py --config experiments/siamban_r50_l234/config.yaml --snapshot experiments/siamban_r50_l234/snapshot/checkpoint_e30.pth --video_path test_path
```

Contact: lizhuanfeng@njust.edu.cn
