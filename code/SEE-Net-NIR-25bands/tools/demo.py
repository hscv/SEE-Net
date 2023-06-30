from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import argparse

import cv2
import torch
import numpy as np
from glob import glob

from siamban.core.config import cfg
from siamban.models.model_builder import ModelBuilder
from siamban.tracker.tracker_builder import build_tracker
from siamban.utils.model_load import load_pretrain

torch.set_num_threads(1)

def set_init_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)

parser = argparse.ArgumentParser(description='tracking demo')
parser.add_argument('--config', type=str, help='config file')
parser.add_argument('--snapshot', type=str, help='model name')
parser.add_argument('--video_name', default='', type=str,
                    help='videos or image files')
parser.add_argument('--video_path', default='', type=str,
                    help='videos or image path')
parser.add_argument('--save', action='store_true',
        help='whether visualzie result')
args = parser.parse_args()


pre_foldName = 'hsiPics'
suffix_foldName = 'HSI'
imageFilter = '*.tif*'

def X2Cube(img, cellNum=4):

    B = [cellNum, cellNum]
    skip = [cellNum, cellNum]
    # Parameters
    M, N = img.shape
    col_extent = N - B[1] + 1
    row_extent = M - B[0] + 1

    # Get Starting block indices
    start_idx = np.arange(B[0])[:, None] * N + np.arange(B[1])

    # Generate Depth indeces
    didx = M * N * np.arange(1)
    start_idx = (didx[:, None] + start_idx.ravel()).reshape((-1, B[0], B[1]))

    # Get offsetted indices across the height and width of input array
    offset_idx = np.arange(row_extent)[:, None] * N + np.arange(col_extent)

    # Get all actual indices & index into input array for final output
    out = np.take(img, start_idx.ravel()[:, None] + offset_idx[::skip[0], ::skip[1]].ravel())
    out = np.transpose(out)
    img = out.reshape(M//cellNum, N//cellNum, cellNum*cellNum)
    return img

def get_gt_txt(gt_name):
    f = open(gt_name,'r')
    gt_arr = []
    gt_res = f.readlines()
    for gt in gt_res:
        kk = gt.split('\t')[:-1]
        x = list(map(float, kk))
        gt_arr.append(x)
    return gt_arr

def get_frames(video_name):
    if not video_name:
        cap = cv2.VideoCapture(0)
        for i in range(5):
            cap.read()
        while True:
            ret, frame = cap.read()
            if ret:
                yield frame
            else:
                break
    elif video_name.endswith('avi') or \
        video_name.endswith('mp4') or \
        video_name.endswith('mov'):
        cap = cv2.VideoCapture(video_name)
        while True:
            ret, frame = cap.read()
            if ret:
                yield frame
            else:
                break
    else:
        images = glob(os.path.join(video_name, imageFilter))
        images = sorted(images,
                        key=lambda x: int(x.split('/')[-1].split('.')[0]))
        for img in images:
            if imageFilter == '*.tif*':
                frame1 = cv2.imread(img, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
                frame = X2Cube(frame1, cellNum=5)
            else:
                frame = cv2.imread(img)
            yield frame


def get_frames_falseColor(video_name):
    video_name = video_name[:-3]+'HSI'
    images = glob(os.path.join(video_name, '*.jp*'))
    images = sorted(images,
                    key=lambda x: int(x.split('/')[-1].split('.')[0]))
    frameArr = []
    for img in images:
        frame = cv2.imread(img)
        frameArr.append(frame)
    return frameArr

def cal_iou(box1, box2):
    r"""

    :param box1: x1,y1,w,h
    :param box2: x1,y1,w,h
    :return: iou
    """
    x11 = box1[0]
    y11 = box1[1]
    x21 = box1[0] + box1[2] - 1
    y21 = box1[1] + box1[3] - 1
    area_1 = (x21 - x11 + 1) * (y21 - y11 + 1)

    x12 = box2[0]
    y12 = box2[1]
    x22 = box2[0] + box2[2] - 1
    y22 = box2[1] + box2[3] - 1
    area_2 = (x22 - x12 + 1) * (y22 - y12 + 1)

    x_left = max(x11, x12)
    x_right = min(x21, x22)
    y_top = max(y11, y12)
    y_down = min(y21, y22)

    inter_area = max(x_right - x_left + 1, 0) * max(y_down - y_top + 1, 0)
    iou = inter_area / (area_1 + area_2 - inter_area)
    return iou


def cal_success(iou):
    success_all = []
    overlap_thresholds = np.arange(0, 1.05, 0.05)
    for overlap_threshold in overlap_thresholds:
        success = sum(np.array(iou) > overlap_threshold) / len(iou)
        success_all.append(success)
    return np.array(success_all)

def track_once(gtArr, video_path_name):
    args.save = True
    # load config
    cfg.merge_from_file(args.config)
    set_init_seed(cfg.TRACK.SEED)
    
    cfg.CUDA = torch.cuda.is_available() and cfg.CUDA
    device = torch.device('cuda' if cfg.CUDA else 'cpu')
    model = ModelBuilder() # create model
    model = load_pretrain(model, args.snapshot).cuda().eval() # load model

    tracker = build_tracker(model) # build tracker
    video_name = video_path_name.split('/')[-1].split('.')[0]
    model_name_tmp_m = args.snapshot.split('/')[-1].split('_')[-1][:-4]
    save_det_path = 'demo/'+pre_foldName+'/'+model_name_tmp_m+'/' + video_name+'_det.txt'
    if not os.path.exists('demo/'+pre_foldName+'/'+model_name_tmp_m):
        os.mkdir('demo/'+pre_foldName+'/'+model_name_tmp_m)
    video_path_name = video_path_name + '/'+suffix_foldName

    det_arr = []
    f = open(save_det_path,'w')
    gt_arr = gtArr

    first_frame = True
    cnt = -1
    for frame in get_frames(video_path_name):
        cnt += 1
        falseColorFrame = frame[:,:,-3:].copy()
        if first_frame:
            # build video writer
            if args.save:
                if video_path_name.endswith('avi') or \
                    video_path_name.endswith('mp4') or \
                    video_path_name.endswith('mov'):
                    cap = cv2.VideoCapture(video_path_name)
                    fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
                else:
                    fps = 30
                save_video_path = 'demo/'+pre_foldName+'/'+model_name_tmp_m+'/'+video_name+'_tracking.mp4'
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                frame_size = (frame.shape[1], frame.shape[0])
                video_writer = cv2.VideoWriter(save_video_path, fourcc, fps, frame_size)
            try:
                first_gt = gt_arr[0]
                det_arr.append(first_gt)
                init_rect = np.array(first_gt)
                for tmp in first_gt:
                    f.write(str(tmp)+'\t')
                f.write('\n')
            except:
                exit()
            tracker.init(frame, init_rect)
            print (cnt,', bbox = ', init_rect, ' gt_arr[cnt] = ', init_rect)
            first_frame = False
        else:
            outputs = tracker.track(frame,gt_arr[cnt])
            bbox = list(map(int, outputs['bbox']))
            print (cnt,', bbox = ', outputs['bbox'], ' gt_arr[cnt] = ', gt_arr[cnt])
            cv2.rectangle(falseColorFrame, (bbox[0], bbox[1]),
                          (bbox[0]+bbox[2], bbox[1]+bbox[3]),
                          (0, 255, 0), 2)
            det_arr.append(outputs['bbox'])
            for tmp in outputs['bbox']:
                f.write(str(tmp)+'\t')
            f.write('\n')

        if args.save:
            video_writer.write(falseColorFrame)
    f.close()
    if args.save:
        video_writer.release()
    return det_arr



def overlap_ratio(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,w,h] or
            2d array of N x [x,y,w,h]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]

    left = np.maximum(rect1[:, 0], rect2[:, 0])
    right = np.minimum(rect1[:, 0] + rect1[:, 2], rect2[:, 0] + rect2[:, 2])
    top = np.maximum(rect1[:, 1], rect2[:, 1])
    bottom = np.minimum(rect1[:, 1] + rect1[:, 3], rect2[:, 1] + rect2[:, 3])

    intersect = np.maximum(0, right - left) * np.maximum(0, bottom - top)
    union = rect1[:, 2] * rect1[:, 3] + rect2[:, 2] * rect2[:, 3] - intersect
    iou = np.clip(intersect / union, 0, 1)
    return iou

def main():
    root = args.video_path
    video_dir_arr = []
    gtArr = []
    detArr = []
    dir_arr = os.listdir(root)
    dir_arr.sort()
    for d in dir_arr:
        path = os.path.join(root, d)
        if os.path.isdir(path):
            video_dir_arr.append(path)

    for video_name in video_dir_arr:
        gt_path = video_name + '/groundtruth_rect.txt'
        gt = get_gt_txt(gt_path)
        gtArr.append(gt)

    for i in range(len(video_dir_arr)):  
        print (video_dir_arr[i])
        detRes = track_once(gtArr[i], video_dir_arr[i])
        overlap_arr = []
        for cnt in range(len(detRes)):
            overlap_arr.append(overlap_ratio(np.array(gtArr[i][cnt]), np.array(detRes[cnt]))[0])
        detArr.append(detRes)
        print ('video_dir_arr = ',video_dir_arr[i],' , overlap_arr = ',np.array(overlap_arr).mean())

if __name__ == '__main__':
    main()
