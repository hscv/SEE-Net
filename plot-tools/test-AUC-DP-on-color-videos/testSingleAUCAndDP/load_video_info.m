function [seq, ground_truth] = load_video_info(video_name)

ground_truth = dlmread(['./gt_color_website/' video_name '_gt.txt']);

seq.len = size(ground_truth, 1);
seq.init_rect = ground_truth(1,:);

end

