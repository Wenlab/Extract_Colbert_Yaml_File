import cv2
import numpy as np
from YamlLib.YamlFrames import YamlExportMatAll
import time,os

"""
视频缩小了一倍进行存储的
"""

data_folder = "G:/WenLabData/ExtractWormPoseData/xrk/N2_Free_Moving/YamlFiles"



SaveFolder = os.path.join(data_folder,'ExtractData')

YamlExportMatAll(data_folder,SaveFolder=SaveFolder,
                ExperimentTime=True,
                BoundaryA=True,
                BoundaryB=True,
                Centerline=True,
                curvedatafiltered=True,
                TimeElapsed=True,
                angle_data=True,
                curve_data=True,
                mean_worm_length=True,
                StageFeedbackTarget=True,
                StagePosition=True,
                StageVelocity=True,
                Head=True,
                name=True,
                worm_length=True,
                savevideo=False,
                 )



