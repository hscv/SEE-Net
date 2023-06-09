clear all;clc;
close all;
trackerName = 'SEE-Net'; % tracker name
root_path= ['../../../detection-res/HOT-tracker-results/' trackerName]; % src path
base_path=root_path;
addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))

videos={'ball';'basketball';'board';'book';'bus';'bus2';'campus';'car';'car2';'car3';'card';'coin';'coke';'drive';'excavator';'face';'face2';'forest';'forest2';'fruit';'hand';'kangaroo';'paper';'pedestrain';'player';'playground';'rubik';'student';'toy1';'toy2';'worker';'pedestrian2';'rider1';'rider2';'trucker'};
index=[1:35];


distance_precision_threshold=0:50;
PASCAL_threshold=0:0.02:1;

saveOTB = 0;
cle = 0;
dp = 0;
OP = 0;
for i=1:35
    videos{index(i)};
    [seq, ground_truth] = load_video_info(videos{index(i)});
    res = dlmread(strcat(base_path,'/',videos{index(i)},'.txt')); 
    [distance_rec(i,:),PASCAL_rec(i,:),average_cle_rec(i,:)]= computeMetric(res,ground_truth,distance_precision_threshold,PASCAL_threshold);
    
end

% AUC, DP
res = [mean(mean(PASCAL_rec(index,2:51))) ,mean(distance_rec(index,21))]

ss = sprintf('%.4f-%.4f.mat', res(1), res(2));
savename = strcat(trackerName, '-', ss);
save(savename, 'PASCAL_rec', 'average_cle_rec', 'distance_rec');

