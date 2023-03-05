workpath = fullfile('G:','Data','WenLab','Worm_Forward_Backward');  % 设置工作路径 For PC-3070
%workpath=fullfile('/','home','wenlab','xrk','Worm_Forward_Backward');  %For Remote Serve
wormdatapath = fullfile('H:','WenLabData','wormdata'); % 线虫数据的主目录
addpath(genpath(fullfile(workpath,'rawdata')));  %将原始数据目录 添加到工作搜索路径
addpath(genpath(fullfile(workpath,'LibKang')));   %将函数库目录 添加到工作搜索路径
addpath(genpath(fullfile(workpath,'data')));     %将提取后的数据目录 添加到工作搜索路径
addpath(genpath(fullfile(workpath,'Parameter')));     %将参数数据目录 添加到工作搜索路径
addpath(genpath(fullfile(workpath,'Prodata')));   %将处理后的数据目录 添加到工作搜索路径