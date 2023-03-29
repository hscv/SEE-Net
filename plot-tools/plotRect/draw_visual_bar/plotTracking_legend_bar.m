tracker{1}.name='Ours';
tracker{1}.Color=[255,0,0]/255;

tracker{2}.name='BAE-Net';
tracker{2}.Color=[255,165,0]/255;


tracker{3}.name='MHT';
tracker{3}.Color=[255,0,255]/255;


tracker{4}.name='MFI';
tracker{4}.Color=[236,233,79]/255;

tracker{5}.name='SST-Net';
tracker{5}.Color=[64,224,205]/255;

% 
tracker{6}.name='DROL';
tracker{6}.Color=[50,205,50]/255;

tracker{7}.name='GroundTruth';
tracker{7}.Color=[0, 0, 255]/255;
% 


plotWidth = 5;
%% 5 控制bar的高�?
h{1}=plot(0,0,'linewidth',plotWidth,'Color',tracker{1}.Color);
lengend_name{1}=tracker{1}.name;
hold on
h{2}=plot(0,0,'linewidth',plotWidth,'Color',tracker{2}.Color);
lengend_name{2}=tracker{2}.name;
hold on
h{3}=plot(0,0,'linewidth',plotWidth,'Color',tracker{3}.Color);
lengend_name{3}=tracker{3}.name;
hold on
h{4}=plot(0,0,'linewidth',plotWidth,'Color',tracker{4}.Color);
lengend_name{4}=tracker{4}.name;
hold on
h{5}=plot(0,0,'linewidth',plotWidth,'Color',tracker{5}.Color);
lengend_name{5}=tracker{5}.name;
hold on
h{6}=plot(0,0,'linewidth',plotWidth,'Color',tracker{6}.Color);
lengend_name{6}=tracker{6}.name;
hold on
h{7}=plot(0,0,'linewidth',plotWidth,'Color',tracker{7}.Color);
lengend_name{7}=tracker{7}.name;
axis off;
hold on;
legend([h{1} h{2} h{3} h{4} h{5} h{6} h{7}],lengend_name,'FontSize',6.5,'Fontweight','bold','Orientation','horizontal');
% legend([h{1} h{2} h{3} h{4}],lengend_name,'FontSize',6.5,'Fontweight','bold','Orientation','horizontal');

% legend('boxoff') 删除边框信息
legend('boxoff')
saveas(gcf,'Qualitive-Legend.eps','epsc')
