%% Background Clutters
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))

%videos={'ball';'basketball';'board';'book';'bus';'bus2';'campus';'car';'car2';'car3';'card';'coin';'coke';'drive';'excavator';'face';'face2';'forest';'forest2';'fruit';'hand';'kangaroo';'paper';'pedestrain';'player';'playground';'rubik';'student';'toy1';'toy2';'worker';'pedestrian2';'rider1';'rider2';'trucker'};
videos={'board';'bus';'card';'coin';'coke';'drive';'forest';'forest2';'fruit';'hand';'kangaroo';'paper';'toy1';'toy2';'worker'};
% the number represents the video of videos{number}, the cell of videos is 
% in the Line 9 (Program Comments), the number in below is same.
index=[3 5 11 12 13 14 18 19 20 21 22 23 29 30 31]; 
drawPlot_new(index,'Background Clutters','BC',1);

%% Deformation
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
%% attribute comparison
videos={'book';'excavator';'hand';'kangaroo';'player';'rubik'; 'pedestrian2'};
index=[4 15 21 22 25 27 32];
drawPlot_new(index,'Deformation','DEF',2);


%% Fast Motion
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
%% attribute comparison
videos={'basketball';'bus';'bus2';'coke'};
index=[2 5 6 13];
drawPlot_new(index,'Fast Motion','FM',3);



%% Illumination Variation
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
%% attribute comparison
videos={'bus2';'campus';'car3';'pedestrain';'rider1';'rider2';'student';'toy2';'pedestrian2';'trucker'};
index=[6 7 10 24 33 34 28 30 32 35];
drawPlot_new(index,'Illumination Variation','IV',4);



%% In-Plane Rotation
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
%% attribute comparison
videos={'board';'book';'car';'car2';'card';'coke';'drive';'excavator';'face';'face2';'paper';'player';'rubik'};
index=[3 4 8 9 11 13 14 15 16 17 23 25  27];
drawPlot_new(index, 'In-Plane Rotation','IPR',5);

%% Low Resolution
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'basketball';'bus';'car3';'rider1';'rider2';'worker';'pedestrian2'};
index=[2 5 10 33 34 31 32];
drawPlot_new(index,'Low Resolution','LR',6);

%% Motion Blur
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'ball';'basketball';'face';'kangaroo'};
index=[1 2 16 22];
drawPlot_new(index,'Motion Blur','MB',7);


%% Occlusion
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'ball';'basketball';'board';'bus2';'campus';'car';'car3';'card';'excavator';'face2';'forest';'forest2';'fruit';'playground';'rider1';'rider2';'toy1';'toy2';'pedestrian2';'trucker'};
index=[1 2 3 6 7 8 10 11 15 17 18 19 20 26 33 34 29 30 32 35];
drawPlot_new(index,'Occlusion','OCC',8);


%% Out-of-Plane Rotation
clear all;clc;
close all;

addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'board';'book';'car';'car2';'coke';'drive';'excavator';'face';'face2';'hand';'kangaroo';'player';'rubik';'toy2'};
index=[3 4 8 9 13 14 15 16 17 21 22 25 27 30];
drawPlot_new(index,'Out-of-Plane Rotation','OPR',9);


%% Out-of-View
clear all;clc;
close all;
addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'trucker'};
index=[35];
drawPlot_new(index,'Out-of-View','OV',10);


%% Scale Variation
clear all;clc;
close all;
addpath(genpath('../tools'));
addpath(genpath('../hyperspectralToolbox'))
addpath(genpath('../toolbox'))
videos={'ball';'board';'bus2';'campus';'car';'car2';'car3';'coke';'drive';'excavator';'face';'face2';'hand';'kangaroo';'pedestrain';'player';'playground';'rider1';'rider2';'student';'toy2';'trucker';'worker'};
index=[1 3 6 7 8 9 10 13 14 15 16 17 21 22 24 25 26 33 34 28 30 35 31];
drawPlot_new(index,'Scale Variation','SV',11);
