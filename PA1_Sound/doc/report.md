---
typora-root-url: ./
---

**1.主界面和结果**

python部分：

SignalProcess.py运行生成函数后，会在同目录生成sound.wav音频文件。

运行读取函数后会得到波形，如下（20HZ）：

![wave](/wave.png)

安卓部分：

主界面如下

![](/main.jpg)

运行结果参考演示视频

**2.困难：读取本地音频**

解决方法：

1.点击按钮发送一个选取audio/*的intent

2.回调函数用data.uri作为uri初始化音频播放器，用getContentResolver().query()得到的cursor搜索音频名称并且显示

3.新录制的音频可能在媒体库未更新找不到：每次录制和生成本地音频都用代码通知媒体库生成了新的音频。