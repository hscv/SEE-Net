function drawPlot(PASCAL_rec_arr, index, chanlleng_name, cn_berif, mode)
    
    load TIP_1_UBHT.mat;
    Our_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        Our_PASCAL=PASCAL_rec(index,2:end);
    end
    arr{1}=mean(mean(PASCAL_rec(index,2:end),2));
    h1=plot(Our_PASCAL,'-','Color','r','linewidth',3,'MarkerSize',7);hold on;
    legend_name{1}=['DEN [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];
    
    cc = 1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h2=plot(HKCF_PASCAL,'-','Color',[3.0/255,167.0/255,158.0/255],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{2}=['ECO [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];


    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    Our_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        Our_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h3=plot(Our_PASCAL,'-','Color',[217.0/255,165.0/255,31.0/255],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{3}=['DSiam [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];


    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h4=plot(HKCF_PASCAL,':','Color',[1.0,0,1.0],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{4}=['SiamDW [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];


    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h5=plot(HKCF_PASCAL,':','Color',[0, 1.0, 0],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{5}=['SiamFC [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];

    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h6=plot(HKCF_PASCAL,':.','Color',[0,1.0,1.0],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{6}=['SiamRPN [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];

    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h7=plot(HKCF_PASCAL,'-','Color',[205.0/255 197.0/255 186.0/255],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{7}=['SiamRPNpp [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];

    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h8=plot(HKCF_PASCAL,'-','Color',[30.0/255 144.0/255 1.0],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{8}=['UpdateNet [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];

    cc = cc+1;
    PASCAL_rec = PASCAL_rec_arr{cc};
    HKCF_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        HKCF_PASCAL=PASCAL_rec;
    end
    arr{cc+1}=mean(mean(PASCAL_rec(index,2:end),2));
    h9=plot(HKCF_PASCAL,'-.','Color',[127.0/255 10.0/255 0.0],'linewidth',3,'MarkerSize',7);hold on;
    legend_name{9}=['VITAL [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];


    
    load TIP_1_MHT.mat;
    Our_PASCAL=mean(PASCAL_rec(index,2:end));
    if mode==10
        Our_PASCAL=PASCAL_rec(index,2:end);
    end
    arr{10}=mean(mean(PASCAL_rec(index,2:end),2));
    h10=plot(Our_PASCAL,':','Color','k','linewidth',3,'MarkerSize',7);hold on;
    legend_name{10}=['MHT [',sprintf('%.3f',mean(mean(PASCAL_rec(index,2:end),2))),']'];
    
    
    a2 = cell2mat(arr(:));
    [~,ind] = sort(a2);ind
    mode
    if mode == 1
    legend([h1,h9,h7,h8,h5,h10,h3,h6,h4,h2],legend_name([1,9,7,8,5,10,3,6,4,2]),'location','southwest');%% BC
    elseif mode == 2
    legend([h7,h8,h9,h1,h6,h4,h3,h10,h5,h2],legend_name([7,8,9,1,6,4,3,10,5,2]),'location','southwest');%% DEF
    elseif mode == 3
    legend([h1, h7, h8, h6, h5, h9, h10, h3, h4, h2],legend_name([1, 7, 8, 6, 5, 9, 10, 3, 4, 2]),'location','southwest');%% FM
    elseif mode == 4
    legend([h1,h10,h8,h2,h7,h6,h3,h9,h5,h4],legend_name([1,10,8,2,7,6,3,9,5,4]),'location','southwest');%%IV
    elseif mode == 5
    legend([h7,h9,h8,h3,h1,h5,h4,h6,h10,h2],legend_name([7,9,8,3,1,5,4,6,10,2]),'location','southwest');%%IPR
    elseif mode == 6
    legend([h1,h10,h7,h6,h8,h3,h5,h2,h4,h9],legend_name([1,10,7,6,8,3,5,2,4,9]),'location','southwest');%% LR
    elseif mode == 7
    legend([h6,h7,h1,h4,h8,h2,h10,h3,h9,h5],legend_name([6,7,1,4,8,2,10,3,9,5]),'location','southwest');%% MB
    elseif mode == 8
    legend([h1,h10,h7,h9,h2,h8,h3,h6,h5,h4],legend_name([1,10,7,9,2,8,3,6,5,4]),'location','southwest');%% OCC
    elseif mode == 9
    legend([h7,h8,h9,h4,h1,h6,h3,h5,h2,h10],legend_name([7,8,9,4,1,6,3,5,2,10]),'location','southwest');%% OPR
    elseif mode == 10
    legend([h1,h2,h8,h10,h7,h9,h3,h6,h5,h4],legend_name([1,2,8,10,7,9,3,6,5,4]),'location','southwest');%% OV
    else
    legend([h1,h8,h10,h7,h6,h3,h2,h4,h9,h5],legend_name([1,8,10,7,6,3,2,4,9,5]),'location','southwest');%% BC
    end
    set(gca,'fontSize',12,'ylim',[0,1],'xlim',[1,50]);
    grid on;
    title(strcat('Success plots of OPE - ',chanlleng_name), 'FontWeight','bold')
    xlabel('Overlap threshold','fontSize',18), ylabel('Success rate','fontSize',18)
    
    saveas(gcf,strcat('AttributeRes/',cn_berif,'_AUC.eps'),'epsc')
end