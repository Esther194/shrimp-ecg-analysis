import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

a=pd.read_excel("data.xlsx")
fig=plt.figure()
ax=fig.add_subplot()
begin,end=500,630
e=0#出波點計數器
f=0#反向推算的標的
w=0#波的個數
wavein,waveout=[],[]#入波出波時間
for i in range(begin,end):
    b=a.iat[i,0]#第一(i)筆資料
    c=a.iat[i+1,0]#第二(i+1)筆資料
    xpoints=np.array([(i/1000),((i+1)/1000)])
    ypoints=np.array([b,c])
    if(c>0.01 and i> f+10):
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
                xpoints=np.array([(f/1000),((f-1)/1000)])
                ypoints=np.array([b,c])
                ax.plot(xpoints,ypoints,marker='o',linewidth='0.5',color='b')
                e=1
                waveout.append(f/1000)
                w=w+1
                
        
    else:
        ax.plot(xpoints,ypoints,linewidth='0.5',color='k')
print("共有",w,"個波")
print("週期",(wavein[w-1]-wavein[0])/w,"次/秒")
print("頻率",w/(wavein[w-1]-wavein[0]),"秒/次")
    
plt.show()