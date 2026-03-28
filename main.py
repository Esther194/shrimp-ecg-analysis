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

waveNumber=0#波的個數
wavein,waveout=[],[]#入波出波時間
wave1,wave2=[],[]#作圖的波


#圖
def ECG(ax,l=0.5,begin=0, end=600,co='k'):
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

def periodGraph(ax):
    ax.clear()
    global wave1
    global wave2
    ax.plot(wave1,wave2,linewidth='1',color='k')
    
def FourierTransformGraph(ax):
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

#獲取入波和出波的時間點
def getPoint ():
    a=pd.read_excel("data.xlsx")
    begin,end=0,600
    e=0#出波點計數器
    f=0#反向推算的標的
    global waveNumber
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
                    waveNumber+=1
#陣列轉換
def changeArray(wave):
    global wave1
    global wave2
    global waveNumber
    wave1.clear()
    wave2.clear()
    wave1.append(wave[0])
    wave1.append(wave[0])
    wave1.append(wave[1])
    wave2.append(0)
    wave2.append(wave[1]-wave[0])
    wave2.append(wave[1]-wave[0])
    for i in range(0,waveNumber-2):
        wave1.append(wave[i+1])
        wave1.append(wave[i+1])
        wave1.append(wave[i+2])
        wave2.append(wave[i+1]-wave[i])
        wave2.append(wave[i+2]-wave[i+1])
        wave2.append(wave[i+2]-wave[i+1])
    
e=0#週期頻率變化按鈕
#元件
def menu():
    menu=tk.OptionMenu((root), var, "心電圖", "頻率","傅立葉轉換","波型比較")
    menu.place(x=0,y=0)
    var.trace('w',show)
    var.set("菜單")
    
def tool(canvas,root):
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    
class Counter:
    def __init__(self, root, p, l, w, ax, canvas):
        self.root = root
        self.count1 = 1
        self.count2 = 1
        self.w = w
        self.ax = ax
        self.canvas = canvas

        self.plus_button1 = tk.Button(root, command=lambda: self.plus1(), text=">")
        self.minus_button1 = tk.Button(root, command=lambda: self.minus1(), text="<")
        self.plus_button2 = tk.Button(root, command=lambda: self.plus2(), text=">")
        self.minus_button2 = tk.Button(root, command=lambda: self.minus2(), text="<")

        self.label1 = tk.Label(root, text=self.count1, font=(24))
        self.label2 = tk.Label(root, text=self.count2, font=(24))

        self.plus_button1.place(x=p+13, y=l-4)
        self.minus_button1.place(x=p-20, y=l-3)
        self.plus_button2.place(x=p+213, y=l-4)
        self.minus_button2.place(x=p+180, y=l-3)

        self.label1.place(x=p, y=l)
        self.label2.place(x=p+200, y=l)
    
    def plus1(self):
        if  self.count1 < self.w:
            self.count1+=1
            self.ax.clear()
            self.label1.config(text=self.count1)
            ECG(self.ax,5,int(wavein[self.count2-1]*1000),int(waveout[self.count2-1]*1000),'r')
            ECG(self.ax,5,int(wavein[self.count1-1]*1000),int(waveout[self.count1-1]*1000),'b')
            self.canvas.draw()
            
    def plus2(self):
       if  self.count2 < self.w:
           self.count2+=1
           self.ax.clear()
           self.label2.config(text=self.count2)
           ECG(self.ax,5,int(wavein[self.count1-1]*1000),int(waveout[self.count1-1]*1000),'b')
           ECG(self.ax,5,int(wavein[self.count2-1]*1000),int(waveout[self.count2-1]*1000),'r')
           self.canvas.draw()
           
    def minus1(self):
        if  self.count1 > 1:
            self.count1-=1
            self.ax.clear()
            self.label1.config(text=self.count1)
            ECG(self.ax,5,int(wavein[self.count2-1]*1000),int(waveout[self.count2-1]*1000),'r')
            ECG(self.ax,5,int(wavein[self.count1-1]*1000),int(waveout[self.count1-1]*1000),'b')
            self.canvas.draw()
            
    def minus2(self):
       if  self.count2 > 1:
           self.count2-=1
           self.ax.clear()
           self.label2.config(text=self.count2)
           ECG(self.ax,5,int(wavein[self.count1-1]*1000),int(waveout[self.count1-1]*1000),'b')
           ECG(self.ax,5,int(wavein[self.count2-1]*1000),int(waveout[self.count2-1]*1000),'r')
           self.canvas.draw()
    
#元件變化   

def periodFrequencyButton(tb,ax,canvas):
    global e
    global wave2
    tb2=["週期","頻率"]
    tb["text"]=tb2[e%2]
    changeArray(wavein)   
    if(e%2==1):
        for i in range(2* waveNumber +3):
            if(wave2[i]!=0):
                wave2[i]=1/wave2[i]
        periodGraph(ax)
        ax.set_ylabel("frequency(Hz)")
    else:
        periodGraph(ax)
        ax.set_ylabel("period(s)")
    canvas.draw()
    e+=1
        
def show(i,j,k):
    if(var.get()=="心電圖"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        root1.state("zoomed")
        ax6=fig1.add_subplot()
        ECG(ax6)
        tool(canvas1,root1)
        canvas1.draw()
    elif(var.get()=="頻率"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        root1.state("zoomed")
        ax6=fig1.add_subplot()
        tool(canvas1,root1)
        tbu=tk.Button(root1,command=lambda:periodFrequencyButton(tbu,ax6,canvas1))
        tbu.pack()
        periodFrequencyButton(tbu,ax6,canvas1)
    elif(var.get()=="傅立葉轉換"):
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        root1.state("zoomed")
        ax6=fig1.add_subplot()
        FourierTransformGraph(ax6)
        tool(canvas1,root1)
        canvas1.draw()
    elif(var.get()=="波型比較"):
        global wavein,waveout,waveNumber#入波出波時間
        root1=tk.Tk()
        fig1=Figure()
        canvas1=FigureCanvasTkAgg(fig1,master=root1)
        canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        root1.state("zoomed")
        ax1=fig1.add_subplot()
        ax2=fig1.add_subplot()
        ax3=fig1.add_subplot()
        ax4=fig1.add_subplot()
        ax1.set_position([0.1,0.6,0.35,0.35])
        ax2.set_position([0.1,0.1,0.35,0.35])
        ax3.set_position([0.6,0.6,0.35,0.35])
        ax4.set_position([0.6,0.1,0.35,0.35])
        tool(canvas1,root1)
        counter1= Counter(root1,250,290,waveNumber,ax1,canvas1)
        counter2= Counter(root1,250,620,waveNumber,ax2,canvas1)
        counter3= Counter(root1,950,290,waveNumber,ax3,canvas1)
        counter4= Counter(root1,950,620,waveNumber,ax4,canvas1)
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
tb=tk.Button(root,command=lambda:periodFrequencyButton(tb,ax2,canvas))
tb.place(relx=1.0,rely=0.0,anchor="ne")
menu()
tool(canvas,root)

getPoint()
ECG(ax1)
changeArray(wavein)
periodFrequencyButton(tb,ax2,canvas)
FourierTransformGraph(ax3)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tk.mainloop()