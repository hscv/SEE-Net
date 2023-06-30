# Copyright (c) SenseTime. All Rights Reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import sys
import os

import cv2
import numpy as np
from torch.utils.data import Dataset

from siamban.utils.bbox import center2corner, Center
from siamban.datasets.point_target import PointTarget
from siamban.datasets.augmentation import Augmentation
from siamban.core.config import cfg
logger = logging.getLogger("global")

# setting opencv
pyv = sys.version[0]
if pyv[0] == '3':
    cv2.ocl.setUseOpenCL(False)


class SubDataset(object):
    def __init__(self, name, root, anno, frame_range, num_use, start_idx):
        
        self.name = name
        self.root = root 
        self.anno = anno 
        self.frame_range = frame_range
        self.num_use = num_use
        self.start_idx = start_idx
        logger.info("loading " + name)
        with open(self.anno, 'r') as f:
            meta_data = json.load(f)
            meta_data = self._filter_zero(meta_data)
        self.video_frame_number = {}

        tm_video_arr = []
        for data in list(meta_data.keys()):
            tm_video_arr.append(data.split('/')[1])
        tm_video_arr = list(set(tm_video_arr))
        for video_tmp in tm_video_arr:
            ss = 0
            for data in list(meta_data.keys()):
                if data.find('/'+video_tmp+'/') != -1:
                    ss += 1
            self.video_frame_number[video_tmp] = ss
        for video in list(meta_data.keys()):
            for track in meta_data[video]:
                frames = meta_data[video][track]
                frames = list(map(int,
                              filter(lambda x: x.isdigit(), frames.keys())))
                frames.sort()
                meta_data[video][track]['frames'] = frames
                if len(frames) <= 0:
                    logger.warning("{}/{} has no frames".format(video, track))
                    del meta_data[video][track]

        for video in list(meta_data.keys()):
            if len(meta_data[video]) <= 0:
                logger.warning("{} has no tracks".format(video))
                del meta_data[video]

        self.labels = meta_data
        self.num = len(self.labels)
        self.num_use = self.num
        self.videos = list(meta_data.keys())
        logger.info("{} loaded".format(self.name))
        self.path_format = '{}.{}.{}.jpg'
        self.pick = self.shuffle()

    def _filter_zero(self, meta_data):
        meta_data_new = {}
        for video, tracks in meta_data.items():
            new_tracks = {}
            for trk, frames in tracks.items():
                new_frames = {}
                for frm, bbox in frames.items():
                    if not isinstance(bbox, dict):
                        if len(bbox) == 4:
                            x1, y1, x2, y2 = bbox
                            w, h = x2 - x1, y2 - y1
                        else:
                            w, h = bbox
                        if w <= 0 or h <= 0:
                            continue
                    new_frames[frm] = bbox
                if len(new_frames) > 0:
                    new_tracks[trk] = new_frames
            if len(new_tracks) > 0:
                meta_data_new[video] = new_tracks
        return meta_data_new


    def log(self):
        logger.info("{} start-index {} select [{}/{}] path_format {}".format(
            self.name, self.start_idx, self.num_use,
            self.num, self.path_format))

    def shuffle(self):
        lists = list(range(self.start_idx, self.start_idx + self.num))
        pick = []
        while len(pick) < self.num_use:
            np.random.shuffle(lists)
            pick += lists
        return pick[:self.num_use]

    def get_image_anno_pre(self, video, track, frame):
        frame = "{:06d}".format(frame)
        image_path = os.path.join(self.root, video,
                                  self.path_format.format(frame, track, 'x'))
        image_anno = self.labels[video][track][frame]
        return image_path, image_anno

    def get_image_anno(self, video, track, frame):
        frame = "{:06d}".format(frame)
        tMpkk = video.split('/')
        lastFileName = os.path.join(tMpkk[1], 'HSI', tMpkk[2].split('_')[-1])
        image_path = os.path.join(self.root, lastFileName+'.tif')
        image_anno = self.labels[video][track][frame]
        return image_path, image_anno

    def get_positive_pair(self, index):
        video_name = self.videos[index]
        video = self.labels[video_name]
        track = np.random.choice(list(video.keys()))
        track_info = video[track]

        frames = track_info['frames']
        template_frame = np.random.randint(0, len(frames))
        left = max(template_frame - self.frame_range, 0)
        right = min(template_frame + self.frame_range, len(frames)-1) + 1
        search_range = frames[left:right]
        template_frame = frames[template_frame]
        search_frame = np.random.choice(search_range)
        return self.get_image_anno(video_name, track, template_frame), \
                    self.get_image_anno(video_name, track, search_frame)

    def get_random_target(self, index=-1):
        if index == -1:
            index = np.random.randint(0, self.num)
        video_name = self.videos[index]
        video = self.labels[video_name]
        track = np.random.choice(list(video.keys()))
        track_info = video[track]
        frames = track_info['frames']
        frame = np.random.choice(frames)
        
        return self.get_image_anno(video_name, track, frame)

    def __len__(self):
        return self.num


class BANDataset(Dataset):
    def __init__(self,):
        super(BANDataset, self).__init__()

        desired_size = (cfg.TRAIN.SEARCH_SIZE - cfg.TRAIN.EXEMPLAR_SIZE) / \
            cfg.POINT.STRIDE + 1 + cfg.TRAIN.BASE_SIZE
        if desired_size != cfg.TRAIN.OUTPUT_SIZE:
            raise Exception('size not match!')

        # create point target
        self.point_target = PointTarget()

        # create sub dataset
        self.all_dataset = []

        start = 0
        self.num = 0
        sub_dataset = self.readAllDataset('/nas_data/lizf/HOT/IMEC25Dataset/nir_train.json', \
                                     '/nas_data/lizf/HOT/IMEC25Dataset/train/', start)
        sub_dataset.log()
        self.all_dataset.append(sub_dataset)

        start += sub_dataset.num
        self.num += sub_dataset.num_use

        self.template_aug = Augmentation(
                cfg.DATASET.TEMPLATE.SHIFT,
                cfg.DATASET.TEMPLATE.SCALE,
                cfg.DATASET.TEMPLATE.BLUR, 
                cfg.DATASET.TEMPLATE.FLIP, 
                cfg.DATASET.TEMPLATE.COLOR 
            )

        self.search_aug = Augmentation(
                cfg.DATASET.SEARCH.SHIFT, 
                cfg.DATASET.SEARCH.SCALE, 
                cfg.DATASET.SEARCH.BLUR, 
                cfg.DATASET.SEARCH.FLIP, 
                cfg.DATASET.SEARCH.COLOR 
            )
        self.num *=  cfg.TRAIN.EPOCH
        self.pick = self.shuffle()


    def readAllDataset(self, ANNO, ROOT, start):
        name = 'LASOT' ## just a name
        subdata_cfg = getattr(cfg.DATASET, name)

        sub_dataset = SubDataset(
                name,
                ROOT,
                ANNO,
                subdata_cfg.FRAME_RANGE,
                subdata_cfg.NUM_USE,
                start
            )
        return sub_dataset

    def shuffle(self):
        pick = []
        m = 0
        while m < self.num:
            p = []
            for sub_dataset in self.all_dataset:
                sub_p = sub_dataset.pick
                p += sub_p
            np.random.shuffle(p)
            pick += p
            m = len(pick)
        logger.info("shuffle done!")
        logger.info("dataset length {}".format(self.num))
        return pick[:self.num]

    def _find_dataset(self, index):
        for dataset in self.all_dataset:
            if dataset.start_idx + dataset.num > index:
                return dataset, index - dataset.start_idx

    def _get_bbox(self, image, shape):
        imh, imw = image.shape[:2]
        if len(shape) == 4:
            w, h = shape[2]-shape[0], shape[3]-shape[1]
        else:
            w, h = shape
        context_amount = 0.5
        exemplar_size = cfg.TRAIN.EXEMPLAR_SIZE
        wc_z = w + context_amount * (w+h)
        hc_z = h + context_amount * (w+h)
        s_z = np.sqrt(wc_z * hc_z)
        scale_z = exemplar_size / s_z
        w = w*scale_z
        h = h*scale_z
        cx, cy = imw//2, imh//2
        bbox = center2corner(Center(cx, cy, w, h))
        return bbox

    def __len__(self):
        return self.num

    def __getitem__(self, index):
        index = self.pick[index]
        dataset, index = self._find_dataset(index)

        gray = cfg.DATASET.GRAY and cfg.DATASET.GRAY > np.random.random()
        neg = cfg.DATASET.NEG and cfg.DATASET.NEG > np.random.random()
        if neg:
            template = dataset.get_random_target(index) 
            kk_index = -1
            video_mm = template[0].split('/')[-3]
            while True:
                kk_index = np.random.randint(0, self.num // cfg.TRAIN.EPOCH)
                search = dataset.get_random_target(kk_index)
                if search[0].find(video_mm) == -1:
                    break
        else:
            template, search = dataset.get_positive_pair(index)

        # get image and bounding box
        template_image = np.load(template[0])
        search_image = np.load(search[0])

        # template_image same with search_image
        template_box = self._get_bbox(template_image, template[1])
        search_box = self._get_bbox(search_image, search[1])

        # augmentation
        template, _ = self.template_aug(template_image,
                                        template_box,
                                        cfg.TRAIN.EXEMPLAR_SIZE,
                                        gray=gray)
        search, bbox = self.search_aug(search_image,
                                       search_box,
                                       cfg.TRAIN.SEARCH_SIZE,
                                       gray=gray)
        # get labels
        cls, delta = self.point_target(bbox, cfg.TRAIN.OUTPUT_SIZE, neg)
        template = template.transpose((2, 0, 1)).astype(np.float32)
        search = search.transpose((2, 0, 1)).astype(np.float32)
        return {
                'template': template,
                'search': search,
                'label_cls': cls,
                'label_loc': delta,
                'bbox': np.array(bbox)
                }

