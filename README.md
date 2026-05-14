# 科研绘图库
## 结构总览
research-plot-utils/

--- **基础功能区** ---

├── style.py            # 全局风格

├── colors.py           # 常用颜色

├── save.py             # 保存为 pdf 的统一接口


--- **常用图** ---

├── bar.py              # 柱形图

├── histogram.py        # 直方图

├── radar.py            # 雷达图

├── scatter.py          # 散点图

├── sunburst.py         # 双层扇面图

├── sunburst.py         # 双层扇面图

├── umap_plot.py        # umap散点分布图


## audio绘图子库
- 专门放audio绘图所需的代码。非通用绘图。

├── spectrogram.py            # 梅尔频谱图

## score绘图子库
- 专门放score乐谱绘图所需的代码。


## ⚠️警告
这里就是代码库，不要存放数据，污染库环境

## 关于使用方式
本地导入：适用于初期开发
```
import sys
sys.path.append("/data7/fwh/plot-utils/")
```
当开发稳定，可以在作为项目内的一个包，放在：
./plot-utils