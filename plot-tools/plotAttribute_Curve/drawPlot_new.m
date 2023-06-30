function drawPlot(index, chanlleng_name, cn_berif, mode)
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
    trackMatDeep = {'SEE-Net-0.6657-0.9327.mat'; 'BAE-Net-0.6062-0.8778.mat'; 'MHT-0.5860-0.8818.mat'; 'CNHT-0.1713-0.3351.mat'; 'DeepHKCF-0.3033-0.5415.mat'; 'MFI-0.6009-0.8925.mat'; 'SST-Net-0.6230-0.9161.mat'; 'DROL-0.6262-0.9001.mat' };
    nameTrkAllDeep = {'SEE-Net'; 'BAE-Net'; 'MHT'; 'CNHT'; 'DeepHKCF'; 'MFI'; 'SST-Net'; 'DROL'};
    trackMat = trackMatDeep;
    nameTrkAll = nameTrkAllDeep;
    rankNum = size(trackMat);
    % scrsz = get(0,'ScreenSize');
    for idxTrk=1:size(trackMat)
        load(trackMat{idxTrk});
        arr{idxTrk}=mean(mean(PASCAL_rec(index,2:end),2));
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
        if mode==10
            Our_PASCAL=PASCAL_rec(index,2:end);
        end
        tmp = sprintf('%.3f', mean(mean(PASCAL_rec(index,2:end),2)));
        tmpName{tmp_i} = [nameTrkAll{idxTrk} ' [' tmp ']'];
        
        h(tmp_i) = plot(Our_PASCAL,'Color',plotDrawStyle{tmp_i}.color,'lineStyle', plotDrawStyle{tmp_i}.lineStyle,'linewidth',3,'MarkerSize',7, 'Parent',axes1);
        hold on
        tmp_i=tmp_i+1;
    end
    
    fontSizeLegend = 11;
    legend1=legend(tmpName,'Interpreter', 'none','fontsize',fontSizeLegend, 'location','southwest');
    set(gca,'fontSize',12,'ylim',[0,1],'xlim',[1,50], 'XTick',0:10:50);
    grid on;
    title(strcat('Success plots of OPE - ',chanlleng_name), 'FontWeight','bold');
    xlabel('Overlap threshold','fontSize',18);
    ylabel('Success rate','fontSize',18);
    saveas(gcf,strcat('AttributeRes/',cn_berif,'_AUC.eps'),'epsc')

end