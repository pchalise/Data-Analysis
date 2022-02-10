import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

read_file1 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/data.xlsx')
read_file2 = pd.read_excel (r'/Users/chaliseparik/Desktop/CodeSoka/dev.xlsx')
new_df1 = (read_file1.dropna())
new_df2 = (read_file2.dropna())
new_df3 = new_df2.merge(new_df1, how='inner', on=None, left_on="Country_Code", right_on="Country_Code")

#threshold metrics of high and ok
bad_TFR = new_df3['TFR'].quantile(q=0.8)
bad_Life_Expectancy = new_df3['Life_Expectancy'].quantile(q=0.2)
bad_Employment = new_df3['Employment'].quantile(q=0.2)

print(bad_TFR)
#print(bad_Life_Expectancy)
#print(bad_Employment)

high_TFR_list=[]
ok_TFR_list=[]
i = 0
while i < len(new_df3.index):
    data = new_df3['TFR'][i]
    if data > bad_TFR:
        high_TFR_list.append(new_df3['Country_Name'][i])
    else:
        ok_TFR_list.append(new_df3['Country_Name'][i])
    i+=1
#print(high_TFR_list)
#print(ok_TFR_list)

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
        col = 'skyblue'
        color.append(col)
    i+=1
new_df3['colors']= color
#print(new_df3)
#new_df3.to_csv (r'/Users/chaliseparik/Desktop/CodeSoka/color_coded_final_data.csv', index = None, header=True)

#high vs ok cluster
data = []
i = 0
while i < len(high_TFR_list):
    j = 0
    while j < len(high_TFR_list):
        dt = [high_TFR_list[i],high_TFR_list[j]]
        data.append(dt)
        j+=1
    i+=1

i = 0
while i < len(ok_TFR_list):
    j = 0
    while j < len(ok_TFR_list):
        dt = [ok_TFR_list[i],ok_TFR_list[j]]
        data.append(dt)
        j+=1
    i+=1
dff = pd.DataFrame(data)
#print(dff)

G = networkx.from_pandas_edgelist(dff, 0, 1)
pos = networkx.spring_layout(G, k=0.15, iterations=20)
networkx.draw_networkx(G, pos = pos, node_color = new_df3['colors'], with_labels = False, node_size = 50)
plt.show()

#a proper visualization

#defining neighbors
data = []
i = 0
while i < len(new_df3.index):
    j = 0
    while j < len(new_df3.index):
        #set x and y to define a relationship
        x = new_df3['TFR'][i]
        y = new_df3['TFR'][j]
        if abs(x-y)<=0.1:
            dt = [new_df3['Country_Name'][i],new_df3['Country_Name'][j]]
            data.append(dt)
        j+=1
    i += 1
df = pd.DataFrame(data)
#print(df)

#to see what's in the column:
#print(new_df3['Income_Group'].unique())

#merging files with unequal number of rows is also possible :
#ddf = df.merge(new_df3, how='inner', on=None, left_on=0, right_on="Country_Name")
#print(ddf)

#network viz using networkx
G = networkx.from_pandas_edgelist(df, 0, 1)
pos = networkx.spring_layout(G, k=0.15, iterations=20)
networkx.draw_networkx(G, pos = pos, node_color = new_df3['colors'], with_labels = False, node_size = 50)
plt.show()

#network viz using bokeh
G = networkx.from_pandas_edgelist(df, 0, 1)

title = 'TFR – Life Expectancy Relationship'
HOVER_TOOLTIPS = [("Character","@index")]
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10, 10), y_range=Range1d(-10, 10), title=title)
# https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
network_graph = from_networkx(G, networkx.spring_layout, scale=50, center=(0, 0))

network_graph.node_renderer.glyph = Circle(size=5, fill_color='skyblue')
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

plot.renderers.append(network_graph)

show(plot)
