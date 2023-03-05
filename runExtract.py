import cv2
import numpy as np
from YamlLib.YamlFrames import YamlExportMatAll
import time,os

"""
视频缩小了一倍进行存储的
"""

# data_folder = "G:/WenLabData/ExtractWormPoseData/xrk/N2_Free_Moving/YamlFiles"

data_folder = "G:/WenLabData/ExtractWormPoseData/Colbert-hpis258/YamlFiles"
SaveFolder = os.path.join(data_folder,'ExtractData')

YamlExportMatAll(data_folder,SaveFolder=SaveFolder,
                 Centerline=True,
                 curvedatafiltered=True,
                 TimeElapsed=True,
                 Head=True,
                 mean_worm_length=True,
                 name=True,
                 worm_length=True,
                 savevideo=False,
                 )



