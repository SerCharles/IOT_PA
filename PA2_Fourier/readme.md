## 复现方法

## 1.傅里叶变换

### 1.1 对给定的函数进行DFT

使用Spectrum.py文件，type是函数类型（constant/linear/sin），N是个数（16/64/1024)

```shell
python Spectrum.py --type=constant --N=16
python Spectrum.py --type=constant --N=64
python Spectrum.py --type=constant --N=1024
python Spectrum.py --type=linear --N=16
python Spectrum.py --type=linear --N=64
python Spectrum.py --type=linear --N=1024
python Spectrum.py --type=sin --N=16
python Spectrum.py --type=sin --N=64
python Spectrum.py --type=sin --N=1024
```

### 1.2 对res1.wav进行DFT和STFT

使用Spectrum.py文件，要求res1.wav在代码根目录下res文件夹内（我提交的格式），具体代码如下

**对res1.wav本身进行DFT**

```shell
python Spectrum.py --type=load
```

**对res1.wav补零波进行DFT**

```shell
python Spectrum.py --type=add_zero
```

**对res1.wav补零波进行STFT**

此时window为窗口大小，我测试了16,64,256,1024

```shell
python Spectrum.py --type=stft --window=16
python Spectrum.py --type=stft --window=64
python Spectrum.py --type=stft --window=256
python Spectrum.py --type=stft --window=1024
```

## 2.滤波

### 2.1 低通滤波

使用Filt.py文件，其中type为moving_average, window为窗口大小（3,4,8,16）

```shell
python Filt.py --type=moving_average --window=3
python Filt.py --type=moving_average --window=4
python Filt.py --type=moving_average --window=8
python Filt.py --type=moving_average --window=16
```

### 2.2 带通滤波

```shell
python Filt.py --place=res2 --type=bandpass
```

