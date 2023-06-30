CUDA_VISIBLE_DEVICES=7 nohup python -u tools/demo.py --config experiments/siamban_r50_l234/config.yaml --snapshot experiments/siamban_r50_l234/snapshot/SEE-Net-NIR-Model.pth --video_path /data/lizf/HOT/IMEC25Dataset/test/test_HSI/ > nohup.test.NIR.log 2>&1 &

