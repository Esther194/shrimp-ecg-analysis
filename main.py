import pandas as pd
import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
w=0#波的個數
wavein,waveout=[],[]#入波出波時間
wave1,wave2=[],[]#作圖的波
#圖
def ele(ax):
    a=pd.read_excel("data.xlsx")
    begin,end=0,600
    e=0#出波點計數器
    f=0#反向推算的標的
    global w
  
    for i in range(begin,end):
        b=a.iat[i,0]#第一(i)筆資料
        c=a.iat[i+1,0]#第二(i+1)筆資料
        xpoints=np.array([(i/1000),((i+1)/1000)])
        ypoints=np.array([b,c])
        if(c>0.01 and i> f):
            ax.plot(xpoints,ypoints,marker='o',linewidth='0.5',color='k')
            wavein.append(i/1000)
            f=i+50
            e=0
            if(f>end):
                f=end
            while(e==0):
                f=f-1
                b=a.iat[f,0]#第二(f)筆資料
                c=a.iat[f-1,0]#第一(f-1)筆資料
                if(c<-0.04):    
                    waveout.append(f/1000)
                    xpoints=np.array([(f/1000),((f-1)/1000)])
                    ypoints=np.array([b,c])
                    ax.plot(xpoints,ypoints,marker='o',linewidth='0.5',color='b')
                    e=1
                    w=w+1
        else:
            ax.plot(xpoints,ypoints,linewidth='0.5',color='k')
    ax.set_ylabel("electric potential(V)")
    ax.set_xlabel("time(s)")

def t(ax):
    ax.clear()
    global w
    global wave1
    global wave2
    ax.plot(wave1,wave2,linewidth='1',color='k')

  
def cha(wave):
    global wave1
    global wave2
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
    menu=tk.OptionMenu((root), var, "心電圖", "頻率","傅立葉轉換","振幅")
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
        ele(ax6)
        tool(canvas1,root1)
        canvas1.draw()
    elif(var.get()=="頻率"):
        root2=tk.Tk()
        fig2=Figure()
        canvas2=FigureCanvasTkAgg(fig2,master=root2)
        canvas2.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        ax7=fig2.add_subplot()
        tool(canvas2,root2)  
        tbu=tk.Button(root2,command=lambda:tb1(tbu,ax7,canvas2))
        tbu.pack()
        tb1(tbu,ax7,canvas2)


    
root=tk.Tk()
fig=Figure()

ax1=fig.add_subplot()
ax2=fig.add_subplot()
ax3=fig.add_subplot()

ax1.set_position([0.1,0.7,0.8,0.2])
ax2.set_position([0.1,0.4,0.8,0.2])
ax3.set_position([0.1,0.1,0.8,0.2])





canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)


var=tk.StringVar(root)
tb=tk.Button(root,command=lambda:tb1(tb,ax2,canvas))
tb.place(relx=1.0,rely=0.0,anchor="ne")
men()
tool(canvas,root)



ele(ax1)
cha(wavein)
tb1(tb,ax2,canvas)






canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tk.mainloop()