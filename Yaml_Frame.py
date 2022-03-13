from cmath import nan


class Yaml_Frame:
    def __init__(self):
        ExperimentTime = 'None'
        DefaultGridSizeForNonProtocolIllum = [nan,nan]
        FrameNumbers = [nan]
        sElapsed = [nan]
        msRemElapsed = [nan]
        Head = [nan,nan]
        Tail = [nan,nan]
        BoudaryA = [1:200]*nan
        BoudaryB: n*100 维
        SegmentedCenterline: n*100维
        DLPIsOn: [number] n*1
        FloodLightIsOn: n*1
        IllumInvert: n*1
        IllumFlipLR: n*1
        IllumRectOrigin: n*2
        IllumRectRadius: n*2
        StageVelocity: n*2
        StagePosition: n*2
        WormSpeed: n*1
        StageFeedbackTarget: n*2
        LaserPower: n*2
        ProtocolIsOn: n*1
        ProtocolStep: n*1

       