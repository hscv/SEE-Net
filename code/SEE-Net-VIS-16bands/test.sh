CUDA_VISIBLE_DEVICES=3 nohup python -u tools/demo.py --config experiments/siamban_r50_l234/config.yaml --snapshot experiments/siamban_r50_l234/snapshot/Final-VIS-Model.pth --video_path /data/lizf/HOT/dataset/test/test_HSI/ > nohup.test.VIS.log 2>&1 &