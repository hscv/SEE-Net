close all;
clear;

plotDrawStyleAll={   struct('color',[1,0,0],'lineStyle','-'),...
    struct('color',[0,0,1],'lineStyle','-'),...
    struct('color',[0,0,0],'lineStyle','-'),...%    struct('color',[1,1,0],'lineStyle','-'),...%yellow
    struct('color',[1,0,1],'lineStyle','-'),...%pink %% delete - struct('color',[0,1,1],'lineStyle','-'),...
    struct('color',[0,1,0],'lineStyle','-'),...
    struct('color',[0.5,0.5,0.5],'lineStyle','-'),...%gray-25% %% delete -- struct('color',[136,0,21]/255,'lineStyle','-'),...%dark red
    struct('color',[255,127,39]/255,'lineStyle','-'),...%orange %% 
    struct('color',[0,162,232]/255,'lineStyle','-'),...%Turquoise
    struct('color',[163,73,164]/255,'lineStyle','-'),...%purple    %%%%%%%%%%%%%%%%%%%%
    struct('color',[1,0,0],'lineStyle','-.'),...
    struct('color',[0,1,0],'lineStyle','-.'),...
    struct('color',[0,0,1],'lineStyle','-.'),...
    struct('color',[0,0,0],'lineStyle','-.'),...%    struct('color',[1,1,0],'lineStyle',':'),...%yellow
    struct('color',[1,0,1],'lineStyle','-.'),...%pink
    struct('color',[0,1,1],'lineStyle','-.'),...
    struct('color',[0.5,0.5,0.5],'lineStyle','-.'),...%gray-25%
    struct('color',[136,0,21]/255,'lineStyle','-.'),...%dark red
    struct('color',[255,127,39]/255,'lineStyle','-.'),...%orange
    struct('color',[0,162,232]/255,'lineStyle','-.'),...%Turquoise
    struct('color',[163,73,164]/255,'lineStyle','-.'),...%purple
    struct('color',[1,0,0],'lineStyle','--'),...
    struct('color',[0,1,0],'lineStyle','--'),...
    struct('color',[0,0,1],'lineStyle','--'),...
    struct('color',[0,0,0],'lineStyle','--'),...%    struct('color',[1,1,0],'lineStyle','--'),...%yellow
    struct('color',[1,0,1],'lineStyle','--'),...%pink
    struct('color',[0,1,1],'lineStyle','--'),...
    struct('color',[0.5,0.5,0.5],'lineStyle','--'),...%gray-25%
    struct('color',[136,0,21]/255,'lineStyle','--'),...%dark red
    struct('color',[255,127,39]/255,'lineStyle','--'),...%orange
    struct('color',[0,162,232]/255,'lineStyle','--'),...%Turquoise
    struct('color',[163,73,164]/255,'lineStyle','--'),...%purple    %%%%%%%%%%%%%%%%%%%
    };
plotDrawStyle = plotDrawStyleAll;
% results of trackers
trackMatDeep = {'SEE-Net-0.6657-0.9327.mat'; 'BAE-Net-0.6062-0.8778.mat'; 'MHT-0.5860-0.8818.mat'; 'DeepHKCF-0.3033-0.5415.mat'; 'CNHT-0.1713-0.3351.mat'; 'SST-Net-0.6230-0.9161.mat'; 'MFI-0.6009-0.8925.mat'};
nameTrkAllDeep = {'SEE-Net'; 'BAE-Net'; 'MHT'; 'DeepHKCF'; 'CNHT'; 'SST-Net'; 'MFI'};
trackMat = trackMatDeep;
nameTrkAll = nameTrkAllDeep;
rankNum = size(trackMat);
fontSizeLegend = 12;

index = [1:35];
if 1  %% 0 for DP curve, 1 for AUC curve
for idxTrk=1:size(trackMat)
    load(trackMat{idxTrk});
    perf(idxTrk) = mean(mean(PASCAL_rec(index,2:end),2));
end
perf = round(perf,3);
[tmp,indexSort]=sort(perf,'descend');
AUC=[];
figure1 = figure;
tmp_i = 1;
axes1 = axes('Parent',figure1,'FontSize',14);
for idxTrk=indexSort(1:rankNum)
    load(trackMat{idxTrk});
    Our_PASCAL=mean(PASCAL_rec(index,2:end));
    tmp = sprintf('%.3f', mean(mean(PASCAL_rec(index,2:end),2)));
    tmpName{tmp_i} = [nameTrkAll{idxTrk} ' [' tmp ']'];
    h(tmp_i) = plot(Our_PASCAL,'Color',plotDrawStyle{tmp_i}.color,'lineStyle', plotDrawStyle{tmp_i}.lineStyle,'linewidth',3,'MarkerSize',7, 'Parent',axes1);
    hold on
    tmp_i=tmp_i+1;
end

legend1=legend(tmpName,'Interpreter', 'none','fontsize',fontSizeLegend, 'location','southwest');
set(gca,'fontSize',12,'ylim',[0,1],'xlim',[1,50], 'XTick',0:10:50);
set(gca,'xtick',0:10:50,'XTickLabel',{'0' '0.2' '0.4' '0.6' '0.8' '1'});
grid on;
title('Success plots of OPE', 'FontWeight','bold')
xlabel('Overlap threshold','fontSize',18);
ylabel('Success rate','fontSize',18);
saveas(gcf,'DP_AUC/AUC_HS_tracker.eps','epsc')


else
for idxTrk=1:size(trackMat)
    load(trackMat{idxTrk});
    HKCF_distance_tmp = mean(distance_rec(index,1:51));
    perf(idxTrk) = HKCF_distance_tmp(21);
end
perf = round(perf,3);
[tmp,indexSort]=sort(perf,'descend');
AUC=[];
figure1 = figure;
tmp_i = 1;
axes1 = axes('Parent',figure1,'FontSize',14);
for idxTrk=indexSort(1:rankNum)
    load(trackMat{idxTrk});
    Our_PASCAL=mean(distance_rec(index,1:51));
    tmp = sprintf('%.3f', Our_PASCAL(21));
    tmpName{tmp_i} = [nameTrkAll{idxTrk} ' [' tmp ']'];
    h(tmp_i) = plot(Our_PASCAL,'Color',plotDrawStyle{tmp_i}.color,'lineStyle', plotDrawStyle{tmp_i}.lineStyle,'linewidth',3,'MarkerSize',7, 'Parent',axes1);
    hold on
    tmp_i=tmp_i+1;
end

legend1=legend(tmpName,'Interpreter', 'none','fontsize',fontSizeLegend, 'location','southeast');
set(gca,'fontSize',12,'ylim',[0,1],'xlim',[1,50], 'XTick',0:10:50);
set(gca,'xtick',0:10:50,'XTickLabel',{'0' '10' '20' '30' '40' '50'});
grid on;
title('Precision plots of OPE', 'FontWeight','bold')
xlabel('Location error threshold','fontSize',18), ylabel('Precision','fontSize',18)
saveas(gcf,'DP_AUC/DP_HS_tracker.eps','epsc')
end