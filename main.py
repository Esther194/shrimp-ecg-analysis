import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
a=pd.read_excel("data.xlsx")
fig=plt.figure()
ax=fig.add_subplot()
begin,end=0,630
for i in range(begin,end):
    b=a.iat[i,0]
    c=a.iat[i+1,0]
    xpoints=np.array([(i/1000),((i+1)/1000)])
    ypoints=np.array([b,c])
    ax.plot(xpoints,ypoints,linewidth='0.5',color='k')
plt.show()