function [distance_rec,PASCAL_rec,average_cle_rec]= computeMetric(pd_boxes,ground_truth,distance_precision_threshold,PASCAL_threshold)
PASCAL_rec=zeros(1,length(PASCAL_threshold));
average_cle_rec=zeros(1,length(PASCAL_threshold));
distance_rec=zeros(1,length(distance_precision_threshold));
for j=1:length(distance_precision_threshold)
    [distance_rec(j),PASCAL_rec(j),average_cle_rec(j)]= ...
        compute_performance_measures(pd_boxes, ground_truth,distance_precision_threshold(j),PASCAL_threshold(j));
end
end