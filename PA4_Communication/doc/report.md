---
typora-root-url: ./
---

# 物联网第四次作业报告

软73 沈冠霖 2017013569

## 一.实现方法

### 调制-解调方法

我使用了脉冲调制-解调方法，而没有使用QPSK相位调制-解调算法。虽然后者更加鲁棒，但是因为接收数据需要录音，而录音的首尾阶段都会录制有一段空白，QPSK算法并不能知道哪里是空白哪里不是，而脉冲算法则可以通过计算脉冲开始时刻间隔，如果不符合条件就舍去来解决这个问题。

### 图形界面

我使用python的tkinder库实现图形界面。

发送端能够检测输入合法性，指定保存文件名，并且将输入进行转二进制，调制，保存。界面如下：

![sender](/sender.png)

接收端能够进行录音来接收信息，同时可以输入原始信息，对接受信息进行解调进行比较求得各项指标。

![receiver](/receiver.png)

![report](/report.png)

### 实验方法

我使用两台电脑，一台运行发送程序生成wav并且播放，一台运行接收程序录音并且解码，通过更改两台电脑的距离来进行实验。



## 二.实验结果

我测试了5个距离，每个距离重复测量2次取平均值，原始数据如下：

| 实验编号\结果 | 距离(cm) | 传输速率(byte/s) | 丢包率（%） | 准确率（%） |
| ------------- | -------- | ---------------- | ----------- | ----------- |
| 1             | 0        | 4.17             | 0           | 100         |
| 2             | 0        | 4.35             | 0           | 100         |
| 3             | 25       | 4.13             | 0.94        | 90.67       |
| 4             | 25       | 3.97             | 7.55        | 69.81       |
| 5             | 50       | 4.03             | 8.49        | 17.92       |
| 6             | 50       | 4.57             | 33.02       | 29.36       |
| 7             | 75       | 4.41             | 99.06       | 0           |
| 8             | 75       | 4.22             | 97.17       | 0           |
| 9             | 100      | 3.48             | 100         | 0           |
| 10            | 100      | 3.55             | 100         | 0           |



**平均传输速率：**4.09byte/s

**丢包率：**

| 距离(cm)      | 0    | 25   | 50    | 75    | 100  |
| ------------- | ---- | ---- | ----- | ----- | ---- |
| **丢包率(%)** | 0    | 4.25 | 20.76 | 98.12 | 100  |

**准确率：**

| 距离(cm)      | 0    | 25    | 50    | 75   | 100  |
| ------------- | ---- | ----- | ----- | ---- | ---- |
| **准确率(%)** | 100  | 80.24 | 23.64 | 0    | 0    |



## 三.分析和总结

本次实验的结果和预期大致吻合：距离接近0的时候传输完全正确；距离越远，丢包率越高，准确率越低；距离足够远的时候声音完全衰减无法被捕捉，无法接收到任何有效信息。进一步分析准确率下降的原因，因为我的准确率比较是逐位比较，因此一旦中间有丢包，结果就完全乱了，准确率大幅下降而且显示的数据也会变成无意义的乱码。

本次实验让我能够更好的对比上次作业的脉冲和QPSK两种算法并且选取正确的算法，也更加深入理解了无线通信的原理和其困难之处。