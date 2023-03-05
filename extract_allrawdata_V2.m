tic
%目的：将rawdata中一个文件夹下所有*.yaml文件提取出name,头尾位置，angle_data,curve_datafilter等原始数据
%然后将其导入到data对应文件夹下面


TypePathname={'YamlFiles','N2','Backward','Tosif_data'};
workpath = uigetdir('C:');

for filepath_num=1:length(TypePathname)
    filepath = TypePathname{filepath_num};
    pathname = fullfile(workpath,filepath); %the rawdata's path
    yamlfiles = dir(fullfile(pathname,'*.yaml'));
    if length(yamlfiles)==0
        disp(strcat(filepath,' folder has no *.yaml'))
        continue;
    end
    
    disp(strcat('Begain to process:',filepath));
    for s_yaml=1:length(yamlfiles)
        filename = yamlfiles(s_yaml).name;
        fname=fullfile(pathname,filename);   % the full pathe of the *.yaml
        namepattern = 'w\d*\w*\.yaml';
        timepattern = '\d*_\d\d\d\d_';
        shortname = regexp(filename,namepattern,'match');
        wormname = shortname{1}(1:end-5);
        
        mcd = Mcd_Frame;
        mcd = mcd.yaml2matlab(fname);    % a=mcd(x)
        
        numcurvepts = 100;
        proximity = 50;
        spline_p = 0.0005;
        flip=0;
        timefilter = 5;
        bodyfilter =10 ;
        framnum=length(mcd);
        
        wormdata.name=yamlfiles(s_yaml).name;
        wormdata.wormname=wormname;
        wormdata.wormType = filepath;
        wormdata.curve_data=zeros(framnum,numcurvepts);
        wormdata.angle_data=zeros(framnum,numcurvepts+1);
        wormdata.TimeElapsed=zeros(framnum,1);
        wormdata.Centerline=zeros(framnum,100,2);
        wormdata.StagePosition=zeros(framnum,2);
        wormdata.StageFeedbackTarget=zeros(framnum,2);
        wormdata.BoundaryA=zeros(framnum,100,2);   %A面的坐标
        wormdata.BoundaryB=zeros(framnum,100,2);   %B面的坐标
        wormdata.Framenum=zeros(framnum,1);  %存储视频的framnumber
        wormdata.Head=zeros(framnum,2);
        wormdata.Tail = zeros(framnum,2);
        wormdata.StageVelocity = zeros(framnum,2);
        
        Head_position=mcd(1).Head;
        Tail_position=mcd(1).Tail;
        
        worm_length=0;  %body length in terms of pixels
        t1=0;j1=0; j2=0;
        for i=1:framnum
            if (norm(mcd(i).Head-Head_position)> norm(mcd(i).Tail-Head_position)) %%head and tail flips
                if norm(mcd(i).Head-Tail_position)<=proximity && norm(mcd(i).Tail-Head_position)<=proximity  %%if the tip points are identified
                    flips=~flip;
                    Head_position=mcd(i).Tail;
                    Tail_position=mcd(i).Head;
                end
            else
                flips = flip;
                Head_position = mcd(i).Head;
                Tail_position = mcd(i).Tail;
            end
            
            if norm(mcd(i).Head-mcd(i).Tail)>proximity
                centerline=reshape(mcd(i).SegmentedCenterline,2,[]);
                if flips
                    centerline(1,:)=centerline(1,end:-1:1);
                    centerline(2,:)=centerline(2,end:-1:1);
                end
            end
            boundary=reshape(mcd(i).BoundaryA,2,[]);
            wormdata.BoundaryA(i,:,1)=boundary(1,:);
            wormdata.BoundaryA(i,:,2)=boundary(2,:);
            boundary=reshape(mcd(i).BoundaryB,2,[]);
            wormdata.BoundaryB(i,:,1)=boundary(1,:);
            wormdata.BoundaryB(i,:,2)=boundary(2,:);
            
            wormdata.Centerline(i,:,1)=centerline(1,:);
            wormdata.Centerline(i,:,2)=centerline(2,:);
            wormdata.TimeElapsed(i)=mcd(i).TimeElapsed;
            wormdata.StagePosition(i,:)=mcd(i).StagePosition;
            wormdata.StageFeedbackTarget(i,:)=mcd(i).StageFeedbackTarget;
            wormdata.Framenum(i)=mcd(i).FrameNumber;
            wormdata.Head(i,:)=mcd(i).Head(:);
            wormdata.Tail(i,:)=mcd(i).Tail(:);
            wormdata.StageVelocity(i,:)=mcd(i).StageVelocity(:);
            
            df = diff(centerline,1,2); %列差分计算，相邻点做差分
            t = cumsum([0, sqrt([1 1]*(df.*df))]);%求矩阵或向量的累积和，here [0,[1:100]] adds one column by the head, thus the matrix becomes [0:101]
            worm_length=worm_length+t(end);
            cv = csaps(t,centerline,spline_p);
            
            cv2 =  fnval(cv, t)';
            df2 = diff(cv2,1,1); df2p = df2';
            
            splen = cumsum([0, sqrt([1 1]*(df2p.*df2p))]);
            cv2i = interp1(splen+.00001*[0:length(splen)-1],cv2, [0:(splen(end)-1)/(numcurvepts+1):(splen(end)-1)]);
            
            df2 = diff(cv2i,1,1);
            atdf2 =  unwrap(atan2(-df2(:,2), df2(:,1)));
            wormdata.angle_data(i,:) = atdf2';
            
            curve = unwrap(diff(atdf2,1));
            wormdata.curve_data(i,:) = curve';
        end
        worm_length=worm_length/framnum;
        
        h = fspecial('average', [timefilter bodyfilter]);
        wormdata.curvedatafiltered = imfilter(wormdata.curve_data*100,  h , 'replicate');  %得到K*L
        wormdata.worm_length = worm_length;
        
        
        clearvars -except wormdata workpath pathname TypePathname filepath filename yamlfiles wormname
        savename=strrep(filename,'.yaml','.mat');
        savefolder=fullfile(workpath,'data',filepath);
        
        if exist(savefolder)==0
            disp('dir is not exist');
            mkdir(savefolder);
            disp('make dir success');
        else
            disp('dir is exist');
        end
        save(fullfile(savefolder,strcat(filepath,'_',savename)),'wormdata')
        disp(['Save file ',savename, ' success'])
        
    end
end



