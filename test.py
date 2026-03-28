import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
"""import pandas as pd
import matplotlib.pyplot as plt
import numpy as np"""
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

e=1#週期頻率變化按鈕
def tb1():
    global e
    tb2=["週期","頻率"]
    tb["text"]=tb2[e%2]
    e=e+1
    
root=tk.Tk()
fig=Figure(figsize=(5,4),dpi=100)
ax1=fig.add_subplot(111)
ax1.plot([1,2],[10,15])
ax2=fig.add_subplot(211)
ax2.plot([1,2],[10,15])
ax3=fig.add_subplot(311)
ax3.plot([1,2],[10,15])
ax3.set_position([0.1,0.7,0.8,0.3])
ax1.set_position([0.1,0.4,0.8,0.3])
ax2.set_position([0.1,0.1,0.8,0.3])
canvas=FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

"""ysb1=tk.Scrollbar(master=root,orient=tk.HORIZONTAL,command=ax1.yaxis.set)
ysb2=tk.Scrollbar(root,orient=tk.HORIZONTAL,command=ax2.yaxis.set)
ysb3=tk.Scrollbar(root,orient=tk.HORIZONTAL,command=ax3.yaxis.set)
ysb1.pack(side=tk.BOTTOM,fill=tk.Y)
ysb1.pack(side=tk.BOTTOM,fill=tk.Y)
ysb1.pack(side=tk.BOTTOM,fill=tk.Y)
ax1.xaxis.config(yscrollcommand=ysb1.set)
ax2.yaxis.config(yscrollcommand=ysb2.set)
ax3.yaxis.config(yscrollcommand=ysb3.set)
"""
tb=tk.Button(root,text="週期",command=tb1)
tb.place(relx=1.0,rely=0.0,anchor="ne")

var=tk.StringVar(root)
var.set("菜單")
menu=tk.OptionMenu((root), var, "心電圖", "頻率","傅立葉轉換","振幅")
menu.place(x=0,y=0)



tk.mainloop()
