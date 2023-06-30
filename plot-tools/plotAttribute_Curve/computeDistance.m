function distances=computeDistance(positions, ground_truth)
distances = sqrt((positions(:,1) - ground_truth(:,1)).^2 + ...
    (positions(:,2) - ground_truth(:,2)).^2);
distances(isnan(distances)) = [];

end