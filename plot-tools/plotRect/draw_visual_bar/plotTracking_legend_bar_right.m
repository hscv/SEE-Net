tracker{1}.name='Ours';
tracker{1}.Color=[255,0,0]/255;

tracker{2}.name='BAE-Net';
tracker{2}.Color=[255, 165, 0]/255;

tracker{3}.name='MHT';
tracker{3}.Color=[255,0,255]/255;

tracker{4}.name='GroundTruth';
tracker{4}.Color=[0, 0, 255]/255;


%% 5 控制bar的高�?
h{1}=plot(0,0,'linewidth',5,'Color',tracker{1}.Color);
lengend_name{1}=tracker{1}.name;
hold on
h{2}=plot(0,0,'linewidth',5,'Color',tracker{2}.Color);
lengend_name{2}=tracker{2}.name;
hold on
h{3}=plot(0,0,'linewidth',5,'Color',tracker{3}.Color);
lengend_name{3}=tracker{3}.name;
hold on
h{4}=plot(0,0,'linewidth',5,'Color',tracker{4}.Color);
lengend_name{4}=tracker{4}.name;
axis off;
hold on;
legend([h{1} h{2} h{3} h{4}],lengend_name,'FontSize',8,'Fontweight','bold','Orientation','horizontal');

% legend('boxoff') 删除边框信息
legend('boxoff')
saveas(gcf,'Qualitive-Legend-right.eps','epsc')
