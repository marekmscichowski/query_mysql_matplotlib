import requests
import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import mysql.connector

mydb = mysql.connector.connect(host='',database='',user='',password='')
mycursor = mydb.cursor(buffered=True)

SQL_Query = pd.read_sql_query(
"""SELECT ma.date as date, ref.index, sum(ma.marketcap) as marketcap FROM peratio.main ma
JOIN peratio.reference ref ON ma.ticker=ref.ticker
WHERE ma.date >= CURRENT_DATE - INTERVAL 21 DAY
and ma.date < IF(DEPRE_DATE is not null, DEPRE_DATE, '2099-01-01')
group by ref.index, ma.date; 
                """, mydb)

data = pd.DataFrame(SQL_Query)

# make market cap chart, normalized

data["date"] = data["date"].astype("|S")
data['date'] = data['date'].str.slice(start=5)

data1 = data[data['index'] == 'Fin']
data2 = data[data['index'] == 'Real']
data3 = data[data['index'] == 'Tech']

x = data2['date']

y = data1['marketcap'] / data1.marketcap.iloc[0]*100
z = data2['marketcap'] / data2.marketcap.iloc[0]*100
a = data3['marketcap'] / data3.marketcap.iloc[0]*100

fig, ax = plt.subplots(figsize=(8, 3))

im2 = plt.imread('watermark.png', format=None)
fig.figimage(im2, 40, 40, zorder=6, alpha=.4)

ax.plot(x, a, '-b', label='Tech',color ='c')
ax.plot(x, y, '-b', label='Fin',color = 'm')
ax.plot(x, z, '-b', label='Real',color = 'k')

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("${x:,.0f}"))

plt.title("index market cap performance normalized")
plt.ylabel('index market cap performance normalized')
plt.xlabel('date')
leg = ax.legend();
plt.gcf().subplots_adjust(bottom=0.15)

plt.savefig(os.path.join('/root/charts', "index_mcn.png"))
