# SEE-Net
Learning a Deep Ensemble Network with Band Importance for Hyperspectral Object Tracking

1. The tools for evaluating the compared trackers can be found in the folder "plot-tools".
2. The source code can be found in the "code" folder for processing 16-bands data and 25-bands hyperspectral images.

## 1. Dataset
Download training and testing datasets in https://www.hsitracking.com/.
```python
1. The format of training dataset:
    rootDir |-
               videoName1
                   |- HSI
                       |- 0001.png
                       |- 0002.png
                       ...
                       |- XXXX.png
                       |- groundturth_rect.txt
               videoName2
                   |- HSI
                       |- 0001.png
                       |- 0002.png
                       ...
                       |- XXXX.png
                       |- groundturth_rect.txt
               ...
               videoNameN
                   |- HSI
                       |- 0001.png
                       |- 0002.png
                       ...
                       |- XXXX.png
                       |- groundturth_rect.txt
```
```python
2. The format of testing dataset:
    rootDir |-
               test_HSI
                   |- videoName1
                       |- groundturth_rect.txt
                       |- HSI
                            |- 0001.png
                            |- 0002.png
                            |- ...
                            |- XXXX.png
                   |- videoName2
                       |- groundturth_rect.txt
                       |- HSI
                            |- 0001.png
                            |- 0002.png
                            |- ...
                            |- XXXX.png
                   ...
                   |- videoNameM
                       |- groundturth_rect.txt
                       |- HSI
                            |- 0001.png
                            |- 0002.png
                            |- ...
                            |- XXXX.png
```

## 2. Results
More results can be found in:
```python
https://pan.baidu.com/s/1BcePsITWMrP59nUcU_eJcg 
Access code: 1234
```

## Citation
If these codes are helpful for you, please cite this paper:
```python
@ARTICLE{10128966,
  author={Li, Zhuanfeng and Xiong, Fengchao and Zhou, Jun and Lu, Jianfeng and Qian, Yuntao},
  journal={IEEE Transactions on Image Processing}, 
  title={Learning a Deep Ensemble Network With Band Importance for Hyperspectral Object Tracking}, 
  year={2023},
  volume={32},
  number={},
  pages={2901-2914},
  doi={10.1109/TIP.2023.3263109}}
```

## Contact
lizhuanfeng@njust.edu.cn
