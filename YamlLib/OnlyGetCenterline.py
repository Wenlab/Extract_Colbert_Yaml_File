
class YamlFrames_Onely_Centerline(object):
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

def Just_Get_Centerline(yaml_path):
    from YamlLib.YamlFrames import OpenYaml,Get_First_Frames,Get_End_Frames,GetWormName,Get_ExperimentTime,Get_DefaultGrid
    from YamlLib.YamlFrames import Get_Any_Frame,Extract_OneFrame
    ListFile = OpenYaml(yaml_path)
    begin_num1 = Get_First_Frames(ListFile)
    end_num = Get_End_Frames(ListFile)
    All_Frames_num = end_num-begin_num1+1  # 总的帧数
    wormname = GetWormName(yaml_path)
    YamlFiles = YamlFrames_Onely_Centerline(wormname,All_Frames_num)
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
    return(YamlFiles)

# class Muti_


# def Just_Get_Centerline_Multiprocess(yaml_path):
#     import os
#     import time
#     import math
#     import datetime
#     import multiprocessing as mp
#     # 并行导入一个Yaml文件
#     time_start = time.time()
#     ListFile = OpenYaml(yaml_path) # 导入数据
#     begin_num1 = Get_First_Frames(ListFile)
#     end_num = Get_End_Frames(ListFile)

#     All_Frames_num = end_num-begin_num1+1  # 总的帧数
#     print("Total frames:",All_Frames_num)
#     YamlData = Just_Get_Raw(yaml_path)

#     time_end = time.time()
#     print('Load data time cost:',time_end-time_start,'s')
#     frames = len(YamlData.Centerline)  # 数据帧数


#     num_cores = int(mp.cpu_count())
#     each_core_pro_num = math.ceil(frames/num_cores) # 平均每个处理多少帧
#     # 并行处理数据
#     time_start = time.time()

#     p=mp.Pool(num_cores) #创建含有num_cores个进程的进程池
#     results=[] #存放每一个进程返回的结果

#     for i in range(num_cores): # 启动8个进程
#         if i<num_cores-1:
#             centerlines = Multi_task(i,YamlData.Centerline[i*each_core_pro_num:(i+1)*each_core_pro_num,:,:])
#             r=p.apply_async(Get_Multi_curvedatafiltered,args=(centerlines,)) # 产生一个非同步进程，函数newsin的参数用args传递
#             results.append(r) # 将返回结果放入results
#         else:
#             centerlines = Multi_task(i,YamlData.Centerline[i*each_core_pro_num:-1,:,:]) # 最后一个核把剩下全部计算
#             r=p.apply_async(Get_Multi_curvedatafiltered,args=(centerlines,)) # 产生一个非同步进程，函数newsin的参数用args传递
#             results.append(r) # 将返回结果放入results