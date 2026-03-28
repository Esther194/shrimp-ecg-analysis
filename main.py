import tkinter as tk
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib Demo')

        # create a 心電圖
        a=pd.read_excel("data.xlsx")
        fig=plt.figure()
        ax=fig.add_subplot()
        begin,end=0,630#開始結束時間
        
        e=0
        wavein=0,0
        waveout=0,0
        for i in range(begin,end):
            y1=a.iat[i,0]
            y2=a.iat[i+1,0]
            xpoints=np.array([(i/1000),((i+1)/1000)])
            ypoints=np.array([y1,y2])
            
            
            if(y2>0.01):
                ax.plot(xpoints,ypoints,marker='o',linewidth='0.5',color='k')
                wavein=(i/1000),y1
            elif(y1<-0.04):
                f=(i+1)/1000
                if(e==0):
                    g=(i+1)/1000
                    e=e+1
                if((f-g)>0.008):
                    ax.plot(xpoints,ypoints,marker='o',linewidth='0.5',color='b')
                    e=0
                ax.plot(xpoints,ypoints,linewidth='0.5',color='k')
                
                
            else:
                ax.plot(xpoints,ypoints,linewidth='0.5',color='k')
        
        
        
        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(fig, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create the barchart
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



app = App()
app.mainloop()