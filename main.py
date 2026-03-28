import tkinter as tk
from tkinter import filedialog
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

#類別，用於繪圖、顯示元件
class G:
    def __init__(self,b=0,e=600):
        self.waveNumber=0#波的個數
        self.wavein=[]#入波時間
        self.waveout=[]#出波時間
        self.wave1=[]#作圖的波
        self.wave2=[]#作圖的波
        
        
        self.selected_file = filedialog.askopenfilename(parent=root)#選檔案
        self.file= pd.read_excel(self.selected_file)#讀檔案
        
        self.begin=b#設定開始繪圖的時間
        self.end=e#設定結束繪圖的時間
        self.e=0
    #繪製心電圖   
    def ECG(self,ax,l=0.5,begin=0, end=600,co='k'):
        d = 0#計算時間(y座標)
        for i in range(begin, end):
            b = self.file.iat[i, 0]  # 第一(i)筆資料
            c = self.file.iat[i + 1, 0]  # 第二(i+1)筆資料
            xpoints = np.array([(d / 1000), ((d + 1) / 1000)])
            ypoints = np.array([b, c])
            ax.plot(xpoints, ypoints, linewidth=l, color=co)
            d += 1#時間增加(y座標)
            self.wave1.extend([b, c])
            self.wave2.extend([0, c - b]) 
    #繪製頻率與週期
    def periodGraph(self,ax):
        ax.clear()#清除子圖
        ax.plot(self.wave1,self.wave2,linewidth='1',color='k')#重新使用wave1、wave2繪製圖形
    #繪製傅立葉轉換   
    def FourierTransformGraph(self,ax):
        e=self.file[self.begin:self.end]# 計算心電圖信號的取樣率和時間間隔
        s = 1000  # 取樣率，假設為1000Hz
        fft_result = fft(e)# 計算頻率軸
        frequencies = fftfreq(len(e), 1/s)# 繪製頻譜
        ax.plot(frequencies, np.abs(fft_result))#畫圖
        plt.show()
        
    #獲取入波和出波的時間點
    def getPoint (self):
        e=0#出波點計數器
        f=0#反向推算的標的
        for i in range(self.begin,self.end):
            c=self.file.iat[i+1,0]#設第二(i+1)筆資料為c點
            if(c>0.01 and i> f):#如果c點的電位高於0.01且距上一個入波點超過50微秒
                self.wavein.append(i/1000)#在wavein增加此時的時間點
                f=i+50
                e=0#已記錄入波點
                if(f>self.end):#防止超出陣列
                    f=self.end
                while(e==0):
                    f=f-1
                    c=self.file.iat[f-1,0]#設第一(f-1)筆資料為c點
                    if(c<-0.04):#如果c點的電位低於-0.04且之前的入波點大於出波點    
                        e=1#已記錄出波點
                        self.waveout.append(f/1000)#在waveout增加此時的時間點
                        self.waveNumber+=1#增加波的個數
                        
    #陣列轉換
    def changeArray(self,wave):
        self.wave1.clear()#清除wave1
        self.wave2.clear()#清除wave2
        #將陣列轉換籌能繪圖的形式
        self.wave1.append(wave[0])
        self.wave1.append(wave[0])
        self.wave1.append(wave[1])
        self.wave2.append(0)
        self.wave2.append(wave[1]-wave[0])
        self.wave2.append(wave[1]-wave[0])
        for i in range(0,self.waveNumber-2):
            self.wave1.append(wave[i+1])
            self.wave1.append(wave[i+1])
            self.wave1.append(wave[i+2])
            self.wave2.append(wave[i+1]-wave[i])
            self.wave2.append(wave[i+2]-wave[i+1])
            self.wave2.append(wave[i+2]-wave[i+1])   
    #菜單元件
    def menu(self):
        menu=tk.OptionMenu((root), var, "心電圖", "頻率","傅立葉轉換","波型比較")#設定下拉選單內的文字說明即在哪個視窗開啟(root)
        menu.place(x=0,y=0)#設定位置
        var.trace('w',self.show)#反應與show函式連動
        var.set("菜單")#設定初始名字
    #工具列    
    def tool(self,canvas,root):
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
    #頻率週期切換按鈕
    def periodFrequencyButton(self,tb,ax,canvas):
        #設定兩個字串交替顯示
        tb2=["週期","頻率"]
        tb["text"]=tb2[self.e%2]
        
        self.changeArray(self.wavein)#轉換陣列   
        if(self.e%2==1):#如果此時為頻率
            #將wave2變成倒數
            for i in range(2* self.waveNumber +3):
                if(self.wave2[i]!=0):
                    self.wave2[i]=1/self.wave2[i]
                    
            self.periodGraph(ax)#繪圖
            ax.set_ylabel("frequency(Hz)")#設定y軸標籤為frequency(Hz)
        else:
            self.periodGraph(ax)#繪圖
            ax.set_ylabel("period(s)")#設定y軸標籤為period(s)
        canvas.draw()
        self.e+=1
    #菜單   
    def show(self,i,j,k):
        if(var.get()=="心電圖"):#如果選擇"心電圖"
            root1=tk.Tk()
            fig1=Figure()
            canvas1=FigureCanvasTkAgg(fig1,master=root1)
            canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
            root1.state("zoomed")#打開為全螢幕
            ax6=fig1.add_subplot()
            self.ECG(ax6)#畫圖
            self.tool(canvas1,root1)#放入工具列
            canvas1.draw()
        elif(var.get()=="頻率"):#如果選擇"頻率"
            root1=tk.Tk()
            fig1=Figure()
            canvas1=FigureCanvasTkAgg(fig1,master=root1)
            canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
            root1.state("zoomed")#打開為全螢幕
            ax6=fig1.add_subplot()
            self.tool(canvas1,root1)#放入工具列
            tbu=tk.Button(root1,command=lambda:self.periodFrequencyButton(tbu,ax6,canvas1))
            tbu.pack()#切換週期、頻率按鈕
            self.periodFrequencyButton(tbu,ax6,canvas1)#畫圖
        elif(var.get()=="傅立葉轉換"):#如果選擇"傅立葉轉換"
            root1=tk.Tk()
            fig1=Figure()
            canvas1=FigureCanvasTkAgg(fig1,master=root1)
            canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
            root1.state("zoomed")#打開為全螢幕
            ax6=fig1.add_subplot()
            self.FourierTransformGraph(ax6)#畫圖
            self.tool(canvas1,root1)#放入工具列
            canvas1.draw()
        elif(var.get()=="波型比較"):#如果選擇"波型比較"
            global wavein,waveout,waveNumber#入波出波時間
            root1=tk.Tk()
            fig1=Figure()
            canvas1=FigureCanvasTkAgg(fig1,master=root1)
            canvas1.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
            root1.state("zoomed")#打開為全螢幕
            #創造4個子圖
            ax1=fig1.add_subplot()
            ax2=fig1.add_subplot()
            ax3=fig1.add_subplot()
            ax4=fig1.add_subplot()
            ax1.set_position([0.1,0.6,0.35,0.35])
            ax2.set_position([0.1,0.1,0.35,0.35])
            ax3.set_position([0.6,0.6,0.35,0.35])
            ax4.set_position([0.6,0.1,0.35,0.35])
            self.tool(canvas1,root1)#放入工具列
            counter1= Counter(root1,250,290,self.waveNumber,ax1,canvas1,self.wavein,self.waveout)
            counter2= Counter(root1,250,620,self.waveNumber,ax2,canvas1,self.wavein,self.waveout)
            counter3= Counter(root1,950,290,self.waveNumber,ax3,canvas1,self.wavein,self.waveout)
            counter4= Counter(root1,950,620,self.waveNumber,ax4,canvas1,self.wavein,self.waveout)
            canvas1.draw()
            
class Counter:
    def __init__(self, root, p, l, w, ax, canvas,wi,wo):
        self.C=G()
        self.wavein=wi
        self.waveout=wo
        
        self.root = root
        self.count1 = 1
        self.count2 = 1
        self.w = w
        self.ax = ax
        self.canvas = canvas
        #設定四種功能按鈕
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
    #對比子圖選擇波行對比
    def plus1(self):
        if  self.count1 < self.w:
            self.count1+=1
            self.ax.clear()
            self.label1.config(text=self.count1)
            self.C.ECG(self.ax,5,int(self.wavein[self.count2-1]*1000),int(self.waveout[self.count2-1]*1000),'r')
            self.C.ECG(self.ax,5,int(self.wavein[self.count1-1]*1000),int(self.waveout[self.count1-1]*1000),'b')
            self.canvas.draw()
            
    def plus2(self):
       if  self.count2 < self.w:
           self.count2+=1
           self.ax.clear()
           self.label2.config(text=self.count2)
           self.C.ECG(self.ax,5,int(self.wavein[self.count1-1]*1000),int(self.waveout[self.count1-1]*1000),'b')
           self.C.ECG(self.ax,5,int(self.wavein[self.count2-1]*1000),int(self.waveout[self.count2-1]*1000),'r')
           self.canvas.draw()
           
    def minus1(self):
        if  self.count1 > 1:
            self.count1-=1
            self.ax.clear()
            self.label1.config(text=self.count1)
            self.C.ECG(self.ax,5,int(self.wavein[self.count2-1]*1000),int(self.waveout[self.count2-1]*1000),'r')
            self.C.ECG(self.ax,5,int(self.wavein[self.count1-1]*1000),int(self.waveout[self.count1-1]*1000),'b')
            self.canvas.draw()
            
    def minus2(self):
       if  self.count2 > 1:
           self.count2-=1
           self.ax.clear()
           self.label2.config(text=self.count2)
           self.C.ECG(self.ax,5,int(self.wavein[self.count1-1]*1000),int(self.waveout[self.count1-1]*1000),'b')
           self.C.ECG(self.ax,5,int(self.wavein[self.count2-1]*1000),int(self.waveout[self.count2-1]*1000),'r')
           self.canvas.draw()
           
root=tk.Tk()
fig=Figure()

ax2=fig.add_subplot()
ax1=fig.add_subplot()
ax3=fig.add_subplot()

ax2.set_position([0.1,0.7,0.8,0.3])
ax1.set_position([0.1,0.4,0.8,0.3])
ax3.set_position([0.1,0.05,0.8,0.3])

canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

A=G()
var=tk.StringVar(root)
tb=tk.Button(root,command=lambda:A.periodFrequencyButton(tb,ax2,canvas))
tb.place(relx=1.0,rely=0.0,anchor="ne")

A.getPoint()
A.ECG(ax1)
A.FourierTransformGraph(ax3)
A.changeArray(A.wavein)
A.periodFrequencyButton(tb,ax2,canvas)

A.menu()
A.tool(canvas,root)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tk.mainloop()
