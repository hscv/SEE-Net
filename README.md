# SEE-Net
Learning a Deep Ensemble Network with Band Importance for Hyperspectral Object Tracking

1. The results of all compared tracker are available in the folder "detection-res".
2. The tools for evaluating the compared trackers can be found in the folder "plot-tools".
3. The source code can be found in SEE-Net-VIS16.zip and SEE-Net-NIR25.zip, where the former represents the code run on 16-bands data and the latter represents the coder run on 25-bands data.

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
Download testing model in https://pan.baidu.com/s/1xUNW1wnyN7_Fo7Gcl1GaKQ  

Access code: 1234 
```python
python tools/demo.py --config experiments/siamban_r50_l234/config.yaml --snapshot experiments/siamban_r50_l234/snapshot/checkpoint_e30.pth --video_path test_path
```

## 5. Results
HSI-VIS (16 bands) and HSI-NIR (25 bands) can be downloaded in : 

https://pan.baidu.com/s/1-B-ng2jQEnLRyFx_IvMniQ ---- Access code : 1234 

More results can be found in the folder "detection-res".

## Contact
lizhuanfeng@njust.edu.cn
