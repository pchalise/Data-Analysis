import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
from sklearn import linear_model
import csv
import networkx as nx

import seaborn as sns

#converting excel to csv
read_file1 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/data.xlsx')
read_file1.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/data.csv', index = None, header=True)

read_file2 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/dev.xlsx')
read_file2.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/dev.csv', index = None, header=True)

#editing csv
new_df1 = (read_file1.dropna())
new_df1.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/data_clean.csv', index = None, header=True)

new_df2 = (read_file2.dropna())
new_df2.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/dev_clean.csv', index = None, header=True)

#merging csv
new_df3 = new_df2.merge(new_df1, how='inner', on=None, left_on="Country_Code", right_on="Country_Code")
new_df3.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/final_data.csv', index = None, header=True)

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
print(new_df3)

#scatterplot
x = new_df3.TFR.values
y = new_df3.Life_Expectancy.values
slope, intercept, R, p, SE = stats.linregress(x,y)

sns.scatterplot('TFR', 'Life_Expectancy', data=new_df3, hue='Income_Group')
#plt.plot(x, y, 'o')
plt.plot(x, intercept + slope*x, 'r')
plt.xlabel('Total Fertility Rate')
plt.ylabel('Female Life Expectancy')
plt.title('Relationship between Female TFR and Life Expectancy')
plt.show()

#correlation
print("")
print("Simple Linear Regression Results:")
print("Slope = ",round(slope,3))
print("Y Intercept = ",round(intercept,3))
print("Correlation Coefficient (R) = ",round(R,3))
print("p-value = {:.3e}".format(p))
print("Standard Error = ",round(SE,3))

# histogram of the TFR
new_df3.TFR.plot(kind='hist', edgecolor='black')
plt.title('TFR')
plt.xlabel('Number')
plt.ylabel('Frequency')
#plt.show()

# histogram of the Life Expectancy
new_df3.Life_Expectancy.plot(kind='hist', edgecolor='black')
plt.title('Life Expectancy')
plt.xlabel('Number')
plt.ylabel('Frequency')
#plt.show()

# histogram of the Employment
new_df3.Employment.plot(kind='hist',edgecolor='black')
plt.title('Employment')
plt.xlabel('Number')
plt.ylabel('Frequency')
#plt.show()

#simple linear regression prediction
If_TFR = 3
print("")
print ('Predicted Life Expectancy with the simple model = ',intercept + slope * If_TFR)

#multiple regression
X = new_df3[['TFR','Employment']]
Y = new_df3['Life_Expectancy']
regr = linear_model.LinearRegression()
regr.fit(X, Y)
# prediction with sklearn
If_TFR = 3
If_Employment = 0
print("")
print ('Predicted Life Expectancy with the new model= ', regr.predict([[If_TFR, If_Employment]]))

# with statsmodels
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
print_model = model.summary()
print("")
#print("Multiple Linear Regression Results:")
#print(print_model)

#3d plot
