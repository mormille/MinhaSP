#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:31:22 2017

@author: luizhenriquemormille
"""

import pandas as pd
#import numpy as np
from sklearn import preprocessing
#import matplotlib.pyplot as plt

pathbase1 = 'treated_data/sp_capital/SP_FAV.csv'
pathbase2 = 'raw_data/sp_capital/SP_MR.csv'

df = pd.read_csv(pathbase1, sep = ",", encoding = 'latin-1',error_bad_lines=False)
df2 = pd.read_csv(pathbase2, sep = ",", encoding = 'latin-1',error_bad_lines=False)

def favela(row):
    if pd.isnull(row["count"]) == True:
        val = 0
    else:
        val = 1
    return val

def morador_rua(row):
    if pd.isnull(row["count"]) == True:
        val = 0
    else:
        val = row["count"]
    return val

df['Flag_favela'] = df.apply(favela, axis=1)
df2['Moradores_de_rua'] = df2.apply(morador_rua, axis=1)

df['Cod_setor'] = df['CD_GEOCODI']
df2['Cod_setor'] = df2['CD_GEOCODI']

def standardize(column):
    if column.dtype == 'O':
        column = pd.to_numeric(column.str.replace(',','.'), errors='force')
    scaler = preprocessing.StandardScaler()
    fit = scaler.fit(column)
    stz_column = fit.transform(column)
    return stz_column

df2["Moradores_de_rua_stz"] = standardize(df2["Moradores_de_rua"])

drops = ['Unnamed: 0', 'ID', 'CD_GEOCODI', 'TIPO', 'CD_GEOCODB', 'NM_BAIRRO',
       'CD_GEOCODS', 'NM_SUBDIST', 'CD_GEOCODD', 'NM_DISTRIT',
       'CD_GEOCODM', 'NM_MUNICIP', 'NM_MICRO', 'NM_MESO', 'sumAREA_m',
       'count']

drops2 = ['Unnamed: 0', 'ID', 'CD_GEOCODI', 'TIPO', 'CD_GEOCODB', 'NM_BAIRRO',
       'CD_GEOCODS', 'NM_SUBDIST', 'CD_GEOCODD', 'NM_DISTRIT',
       'CD_GEOCODM', 'NM_MUNICIP', 'NM_MICRO', 'NM_MESO', 'sumID',
       'sumLONGITU', 'sumLATITUD', 'sumIDADE', 'sumNUMERO_', 'count',"Moradores_de_rua"]

df = df.drop(drops,1)
df2 = df2.drop(drops2,1)


df.to_csv('treated_data/sp_capital/SC_SP_FAV.csv', sep = ";", encoding = 'latin-1')
df2.to_csv('treated_data/sp_capital/SC_SP_MR.csv', sep = ";", encoding = 'latin-1')


