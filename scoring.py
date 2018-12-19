#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jflores
"""

import pandas as pd
import matplotlib.pyplot as plt

sc=pd.read_csv("scoring.csv")

sc=sc[["playerID","yearID","AB","H"]]
#ADD column AVG (batting percentage)
sc.loc[sc['AB'] != 0, 'AVG'] = sc['H']/sc['AB']
#REMOVE people with less than 502 appearances per specification
sc.loc[sc['AB'] == 0, 'AVG'] = -1
data1=sc[sc.AVG!=-1]
sc.loc[sc['AB'] <502, 'AVG'] = -1
data1=sc[sc.AVG!=-1]

#REMOVE AVG less than zero and greater than 1
sc.loc[sc['AVG'] <=0, 'AVG'] = -1
sc.loc[sc['AVG'] >1, 'AVG'] = -1
data1=sc[sc.AVG!=-1]



data1=data1.sort_index(by=['playerID', 'yearID'])

#dist=pd.DataFrame()
#dist["yearID"]=data1['yearID']
#dist=dist.sort_index(by='yearID')

meandistribution=data1.groupby('yearID')["AVG"].mean()
meandistribution = meandistribution.reset_index()
meandistribution = meandistribution.rename(columns={'AVG': 'mean'})

mediandistribution=data1.groupby('yearID')["AVG"].median()
mediandistribution = mediandistribution.reset_index()
mediandistribution = mediandistribution.rename(columns={'AVG': 'median'})

stddistribution=data1.groupby('yearID')["AVG"].std()
stddistribution = stddistribution.reset_index()
stddistribution = stddistribution.rename(columns={'AVG': 'std'})

maxs=data1.groupby('yearID')["AVG"].max()
maxs = maxs.reset_index()
maxs = maxs.rename(columns={'AVG': 'max'})

mins=data1.groupby('yearID')["AVG"].min()
mins = mins.reset_index()
mins = mins.rename(columns={'AVG': 'min'})

modedistribution=data1.groupby('yearID')["AVG"].agg(lambda x:x.value_counts().index[0])
modedistribution = modedistribution.reset_index()
modedistribution = modedistribution.rename(columns={'AVG': 'mode'})

#plt.plot( 'yearID', 'mean', data=meandistribution, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
plt.plot( 'yearID', 'mean', data=meandistribution,color='red')
#plt.plot( 'yearID', 'median', data=mediandistribution,color='blue')
#plt.plot( 'yearID', 'std', data=stddistribution,color='blue')
plt.plot( 'yearID', 'max', data=maxs,color='orange')
plt.plot( 'yearID', 'min', data=mins,color='yellow')
#plt.plot( 'yearID', 'mode', data=modedistribution,color='brown')
plt.xlabel ('YEAR')
plt.ylabel ('AVG')
plt.title ('AVG BY YEAR')
plt.legend()





maxidx=data1.loc[data1.groupby("yearID")["AVG"].idxmax()]
master=pd.read_csv("Master.csv")

result = pd.merge(maxidx[['playerID','yearID',  'AVG', ]],
                 master[['playerID','nameFirst', 'nameLast', 'birthYear']],
                 on='playerID', 
                 how='left')
result=result[result.yearID>1979]
result["AGE"]=result.yearID-result.birthYear
result["NAME"]=result.nameFirst+" "+ result.nameLast
result = result[['yearID', 'NAME', 'AVG', 'AGE']]
result = result.rename(columns={'yearID': 'YEAR'})
print(result.to_string())




data1=data1.sort_index(by=['playerID', 'yearID'])
data1["season"]=data1.groupby('playerID').cumcount()+1
pivot1=pd.pivot_table(data1,index='playerID', columns='season', values='AVG')
pivotT=pivot1.T
res=pd.DataFrame()
res["mean"]=pivotT.mean(axis=1)
res['season'] = pivotT.index
plt.plot( 'season', 'mean', data=res,color='red')
plt.xlabel ('SEASON')
plt.ylabel ('AVG')
plt.title ('AVG BY SEASON')

