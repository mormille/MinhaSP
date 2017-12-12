#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:36:16 2017

@author: luizhenriquemormille
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Initial Parameters
path = 'treated_data/'
state = 'sp_completo/'
uf = 'SP'
file1 = 'basico_float.csv'
file2 = 'domicilio_float.csv'
file3 = 'responsavel_float.csv'
#path to save the ending file
end_dir = 'clusterized_data/'

#Path to open the files
pathbase1 = path + state + uf + file1
pathbase2 = path + state + uf + file2
pathbase3 = path + state + uf + file3

df1 = pd.read_csv(pathbase1, sep = ";", encoding = 'latin-1')
df2 = pd.read_csv(pathbase2, sep = ";", encoding = 'latin-1')
df3 = pd.read_csv(pathbase3, sep = ";", encoding = 'latin-1')

df_1st_merge = pd.merge(df1, df2, on='Cod_setor')
df_final = pd.merge(df_1st_merge, df3, on='Cod_setor')

def final_df(drops, df):
    final = df
    for i in drops:
         final = final.drop(i, 1)
    return final

drops = ['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0']
df_final = final_df(drops, df_final)

df_final = df_final.dropna(axis=0, how='any')

#the model
kmeans = KMeans(n_clusters=6, n_init= 50, random_state=0).fit(df_final.loc[:, 'Situacao':'V052-092_pct':])

df_final['sc_mosaic'] = kmeans.labels_

#Plotting it in 2D
y = df_final['sc_mosaic']
X = df_final

plt.scatter(X[y==0]['V005_stz'], X[y==0]['V009_stz'], label='Class 1', c='red')
plt.scatter(X[y==1]['V005_stz'], X[y==1]['V009_stz'], label='Class 2', c='blue')
plt.scatter(X[y==2]['V005_stz'], X[y==2]['V009_stz'], label='Class 3', c='lightgreen')
plt.scatter(X[y==3]['V005_stz'], X[y==3]['V009_stz'], label='Class 4', c='yellow')
plt.scatter(X[y==4]['V005_stz'], X[y==4]['V009_stz'], label='Class 5', c='orange')
plt.scatter(X[y==5]['V005_stz'], X[y==5]['V009_stz'], label='Class 6', c='darkgreen')

plt.legend()
plt.xlabel('V001')
plt.ylabel('V008_pct')

# display
plt.show()

drops2 = ['Situacao', 'V001_stz_x', 'V002_stz', 'V003_stz',
       'V005_stz', 'V009_stz', 'dom_V002_stz', 'dom_V003/002_pct',
       'dom_V005/002_pct', 'dom_V006/002_pct', 'dom_V007/002_pct',
       'dom_V008/002_pct', 'dom_V012/002_pct', 'dom_V017/002_pct',
       'dom_V034/002_pct', 'dom_V035/002_pct', 'dom_V043/002_pct',
       'dom_V060/002_pct', 'dom_V061/002_pct', 'rsp2_V001_stz',
       'rsp2_V093_stz', 'V001_stz_y', 'V001_pct', 'V002-009_sum',
       'V002-009_pct', 'V010-021_stz', 'V010-021_pct', 'V022-036_stz',
       'V022-036_pct', 'V037-051_stz', 'V037-051_pct', 'V052-092_stz',
       'V052-092_pct']

df_clusters = final_df(drops2, df_final)

#if there is any other attribute to merge with the dbf file
#now is the time to do it

merge_table_path = 'treated_data/sp_completo/SPbasico_completo.csv'
merge_table = pd.read_csv(merge_table_path, sep = ";", encoding = 'latin-1')
df_clusters_plus = pd.merge(df_clusters, merge_table[['Cod_setor','V009']], on='Cod_setor')

df_clusters_plus['CD_GEOCODI'] = df_clusters_plus['Cod_setor']

path_end1 = end_dir + uf + '/' + uf + '_clusterized.csv'
path_end2 = end_dir + uf + '/' + uf + '_sc_clusters.csv'

df_final.to_csv(path_end1, sep=';', encoding='latin-1')
df_clusters.to_csv(path_end2, sep=';', encoding='latin-1')





