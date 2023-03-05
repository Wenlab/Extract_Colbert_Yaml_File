# 提取线虫运动行为学Yaml文件的代码



# 这是提取线虫运动行为学Yaml文件的Python代码

# 使用并行计算

## 环境

需要Python环境,在虚拟环境中执行下面命令,安装依赖包

```python
pip install -r requirements.txt
```

### OpenCV安装

```python
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple 
pip install opencv-contrib-python
```

## 单独数据提取

打开`SingleProcess.ipynb`,在第一个block中 改成你的数据的路径即可

```python
yaml_path = '/home/data2/WormPoseData/ProcessingData/Temp/20210516_2051_w1.yaml'
```

## 带有图像的数据提取

打开`ExtractYamlVideo.ipynb`,在第一个block中 改成你的数据的路径即可

## 数据导出

在第二个block中选择需要导出的数据格式 `.pkl`或者`.mat`

### 导出.mat格式

```python
from YamlLib.YamlFrames import YamlExportMatAll
import time,os
from YamlLib.YamlFrames import Extract_Yaml_Multiprocess_one,YamlExportMatOne


data_folder = '***'
SaveFolder = os.path.join(data_folder,'ExtractData')

YamlExportMatAll(data_folder,SaveFolder=SaveFolder,
                 Centerline=True,
                 curvedatafiltered=True,
                 TimeElapsed=True,
                 Head=True,
                 mean_worm_length=True,
                 name=True,
                 worm_length=True
                 )
```

## 数据导入

导入转换的数据是一个 class()

需要必要的数据可以用
