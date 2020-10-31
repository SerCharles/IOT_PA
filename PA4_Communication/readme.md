---
typora-root-url: doc
---

**实验环境：**

- Windows10系统
- python 3.7.1

**依赖库：**

- 图形界面tkinder
- 录音库pyaudio（不能直接pip，安装方式见[此网页](https://blog.csdn.net/a506681571/article/details/85201279)）
- 音频库wave
- 数值计算库numpy
- 数值计算库scipy
- threading
- struct

**运行方法：**

请进入作业src目录下，保证里面有send和receive两个文件夹

**运行发送界面：**

```shell
python sender.py
```

请在两个框内输入非空ASCII码字符序列，之后会将对应的音频存到对应的位置下，如果输入不合法会报错。

![](/sender.png)

**运行接收界面：**

```shell
python receiver.py
```

请在框内输入你要对比的发送的非空ASCII码字符序列，输入不合法也会报错。

![](/receiver.png)

之后请开始录音，然后另一台设备播放发送界面生成的音频，音频播放完之后再结束录音。之后会卡顿界面进行解调运算，较为耗费时间（一个长英文句子需要几分钟解调完毕），请耐心等待不要强行关闭界面等。之后会弹框提示运行结果。

![](/report.png)

