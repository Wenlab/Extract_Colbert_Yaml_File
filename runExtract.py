import os
import time
from YamlLib.YamlFrames import Extract_Yaml_Multiprocess_one, GetWormName

yaml_path = 'H:/WenLabData/20210715_1627_w1/20210715_1627_w1/20210715_1627_w1.yaml'

wormname = GetWormName(yaml_path)
print("Process worm:", wormname)

yaml_time_start = time.time()
# YamlData = Extract_Yaml_Multiprocess_one(yaml_path)
YamlData = Extract_Yaml_Multiprocess_one(yaml_path)
yaml_time_end = time.time()
print('All time cost:', yaml_time_end - yaml_time_start, 's')
