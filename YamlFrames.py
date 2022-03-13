import os




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
    linenumber = lines[-98].split(':')[-1]
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


class YamlFrames(object):
    def __init__(self,name: str, framessize: int):
        import numpy as np
        self.name = name
        self.ExperimentTime = 'Sun May 16 20:51:33 2021'
        self.DefaultGridSizeForNonProtocolIllum = np.array([20,100]) # DefaultGridSizeForNonProtocolIllum
        self.FrameNumber = np.zeros((framessize,1))  #internal frame number, not nth recorded frame
        self.TimeElapsed = np.zeros((framessize,1)) #time since start of experiment (in s) = sElapsed+ 0.001*msRemElapsed
        self.BoundaryA = np.zeros((framessize,2,100)) # N*2*100 x,y BoundaryA position in pixels on camera
        self.BoundaryB = np.zeros((framessize,2,100)) # N*2*100 x,y BoundaryB position in pixels on camera
        self.SegmentedCenterline = np.zeros((framessize,2,100))  # N*2*100 x,y centerline position in pixels on camera
        self.Head = np.zeros((framessize,2)) #position in pixels on camera
        self.Tail = np.zeros((framessize,2)) #position in pixels on camera
        self.DLPisOn = np.zeros((framessize,1)) #bool whether DLP is active
        self.FloodLightIsOn = np.zeros((framessize,1)) #flood light overrides all other patterns and hits entire fov
        self.IllumInvert = np.zeros((framessize,1)) #whether pattern is inverted (invert has precedence over floodlight)
        self.IllumFlipLR = np.zeros((framessize,1)) #flips output left/right with respect to worm's body
        self.IllumRectOrigin = np.zeros((framessize,2)) #center of the freehand rectangular illumination in wormspace
        self.IllumRectRadius = np.zeros((framessize,2)) #xy value describing dimension of rectangle
        self.StageVelocity = np.zeros((framessize,2)) #velocity sent to stage in stage units/second
        self.ProtocolIsOn = np.zeros((framessize,1)) #bool whether you're using protocol
        self.ProtocolStep = np.zeros((framessize,1)) #what step within protocol is currently selected
        self.GreenLaser = np.zeros((framessize,1))  #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        self.BlueLaser = np.zeros((framessize,1)) #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        self.HeadCurv = np.zeros((framessize,1)) #curvature of the head
        self.HeadCurvDeriv = np.zeros((framessize,1)) #derivative of curvature of the head
        self.StagePosition = np.zeros((framessize,2))
        self.StageFeedbackTarget = np.zeros((framessize,2))

    # def Get_ExperimentTime(self,lines):
    #     # 输入List
        


