clear;clc
%% �����ļ�
% mkdir('.\test');
% cd .\test
% A = imread( 'ngc6543a.jpg' ); % �Դ���ͼƬ
% for i = 1:100
%     imwrite(A,[num2str(i),'.jpg'])
% end
% cd ..
%% ��ȡ�ļ���һ��M*N*K�ľ���
cd F:\desktopMove\�о����γ�\˶��\TIP-2019-MajorV9\Ŀ����ٴ���\�㷨���_whisper\�߹��׷���ͼ\results\car3_0001
files = dir('*.jpg');
I = length(files);
G = zeros(512,256,I*3); % �����������ȡ��ͼƬ����ΪͼƬ��3ͨ���ģ����Գ���3?
for i=1:I
    i
    G(:,:,3*(i-1)+1:3*i)=imread(files(i).name);
end