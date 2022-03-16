from unittest import result
import numpy as np

def OpenYaml(yaml_path:str):
    Yaml_file = []
    with open(yaml_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n') # 删除末尾的回车
            line = line.strip() # 删除前面的空格
            Yaml_file.append(line)
    return(Yaml_file)

def check_tdata(t):
    # 检查输入进caps函数的数据是否单增
    n = t.size
    for i in range(0,n-1):
        if t[i+1]>t[i]:
            continue
        else:
            print(i)
            # break


def GetPlatform():
    # 获取操作系统种类
    import platform
    sysl = platform.system()
    if sysl == "Windows":
        print("OS is Windows")
        return("Windows")
    elif sysl == "Linux":
        print("Os is Linux")
        return("Linux")
    else:
        pass

def GetWormName(yaml_path):
    # 文件路径提取线虫名字
    sysl = GetPlatform()
    if sysl == "Windows":
        wormname = yaml_path.split('\\')[-1]
        wormname = wormname.split(".")[0]
    elif sysl == "Linux":
        wormname = yaml_path.split('/')[-1]
        wormname = wormname.split(".")[0]
    return(wormname)

def Get_Frames_line(lines):
    # 获取'Frames: ' 行数
    import re
    for i in range(30):
        if re.match('Frames',lines[i]):
            break
    return(i)

def Get_First_Frames(lines):
    linenumber = Get_Frames_line(lines)+2
    FramsNumber = lines[linenumber].split(':')[-1]
    return(int(FramsNumber))

def Get_End_Frames(lines):
    # 获取最后一个Frames的开始一行
    import re
    for i in range(1,100):
        if re.match('FrameNumber',lines[-i]):
            break
    linenumber = lines[-i].split(':')[-1]
    return(int(linenumber))

def Get_One_Frame(lines,line_start):
    # 获得一帧的所有数据进入一个list
    # lines是读取的yaml文件,是一个list
    # line_start是这一帧开始的行
    OneFrameList = []
    for i in range(line_start,line_start+98):
        OneFrameList.append(lines[i])
    return(OneFrameList)

def Get_Any_Frame(lines,number):
    # 获取任意指定帧的数据
    # 从第1帧开始数
    begin_num = Get_First_Frames(lines)
    end_num = Get_End_Frames(lines)
    All_Frames_num = end_num-begin_num+1  # 总的帧数
    if number < 1 or number>All_Frames_num:
        print("please input:[",1,",",All_Frames_num,"]")
        return(0)
    else:
        frames_line_num = Get_Frames_line(lines)+2+(number-1)*99
        return(Get_One_Frame(lines,frames_line_num))

def Get_ExperimentTime(lines:list):
    # 获取'ExperimentTime: '
    import re
    for i in range(20):
        if re.match('ExperimentTime',lines[i]):
            break
    str0 = lines[i].split('ExperimentTime')
    str0 = str0[1].strip(':') # 去除冒号
    str0 = str0.replace('"',"") # 去除引号 ""
    str0 = str0.replace('\\n',"") # 删除末尾的回车
    ExperimentTime = str0
    return(ExperimentTime)

def Get_DefaultGrid(lines:list):
    import numpy as np
    linenumber = Get_Frames_line(lines)-2
    data = np.zeros((1,2))
    data[0,0] = int(lines[linenumber].split(':')[-1])
    data[0,1] = int(lines[linenumber+1].split(':')[-1])
    return(data)

def ConvertData(lists:list,begin_data:int,end_data:int):
    import numpy as np

    # 将begin_data~end_data 连起来变为 2*100的数组
    data0 = []
    for i in range(begin_data,end_data+1):
        data0.append(lists[i])
    data0 = ''.join(data0)
    data = data0[8:-2] # 去除前面的和后面的字符
    data = list(map(int,data.split(',')))  # 将list中的字符串转为int
    data = np.array(data)
    data0 = np.zeros((2,100))
    data0[0,:] = data[0:200:2]  # x隔一个取一个值
    data0[1,:] = data[1:200:2]  # y隔一个取一个值
    return(data0)

def Avaryge1D_for_caps(caps_t):
    # 1为numpy数组x1<x2<...<xN
    # 否则用两边的平均值代替中间，返回改变后的结果
    n = caps_t.size
    if caps_t[1] == caps_t[0]:
        caps_t[1] = (caps_t[0]+caps_t[2])/2
    elif caps_t[n-1] == caps_t[n-2]:
        caps_t[n-2] = (caps_t[n-3]+caps_t[n-1])/2
    for i in range(1,n-2):
        if caps_t[i]<caps_t[i+1]:
            continue
        else:
            caps_t[i] = (caps_t[i-1]+caps_t[i+1])/2
    return(caps_t)

def Get_Angle_Curve(centerline):
    # 输入Centerline 2*100维
    # 输出
    # worm_length: 单帧的线虫长度
    # angle：ndarray(101,)单帧的角度
    # curve: ndarray(100,) 曲率
    # curvedatafiltered: ndarray(100,) 归一化后的曲率
    
    
    import numpy as np
    from csaps import csaps
    from scipy import interpolate
    import scipy.ndimage
    
    numcurvepts = 100
    proximity = 50
    spline_p = 0.0005
    flip=0
    timefilter = 5
    bodyfilter =10

    df = np.diff(centerline)
    df1 = df*df
    dfs = np.sqrt(np.dot([1,1],df1))
    dft = dfs.reshape(1,len(dfs))
    t0 = np.insert(dft,0,0.000001)  # 在最前面插入 0.000001 ,防止t前面的有多个0
    t = np.cumsum(t0)
    t = Avaryge1D_for_caps(t)  # 使得x1<x2<...<xN,否则用两边的平均值代替中间
    worm_length = t[-1]  #线虫长度

    cv0 = csaps(t,centerline,smooth = spline_p)
    cv2 = cv0(t)
    df2 = np.diff(cv2)

    df2s = np.sqrt(np.dot([1,1],df2*df2))
    dft = df2s.reshape(1,len(df2s))
    splen = np.cumsum(np.insert(dft,0,0)).reshape(1,100)
    # cv2 = np.interp(splen+0.00001*np.linspace(0,splen.size-1,splen.size,endpoint=True,dtype=float),cv2.transpose().reshape(100,2),(np.linspace(0,splen[0,-1]-1,102)).reshape(1,102))
    cv2i0 = splen+0.00001*np.linspace(0,splen.size-1,splen.size,endpoint=True,dtype=float)
    cv2i1 = cv2
    cv2i2 = (np.linspace(0,splen[0,-1]-1,102)).reshape(1,102)
    cv2i = interpolate.interp1d(cv2i0.reshape(100,),cv2i1,bounds_error=False)
    # df*df
    # t = cumsum([0,np.sqrt(np.array([1,1])*(df*df))])
    newcv = np.array([cv2i(cv2i2)[0,0,:],cv2i(cv2i2)[1,0,:]]).reshape(2,102)

    dfcv2= np.diff(newcv)
    atdf2 = np.arctan2(-dfcv2[1,:],dfcv2[0,:])
    angle = np.unwrap(atdf2)
    curve = (np.unwrap(np.diff(angle))).reshape(1,100)
    kernel = np.ones((timefilter,bodyfilter), np.float32)/(timefilter*bodyfilter)
    curvedatafiltered = (scipy.ndimage.correlate(curve*100, kernel, mode='nearest')).flatten()
    curvedatafiltered = -curvedatafiltered[::-1]
    return(worm_length,angle.transpose(),curve.flatten(),curvedatafiltered)

class Multi_task(object):
    # 存储传入对线程函数的参数
    def __init__(self,tasknum:int,centerlines):
        self.tasknum = tasknum
        self.multicenterlines = centerlines

class MultiData_curvedatafiltered(object):
    def __init__(self,num:int):
        import numpy as np
        # num是处理数量
        self.taskid = 0
        self.worm_length = 0
        self.angle_data = np.zeros((num,101))
        self.curve_data = np.zeros((num,100))
        self.curvedatafiltered = np.zeros((num,100))
        

def Get_Multi_curvedatafiltered(centerlines):
    import numpy as np
    # 输入时M*100维向量,代表M帧的数据
    # 输出是一个class,包含worm_length，angle_data，curve_data，curvedatafiltered
    m = len(centerlines.multicenterlines)
    # print(m)
    result = MultiData_curvedatafiltered(m)
    result.taskid = centerlines.tasknum #记录是第几个进程计算的
    for i in range(m):
        centerline = centerlines.multicenterlines[i,:,:]
        worm_length,result.angle_data[i,:],result.curve_data[i,:],result.curvedatafiltered[i,:] = Get_Angle_Curve(centerline)
        result.worm_length = result.worm_length+worm_length
    return(result)
    

def Just_Get_Raw(yaml_path):
    import math
    ListFile = OpenYaml(yaml_path)
    begin_num1 = Get_First_Frames(ListFile)
    end_num = Get_End_Frames(ListFile)
    All_Frames_num = end_num-begin_num1+1  # 总的帧数
    wormname = GetWormName(yaml_path)
    YamlFiles = YamlFrames(wormname,All_Frames_num)
    YamlFiles.ExperimentTime = Get_ExperimentTime(ListFile)
    print(YamlFiles.ExperimentTime)    

    framesline =  Get_Frames_line(ListFile)  # Frames的行数
    real_frames = math.ceil((len(ListFile)-(framesline+1))/99)
    print("real frames:",real_frames)

    YamlFiles.DefaultGridSizeForNonProtocolIllum = Get_DefaultGrid(ListFile)
    for i in range(0,int(real_frames)):
        framelist = Get_Any_Frame(ListFile,i+1) # 提取的一帧的内容
        frame = Extract_OneFrame(framelist)
        YamlFiles.FrameNumber[i,:] = frame.FrameNumber #internal frame number, not nth recorded frame
        YamlFiles.TimeElapsed[i,:] = frame.TimeElapsed #time since start of experiment (in s) = sElapsed+ 0.001*msRemElapsed
        YamlFiles.BoundaryA[i,0,:] = frame.BoundaryA[0,:] # N*2*100 x,y BoundaryA position in pixels on camera
        YamlFiles.BoundaryA[i,1,:] = frame.BoundaryA[1,:]
    
        YamlFiles.BoundaryB[i,0,:] = frame.BoundaryB[0,:] # N*2*100 x,y BoundaryB position in pixels on camera
        YamlFiles.BoundaryB[i,1,:] = frame.BoundaryB[1,:]
    
        YamlFiles.Centerline[i,0,:] = frame.Centerline[0,:]  # N*2*100 x,y centerline position in pixels on camera
        YamlFiles.Centerline[i,1,:] = frame.Centerline[1,:]
    
        YamlFiles.Head[i,:] = frame.Head[:]  #position in pixels on camera
        YamlFiles.Tail[i,:] = frame.Tail[:]  #position in pixels on camera
        YamlFiles.DLPisOn[i] = frame.DLPisOn #bool whether DLP is active
    
        YamlFiles.FloodLightIsOn[i] = frame.FloodLightIsOn #flood light overrides all other patterns and hits entire fov
        YamlFiles.IllumInvert[i] = frame.IllumInvert #whether pattern is inverted (invert has precedence over floodlight)
        YamlFiles.IllumFlipLR[i] = frame.IllumFlipLR #flips output left/right with respect to worm's body
        YamlFiles.IllumRectOrigin[i,:] = frame.IllumRectOrigin[:] #center of the freehand rectangular illumination in wormspace
        YamlFiles.IllumRectRadius[i,:] = frame.IllumRectRadius[:] #xy value describing dimension of rectangle
        YamlFiles.StageVelocity[i,:] = frame.StageVelocity[:] #velocity sent to stage in stage units/second
        YamlFiles.StagePosition[i,:] = frame.StagePosition[:]
        YamlFiles.StageFeedbackTarget[i,:] = frame.StageFeedbackTarget[:]
        YamlFiles.FirstLaser[i] = frame.FirstLaser
        YamlFiles.SecondLaser[i] = frame.SecondLaser
        YamlFiles.ProtocolIsOn[i] = frame.ProtocolIsOn
        YamlFiles.ProtocolStep[i] =frame.ProtocolStep
    return(YamlFiles)



def Serial_Extraction_Data1(yaml_path):
    ListFile = OpenYaml(yaml_path)
    begin_num1 = Get_First_Frames(ListFile)
    end_num = Get_End_Frames(ListFile)
    All_Frames_num = end_num-begin_num1+1  # 总的帧数
    wormname = GetWormName(yaml_path)
    
    YamlFiles = YamlFrames(wormname,All_Frames_num)
    YamlFiles.ExperimentTime = Get_ExperimentTime(ListFile)
    print(YamlFiles.ExperimentTime)
    
    YamlFiles.DefaultGridSizeForNonProtocolIllum = Get_DefaultGrid(ListFile)
    for i in range(0,All_Frames_num):
        framelist = Get_Any_Frame(ListFile,i+1) # 提取的一帧的内容
        frame = Extract_OneFrame(framelist)
        YamlFiles.FrameNumber[i,:] = frame.FrameNumber #internal frame number, not nth recorded frame
        YamlFiles.TimeElapsed[i,:] = frame.TimeElapsed #time since start of experiment (in s) = sElapsed+ 0.001*msRemElapsed
        YamlFiles.BoundaryA[i,0,:] = frame.BoundaryA[0,:] # N*2*100 x,y BoundaryA position in pixels on camera
        YamlFiles.BoundaryA[i,1,:] = frame.BoundaryA[1,:]
    
        YamlFiles.BoundaryB[i,0,:] = frame.BoundaryB[0,:] # N*2*100 x,y BoundaryB position in pixels on camera
        YamlFiles.BoundaryB[i,1,:] = frame.BoundaryB[1,:]
    
        YamlFiles.Centerline[i,0,:] = frame.Centerline[0,:]  # N*2*100 x,y centerline position in pixels on camera
        YamlFiles.Centerline[i,1,:] = frame.Centerline[1,:]
    
        YamlFiles.Head[i,:] = frame.Head[:]  #position in pixels on camera
        YamlFiles.Tail[i,:] = frame.Tail[:]  #position in pixels on camera
        YamlFiles.DLPisOn[i] = frame.DLPisOn #bool whether DLP is active
    
        YamlFiles.FloodLightIsOn[i] = frame.FloodLightIsOn #flood light overrides all other patterns and hits entire fov
        YamlFiles.IllumInvert[i] = frame.IllumInvert #whether pattern is inverted (invert has precedence over floodlight)
        YamlFiles.IllumFlipLR[i] = frame.IllumFlipLR #flips output left/right with respect to worm's body
        YamlFiles.IllumRectOrigin[i,:] = frame.IllumRectOrigin[:] #center of the freehand rectangular illumination in wormspace
        YamlFiles.IllumRectRadius[i,:] = frame.IllumRectRadius[:] #xy value describing dimension of rectangle
        YamlFiles.StageVelocity[i,:] = frame.StageVelocity[:] #velocity sent to stage in stage units/second
        YamlFiles.StagePosition[i,:] = frame.StagePosition[:]
        YamlFiles.StageFeedbackTarget[i,:] = frame.StageFeedbackTarget[:]
        YamlFiles.FirstLaser[i] = frame.FirstLaser
        YamlFiles.SecondLaser[i] = frame.SecondLaser
        YamlFiles.ProtocolIsOn[i] = frame.ProtocolIsOn
        YamlFiles.ProtocolStep[i] =frame.ProtocolStep
    
        Centerline = YamlFiles.Centerline[i,:,:]
        # print(i)
        worm_length,angle_data,curve_data,curvedatafiltered = Get_Angle_Curve(Centerline)
        YamlFiles.worm_length = YamlFiles.worm_length+worm_length
        YamlFiles.angle_data[i,:] = angle_data
        YamlFiles.curve_data[i,:] = curve_data
        YamlFiles.curvedatafiltered[i,:] = -curvedatafiltered[::-1]  #将数组反转
    # YamlFiles.LaserPower.append(frame.LaserPower)
    YamlFiles.worm_length = YamlFiles.worm_length/All_Frames_num
    return(YamlFiles)

    


class Extract_OneFrame(object):
    # 提取一帧的 类
    def __init__(self,OneFrameList:list):
        import numpy as np
        self.FrameNumber = int(OneFrameList[0].split(':')[-1])
        self.TimeElapsed = int(OneFrameList[1].split(':')[-1])+0.001*float(OneFrameList[2].split(':')[-1])  # 时间
        self.Head = np.array([int(OneFrameList[4].split(':')[-1]),int(OneFrameList[5].split(':')[-1])])
        self.Tail = np.array([int(OneFrameList[7].split(':')[-1]),int(OneFrameList[8].split(':')[-1])])

        self.BoundaryA = ConvertData(OneFrameList,13,29)

        self.BoundaryB = ConvertData(OneFrameList,34,50)

        self.Centerline = ConvertData(OneFrameList,55,71)

        self.DLPisOn =  int(OneFrameList[72].split(':')[-1])
        self.FloodLightIsOn = int(OneFrameList[73].split(':')[-1])
        self.IllumInvert = int(OneFrameList[74].split(':')[-1])
        self.IllumFlipLR = int(OneFrameList[75].split(':')[-1])
        self.IllumRectOrigin = np.array([int(OneFrameList[77].split(':')[-1]),int(OneFrameList[78].split(':')[-1])])
        self.IllumRectRadius = np.array([int(OneFrameList[80].split(':')[-1]),int(OneFrameList[81].split(':')[-1])])
        self.StageVelocity = np.array([int(OneFrameList[83].split(':')[-1]),int(OneFrameList[84].split(':')[-1])])
        self.StagePosition = np.array([int(OneFrameList[86].split(':')[-1]),int(OneFrameList[87].split(':')[-1])])
        self.StageFeedbackTarget = np.array([int(OneFrameList[91].split(':')[-1]),int(OneFrameList[92].split(':')[-1])])
        self.FirstLaser = int(OneFrameList[94].split(':')[-1])
        self.SecondLaser = int(OneFrameList[95].split(':')[-1])
        self.ProtocolIsOn = int(OneFrameList[96].split(':')[-1])
        self.ProtocolStep = int(OneFrameList[97].split(':')[-1])
        # self.curve_data # curve_data
        # self.angle_data   # angle_data
        # self.curvedatafiltered  curvedatafiltered
        
        # self.LaserPower = OneFrameList[93].split(':')[-1]
        # self.GreenLaser = 
        # self.BlueLaser =
        # self.HeadCurv = 
        # self.HeadCurvDeriv =

class YamlFrames(object):
    def __init__(self,name: str, framessize: int):
        import numpy as np
        
        self.worm_length = 0
        self.name = name
        self.ExperimentTime = 'Sun May 16 20:51:33 2021'
        self.DefaultGridSizeForNonProtocolIllum = np.zeros((1,2)) # DefaultGridSizeForNonProtocolIllum
        self.FrameNumber = np.zeros((framessize,1))  #internal frame number, not nth recorded frame
        self.TimeElapsed = np.zeros((framessize,1)) #time since start of experiment (in s) = sElapsed+ 0.001*msRemElapsed
        self.BoundaryA = np.zeros((framessize,2,100)) # N*2*100 x,y BoundaryA position in pixels on camera
        self.BoundaryB = np.zeros((framessize,2,100)) # N*2*100 x,y BoundaryB position in pixels on camera
        self.Centerline = np.zeros((framessize,2,100))  # N*2*100 x,y centerline position in pixels on camera
        self.Head = np.zeros((framessize,2)) #position in pixels on camera
        self.Tail = np.zeros((framessize,2)) #position in pixels on camera
        self.DLPisOn = np.zeros((framessize,1)) #bool whether DLP is active
        self.FloodLightIsOn = np.zeros((framessize,1)) #flood light overrides all other patterns and hits entire fov
        self.IllumInvert = np.zeros((framessize,1)) #whether pattern is inverted (invert has precedence over floodlight)
        self.IllumFlipLR = np.zeros((framessize,1)) #flips output left/right with respect to worm's body
        self.IllumRectOrigin = np.zeros((framessize,2)) #center of the freehand rectangular illumination in wormspace
        self.IllumRectRadius = np.zeros((framessize,2)) #xy value describing dimension of rectangle
        self.StageVelocity = np.zeros((framessize,2)) #velocity sent to stage in stage units/second
        self.StagePosition = np.zeros((framessize,2))
        self.StageFeedbackTarget = np.zeros((framessize,2))
        self.FirstLaser = np.zeros((framessize,1))
        self.SecondLaser = np.zeros((framessize,1))
        self.ProtocolIsOn = np.zeros((framessize,1))
        self.ProtocolStep = np.zeros((framessize,1))
        
        self.curve_data = np.zeros((framessize,100))  # curve_data
        self.angle_data = np.zeros((framessize,101))  # angle_data
        self.curvedatafiltered = np.zeros((framessize,100)) # curvedatafiltered
        # self.LaserPower = []  # 一个空的list
        # self.GreenLaser = np.zeros((framessize,1))  #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        # self.BlueLaser = np.zeros((framessize,1)) #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        # self.HeadCurv = np.zeros((framessize,1)) #curvature of the head
        # self.HeadCurvDeriv = np.zeros((framessize,1)) #derivative of curvature of the head

def Extract_Yaml_Multiprocess_one(yaml_path):
    import os
    import time
    import math
    import datetime
    import multiprocessing as mp

    # 并行导入一个Yaml文件
    time_start = time.time()
    ListFile = OpenYaml(yaml_path) # 导入数据
    begin_num1 = Get_First_Frames(ListFile)
    end_num = Get_End_Frames(ListFile)

    framesline =  Get_Frames_line(ListFile)  # Frames的行数
    real_frames = math.ceil((len(ListFile)-(framesline+1))/99)
    print("real frames:",real_frames)
    All_Frames_num = end_num-begin_num1+1  # 总的帧数
    print("End- begin Total frames:",All_Frames_num)
    
    YamlData = Just_Get_Raw(yaml_path)

    time_end = time.time()
    print('Load data time cost:',time_end-time_start,'s')

    frames = len(YamlData.Centerline)  # 数据帧数



    num_cores = int(mp.cpu_count())

    each_core_pro_num = math.ceil(frames/num_cores) # 平均每个处理多少帧

    # 并行处理数据
    time_start = time.time()

    p=mp.Pool(num_cores) #创建含有num_cores个进程的进程池
    results=[] #存放每一个进程返回的结果

    for i in range(num_cores): # 启动8个进程
        if i<num_cores-1:
            centerlines = Multi_task(i,YamlData.Centerline[i*each_core_pro_num:(i+1)*each_core_pro_num,:,:])
            r=p.apply_async(Get_Multi_curvedatafiltered,args=(centerlines,)) # 产生一个非同步进程，函数newsin的参数用args传递
            results.append(r) # 将返回结果放入results
        else:
            centerlines = Multi_task(i,YamlData.Centerline[i*each_core_pro_num:-1,:,:]) # 最后一个核把剩下全部计算
            r=p.apply_async(Get_Multi_curvedatafiltered,args=(centerlines,)) # 产生一个非同步进程，函数newsin的参数用args传递
            results.append(r) # 将返回结果放入results
    # print(i)
    p.close() #关闭进程池
    p.join()  #结束

    time_end = time.time()
    print('并行处理数据 time cost:',time_end-time_start,'s')


    # 合并数据
    for item in results:
        data = item.get()
        dataid = data.taskid
        if dataid<num_cores-1:
            YamlData.angle_data[dataid*each_core_pro_num:(dataid+1)*each_core_pro_num,:] = data.angle_data[:,:]
            YamlData.curve_data[dataid*each_core_pro_num:(dataid+1)*each_core_pro_num,:] = data.curve_data[:,:]
            YamlData.curvedatafiltered[dataid*each_core_pro_num:(dataid+1)*each_core_pro_num,:] = data.curvedatafiltered[:,:]
            YamlData.worm_length = YamlData.worm_length+data.worm_length
        else:
            YamlData.angle_data[dataid*each_core_pro_num:-1,:] = data.angle_data
            YamlData.curve_data[dataid*each_core_pro_num:-1,:] = data.curve_data
            YamlData.curvedatafiltered[dataid*each_core_pro_num:-1,:] = data.curvedatafiltered
            YamlData.worm_length = YamlData.worm_length+data.worm_length
    YamlData.worm_length = YamlData.worm_length/All_Frames_num

    return(YamlData)