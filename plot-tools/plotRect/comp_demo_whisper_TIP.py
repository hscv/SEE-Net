import glob
import os
import pandas as pd
import numpy as np
import cv2
import sys
from PIL import Image

'''
    rootPath: E:/whisper_data/test/ -- 
                                        | ball
                                            | HSI-FalseColor
                                                | 0001.jpg
                                                | 0002.jpg
                                                ...
                                                | 0625.jpg
                                                | groundtruth_rect.txt
                                        | basketball
                                        ...
                                        | worker
'''
rootPath = 'E:/whisper_data/test/'
video_dir_arr = os.listdir(rootPath)
video_dir_arr.sort()
dec_path = './detection_res/'
savePath = './visResults'
def readTXTFile(filename,frameLen):
    bboxes = pd.read_csv(filename, sep='\t|,| ',
            header=None, names=['xmin', 'ymin', 'width', 'height'],
            engine='python')
    arr = [bboxes.iloc[i].values for i in range(frameLen)]
    for idx in  range(frameLen):
        arr[idx] = [arr[idx][0], arr[idx][1],arr[idx][0]+arr[idx][2], arr[idx][1]+arr[idx][3]]
    return arr


def getALLDectRes(pathName,frameLen):
    dec_root_path = dec_path
    detArr = []
    MFIName = dec_root_path + 'MFI/' + pathName + '.txt'
    MHTName = dec_root_path + 'MHT/' + pathName + '.txt'
    SEENet_Name = dec_root_path + 'SEE-Net/' + pathName + '.txt'
    DROL_Name = dec_root_path + 'DROL/' + pathName + '.txt'
    BAENetName = dec_root_path + 'BAE-Net/' + pathName + '.txt'
    SSTNetName = dec_root_path + 'SST-Net/' + pathName + '.txt'
    GT_Name = dec_root_path + 'GT/' + pathName + '_gt.txt'
    detArr.append(readTXTFile(MFIName,frameLen))
    detArr.append(readTXTFile(MHTName,frameLen))
    detArr.append(readTXTFile(DROL_Name,frameLen))
    detArr.append(readTXTFile(BAENetName,frameLen))
    detArr.append(readTXTFile(SSTNetName,frameLen))
    detArr.append(readTXTFile(GT_Name,frameLen))
    detArr.append(readTXTFile(SEENet_Name,frameLen))
    return detArr



def main(video_dir, idxArr=None):
    print (os.path.join(video_dir, 'HSI-FalseColor', '*.jpg'))
    filenames = sorted(glob.glob(os.path.join(video_dir, 'HSI-FalseColor', '*.jpg')),
           key=lambda x: int(os.path.basename(x).split('.')[0]))
    frames = [np.array(Image.open(filename)) for filename in filenames]

    title = video_dir.split('/')[-1]
    if not os.path.exists(os.path.join(savePath,title)):
        os.makedirs(os.path.join(savePath,title)) 

    height, width = frames[0].shape[:2]
    frameLen = len(frames)
    savename = os.path.join(savePath,title)
    
    bboxRes = getALLDectRes(title,frameLen)
    line_width = 2

    for idx, frame in enumerate(frames):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ori_height, ori_width = frame.shape[:2]
        frame=cv2.resize(frame, dsize=(190*2,105*2), interpolation=cv2.INTER_NEAREST)
        width_ratio = ori_width * 1.0 / 380
        height_ratio = ori_height * 1.0 / 210
        # # (B,G,R)
        if idx == 0:
            color = [(79,233,236), (255,0,255), (50,205,50), 
                 (0,165,255), (205 ,224,64), (0,0,255), (255,0,0)]
            for i in range(len(bboxRes)):
                # MFIName, MHTName, DROL_Name, BAENetName, SSTNetName, GT_Name, SEENet_Name
                TrackName = bboxRes[i][idx]
                frame = cv2.rectangle(frame,
                                      (int(TrackName[0] / width_ratio), int(TrackName[1] / height_ratio)),
                                      (int(TrackName[2] / width_ratio), int(TrackName[3] / height_ratio)),
                                      color[i],
                                      line_width)
        else:
            color = [(79,233,236), (255,0,255), (50,205,50), 
                 (0,165,255), (205 ,224,64), (255,0,0), (0,0,255)]
            for i in range(len(bboxRes)):
                # MFIName, MHTName, DROL_Name, BAENetName, SSTNetName, GT_Name, SEENet_Name
                TrackName = bboxRes[i][idx]
                frame = cv2.rectangle(frame,
                                      (int(TrackName[0] / width_ratio), int(TrackName[1] / height_ratio)),
                                      (int(TrackName[2] / width_ratio), int(TrackName[3] / height_ratio)),
                                      color[i],
                                      line_width)
        label = '#%04d' % (idx+1)
        frame = cv2.putText(frame, label, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
        print (os.path.join(savename,label+'.jpg'))
        cv2.imwrite(os.path.join(savename,label+'.jpg'),frame)


if __name__ == "__main__":
    video_dir_arr = [os.path.join(rootPath,video_dir) for video_dir in video_dir_arr]
    cnt = 0
    for video_dir in video_dir_arr[:]:
        print ('video_dir = ',video_dir)
        main(video_dir, None) 
        cnt += 1