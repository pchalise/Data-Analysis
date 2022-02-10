import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

read_file1 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/data.xlsx')
read_file2 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/dev.xlsx')
new_df1 = (read_file1.dropna())
new_df2 = (read_file2.dropna())
new_df3 = new_df2.merge(new_df1, how='inner', on=None, left_on="Country_Code", right_on="Country_Code")

#color coding
i = 0
color = []
while i < len(new_df3.index):
    if new_df3['Income_Group'][i] == 'Low income':
        col = 'red'
        color.append(col)
    elif new_df3['Income_Group'][i] == 'High income':
        col = 'green'
        color.append(col)
    else:
        col = 'blue'
        color.append(col)
    i+=1
new_df3['colors']= color

data = []
i = 0
while i < len(new_df3):
    dt = [new_df3['TFR'][i],new_df3['Employment'][i]]
    data.append(dt)
    i+=1

X = data
Y = new_df3['Life_Expectancy']

df=pd.DataFrame(X,columns=['TFR','Employment'])
df['Life_Expectancy']=pd.Series(Y)

Regressor = LinearRegression()
Regressor.fit(X,Y)

## Prepare the data for Visualization

x_surf, y_surf = np.meshgrid(np.linspace(df.TFR.min(), df.TFR.max(), 100),np.linspace(df.Employment.min(), df.Employment.max(), 100))
onlyX = pd.DataFrame({'TFR': x_surf.ravel(), 'Employment': y_surf.ravel()})
fittedY=Regressor.predict(onlyX)

## convert the predicted result in an array
fittedY=np.array(fittedY)

fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['TFR'],df['Employment'],df['Life_Expectancy'],c=new_df3['colors'], marker='o', alpha=0.5)
ax.plot_surface(x_surf,y_surf,fittedY.reshape(x_surf.shape), color='b', alpha=0.3)
ax.set_xlabel('TFR')
ax.set_ylabel('Employment')
ax.set_zlabel('Life Expectancy')
plt.show()
