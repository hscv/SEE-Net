function [seq, ground_truth] = load_video_info(video_name)

% ground_truth = dlmread(['F:/desktopMove/�о����γ�/˶��/TIP-2019-MajorV9/Ŀ����ٴ���/�㷨���_whisper/gt_rgb/' video_name '_gt.txt']);%
ground_truth = dlmread(['../../gt_falsecolor/' video_name '_gt.txt']);

seq.len = size(ground_truth, 1);
seq.init_rect = ground_truth(1,:);

end
