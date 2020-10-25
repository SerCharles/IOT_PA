## 复现方法

本次作业我使用python3+numpy+wave+scipy库完成，直接在src目录下运行即可，有缺包请用pip/conda直接安装。

**要求src文件夹里有sound文件夹**

## 1.脉冲调制解调

使用main_pulse.py文件，seq_len是生成的随机序列长度，默认100

```shell
python main_pulse.py --seq_len=100
python main_pulse.py --seq_len=300
python main_pulse.py --seq_len=1000
```

中间结果保存在src/sound/pulse.wav下

## 2.相位调制解调

### 2.1 基本QPSK

使用main_phase.py文件，seq是生成的随机序列长度，默认100

```shell
python main_phase.py --seq_len=100
python main_phase.py --seq_len=300
python main_phase.py --seq_len=1000
```

中间结果保存在src/sound/phase.wav下

### 2.2 带白噪声的QPSK

使用main_phase.py文件，seq_len参数含义和中间结果位置同上。

想要查看有无噪声的波形，可以设置plot参数为1

```shell
python main_phase.py --plot=1
```

想要添加噪声需要设置noise参数为1，SNR参数为想要的信噪比

```shell
python main_phase.py --noise=1 --SNR=20
python main_phase.py --noise=1 --SNR=10
python main_phase.py --noise=1 --SNR=0
```

