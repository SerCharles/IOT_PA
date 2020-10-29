import random
from tkinter import *
import tkinter.messagebox
import hashlib
import time
from phase import phase_modulation, phase_demodulation
from utils import save_wave, load_wave, fill_seq, compare_seqs, generate_random_seq, get_success_rate, init_params, encode, decode



def send_signal(root, args, seq, save_place):
    '''
    描述：保存音频文件
    参数：窗体，args，序列，保存位置
    返回：无
    '''
    if len(seq) == 0:
        tkinter.messagebox.showinfo('错误','待传输信息不能为空！')
        return
    if len(save_place) == 0:
        tkinter.messagebox.showinfo('错误','保存的位置不能为空！')
        return
    try:
        original_seq = encode(seq)
        save_place += '.wav'
        print("The original seq is:\n", original_seq)
    except:
        tkinter.messagebox.showinfo('错误','待传输信息不合法！')
        return
    the_wave = phase_modulation(original_seq, args)
    save_wave(the_wave, framerate = args.framerate, sample_width = args.sample_width, nchannels = args.nchannels, save_base = args.save_base, file_name = save_place)
    root.destroy()

def init_ui(args):
    '''
    描述：初始化gui
    参数：无
    返回：无
    '''
    top = Tk()
    L1 = Label(top, text="请输入数据（必须是ASCII码）")
    L1.grid(row = 0, column = 0, stick = W, pady = 10)
    E1 = Entry(top, bd =5)
    E1.grid(row = 0, column = 1, stick = W, pady = 10)
    L2 = Label(top, text="请输入文件名（不含.wav）")
    L2.grid(row = 1, column = 0, stick = W, pady = 10)
    E2 = Entry(top, bd =5)
    E2.grid(row = 1, column = 1, stick = W, pady = 10)
    B1 = Button(top, text='确定', command = lambda: send_signal(top, args, E1.get(), E2.get()))
    B1.grid(row = 2, column = 1, stick = W, pady = 10)
    top.mainloop()



if __name__ == "__main__":
    args = init_params()
    init_ui(args)