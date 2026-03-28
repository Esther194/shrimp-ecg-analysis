import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from scipy.fft import fft, fftfreq
w=0#波的個數
wavein,waveout=[],[]#入波出波時間
wave1,wave2=[],[]#作圖的波
#圖
def el(ax,l=0.5,begin=0, end=600,co='k'):
    a = pd.read_excel("data.xlsx")
    d = 0
    for i in range(begin, end):
        b = a.iat[i, 0]  # 第一(i)筆資料
        c = a.iat[i + 1, 0]  # 第二(i+1)筆資料
        xpoints = np.array([(d / 1000), ((d + 1) / 1000)])
        ypoints = np.array([b, c])
        ax.plot(xpoints, ypoints, linewidth=l, color=co)
        d += 1
        wave1.extend([b, c])
        wave2.extend([0, c - b]) 

def t(ax):
    ax.clear()
    global wave1
    global wave2
    ax.plot(wave1,wave2,linewidth='1',color='k')
    
def f(ax):
    # 讀取心電圖數據，將其存儲在一個NumPy數組中
    begin,end=0,600
    a=pd.read_excel("data.xlsx")
    e=a[begin:end]
    # 計算心電圖信號的取樣率和時間間隔
    s = 1000  # 取樣率，假設為1000Hz
    fft_result = fft(e)
    # 計算頻率軸
    frequencies = fftfreq(len(e), 1/s)
    # 繪製頻譜
    ax.plot(frequencies, np.abs(fft_result))
    plt.show()

#獲取入波出波點
def g():
    a=pd.read_excel("data.xlsx")
    begin,end=0,600
    e=0#出波點計數器
    f=0#反向推算的標的
    global w
    global wavein,waveout#入波出波時間
    for i in range(begin,end):
        c=a.iat[i+1,0]#第二(i+1)筆資料
        if(c>0.01 and i> f):
            wavein.append(i/1000)
            f=i+50
            e=0
            if(f>end):
                f=end
            while(e==0):
                f=f-1
                c=a.iat[f-1,0]#第一(f-1)筆資料
                if(c<-0.04):    
                    e=1
                    waveout.append(f/1000)
                    w=w+1
#陣列轉換
def cha(wave):
    global wave1
    global wave2
    global w
    wave1.clear()
    wave2.clear()
    wave1.append(wave[0])
    wave1.append(wave[0])
    wave1.append(wave[1])
    wave2.append(0)
    wave2.append(wave[1]-wave[0])
    wave2.append(wave[1]-wave[0])
    for i in range(0,w-2):
        wave1.append(wave[i+1])
        wave1.append(wave[i+1])
        wave1.append(wave[i+2])
        wave2.append(wave[i+1]-wave[i])
        wave2.append(wave[i+2]-wave[i+1])
        wave2.append(wave[i+2]-wave[i+1])
    
e=0#週期頻率變化按鈕
#元件
def men():
    menu=tk.OptionMenu((root), var, "心電圖", "頻率","傅立葉轉換","波型比較")
    menu.place(x=0,y=0)
    var.trace('w',show)
    var.set("菜單")
    
def tool(canvas,root):
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    
    
#元件變化   

def tb1(tb,ax,canvas):
    global e
    global wave2
    tb2=["週期","頻率"]
    tb["text"]=tb2[e%2]
    cha(wavein)   
    if(e%2==1):
        for i in range(2*w+3):
            if(wave2[i]!=0):
                wave2[i]=1/wave2[i]
        t(ax)
        ax.set_ylabel("frequency(Hz)")
    else:
        t(ax)
        ax.set_ylabel("period(s)")
    canvas.draw()
    e+=1

def show(i,j,k):
    if(var.get()=="心電圖"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        ax6=fig1.add_subplot()
        el(ax6)
        tool(canvas1,root1)
        canvas1.draw()
    elif(var.get()=="頻率"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        ax6=fig1.add_subplot()
        tool(canvas1,root1)
        tbu=tk.Button(root1,command=lambda:tb1(tbu,ax6,canvas1))
        tbu.pack()
        tb1(tbu,ax6,canvas1)
    elif(var.get()=="傅立葉轉換"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        ax6=fig1.add_subplot()
        f(ax6)
        tool(canvas1,root1)
        canvas1.draw()
    elif(var.get()=="波型比較"):
        global wavein,waveout#入波出波時間
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        ax1=fig1.add_subplot()
        ax2=fig1.add_subplot()
        ax3=fig1.add_subplot()
        ax4=fig1.add_subplot()
        ax1.set_position([0.1,0.6,0.35,0.35])
        ax2.set_position([0.1,0.1,0.35,0.35])
        ax3.set_position([0.6,0.6,0.35,0.35])
        ax4.set_position([0.6,0.1,0.35,0.35])
        tool(canvas1,root1)
        n,m=1,2
        for i in [ax1,ax2,ax3,ax4]:
            el(i,5,int(wavein[n]*1000),int(waveout[n]*1000),'b')
            el(i,5,int(wavein[m]*1000),int(waveout[m]*1000),'r')
            m+=1
        
        canvas1.draw()

    
root=tk.Tk()
fig=Figure()
a = pd.read_excel("data.xlsx")
ax2=fig.add_subplot()
ax1=fig.add_subplot()
ax3=fig.add_subplot()

ax2.set_position([0.1,0.7,0.8,0.3])
ax1.set_position([0.1,0.4,0.8,0.3])
ax3.set_position([0.1,0.05,0.8,0.3])




canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)


var=tk.StringVar(root)
tb=tk.Button(root,command=lambda:tb1(tb,ax2,canvas))
tb.place(relx=1.0,rely=0.0,anchor="ne")
men()
tool(canvas,root)



g()
el(ax1)
cha(wavein)
tb1(tb,ax2,canvas)
f(ax3)






canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tk.mainloop()