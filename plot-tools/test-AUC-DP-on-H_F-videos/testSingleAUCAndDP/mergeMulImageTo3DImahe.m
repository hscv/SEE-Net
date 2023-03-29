clear;clc
%% 创建文件
% mkdir('.\test');
% cd .\test
% A = imread( 'ngc6543a.jpg' ); % 自带的图片
% for i = 1:100
%     imwrite(A,[num2str(i),'.jpg'])
% end
% cd ..
%% 读取文件到一个M*N*K的矩阵
cd F:\desktopMove\研究生课程\硕博\TIP-2019-MajorV9\目标跟踪代码\算法结果_whisper\高光谱分组图\results\car3_0001
files = dir('*.jpg');
I = length(files);
G = zeros(512,256,I*3); % 带下来自你读取的图片，因为图片是3通道的，所以乘以3?
for i=1:I
    i
    G(:,:,3*(i-1)+1:3*i)=imread(files(i).name);
end