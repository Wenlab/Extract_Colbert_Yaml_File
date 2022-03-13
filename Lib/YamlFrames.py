import numpy as np

def OpenYaml(yaml_path:str):
    Yaml_file = []
    with open(yaml_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n') # 删除末尾的回车
            line = line.strip() # 删除前面的空格
            Yaml_file.append(line)
    return(Yaml_file)

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
        # self.LaserPower = OneFrameList[93].split(':')[-1]
        # self.GreenLaser = 
        # self.BlueLaser =
        # self.HeadCurv = 
        # self.HeadCurvDeriv =

class YamlFrames(object):
    def __init__(self,name: str, framessize: int):
        import numpy as np
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
        # self.LaserPower = []  # 一个空的list
        # self.GreenLaser = np.zeros((framessize,1))  #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        # self.BlueLaser = np.zeros((framessize,1)) #int 0-100 of relative laser power. -1 means leaser is not being controlled programmatically
        # self.HeadCurv = np.zeros((framessize,1)) #curvature of the head
        # self.HeadCurvDeriv = np.zeros((framessize,1)) #derivative of curvature of the head

