#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 23:23:04 2017

@author: luizhenriquemormille
"""

import pandas as pd
from sklearn import preprocessing

#caminho para a pasta com os arquivos dos estados
path = 'raw_data/'
#estado que será processado
state = 'sp_interior/' 
#a sigla do estado para colocar no arquivo final
uf = 'sp2'
#nome do arquivo Básico daquele estado
file = 'Basico_SP2.csv'
#pasta onde os arquivos serão salvos
end_dir = 'treated_data/'
#caminho completo para salvar os arquivos
path_end = end_dir + state + uf 

#carregando o arquivo
pathbase = path + state + file
basico = pd.read_csv(pathbase, sep = ";", encoding = 'latin-1')

non_used = ['Cod_Grandes Regiões','Nome_Grande_Regiao','Cod_meso','Nome_da_meso',
 'Cod_micro','Nome_da_micro','Cod_RM','Nome_da_RM','Cod_distrito','Nome_do_distrito',
 'Cod_subdistrito','Nome_do_subdistrito','Cod_bairro','Nome_do_bairro',
 'Tipo_setor','V004','V006','V010','V007','V008','V011','V012','Unnamed: 33']

def final_df(drops, df):
    final = df
    for i in drops:
         final = final.drop(i, 1)
    return final

basico01 = final_df(non_used, basico)

def situacao_setor(row):
    if row["Situacao_setor"] == 1:
        val = 1
    elif row["Situacao_setor"] == 2:
        val = 2
    elif row["Situacao_setor"] == 3:
        val = 3
    elif row["Situacao_setor"] == 4:
        val = 4
    elif row["Situacao_setor"] == 5:
        val = 4
    elif row["Situacao_setor"] == 6:
        val = 4
    else:
        val = 4
    return val

basico01['Situacao'] = basico01.apply(situacao_setor, axis=1)
basico01 = basico01.drop('Situacao_setor', 1)

basico02 = basico01.dropna(axis=0, how='any')

def standardize(column):
    if column.dtype == 'O':
        column = pd.to_numeric(column.str.replace(',','.'), errors='force')
    scaler = preprocessing.StandardScaler()
    fit = scaler.fit(column)
    stz_column = fit.transform(column)
    return stz_column

basico02['V001_stz'] = standardize(basico02['V001'])
basico02['V002_stz'] = standardize(basico02['V002'])
basico02['V003_stz'] = standardize(basico02['V003'])
basico02['V005_stz'] = standardize(basico02['V005'])
basico02['V009_stz'] = standardize(basico02['V009'])


bins_v001 = [1, 50, 150, 200, 300, 1000]
label_v001 = ['1 - 50', '51 - 150', '151 - 200', '201 -300', 'mais de 350']

bins_v002 = [1, 100, 500, 1000, 2000, 4000]
label_v002 = ['1 - 100', '101 - 500', '501 - 1000', '1001 -2000', 'mais de 2000']

bins_v003 = [0, 2, 3, 4, 10]
label_v003 = ['1 - 2 pessoas', '2 - 3 pessoas', '3 - 4 pessoas', 'mais de 4']

bins_v005 = [0, 1250, 2500, 5000, 10000, 100000]
label_v005 = ['0 - 1250', '1251 - 2500', '2501 - 5000', '5000 - 10000', 'mais de 10000']

bins_v009 = [0, 400, 800, 1500, 3000, 100000]
label_v009 = ['0 - 400', '401 - 800', '801 - 1500', '1500 - 3000', 'mais de 3000']

def bins(df, atributo, faixas, label):
    if df[atributo].dtype == 'O':
        df[atributo] = pd.to_numeric(df[atributo].str.replace(',','.'), errors='force')
    bins = pd.cut(df[atributo], faixas, labels = label)
    return bins

basico02['V001_bin'] = bins(basico02, 'V001', bins_v001, label_v001)
basico02['V002_bin'] = bins(basico02, 'V002', bins_v002, label_v002)
basico02['V003_bin'] = bins(basico02, 'V003', bins_v003, label_v003)
basico02['V005_bin'] = bins(basico02, 'V005', bins_v005, label_v005)
basico02['V009_bin'] = bins(basico02, 'V009', bins_v009, label_v009)

basico02['Situacao_bin'] = basico02['Situacao'].astype(str)

drop_float = ['Cod_UF','Nome_da_UF ', 'Cod_municipio', 'Nome_do_municipio',
 'V001', 'V002', 'V003', 'V005', 'V009', 'Situacao_bin',
 'V001_bin', 'V002_bin', 'V003_bin', 'V005_bin', 'V009_bin']

drop_bin = ['Cod_UF','Nome_da_UF ','Cod_municipio','Nome_do_municipio',
 'V001','V002','V003','V005','V009','Situacao',
 'V001_stz','V002_stz','V003_stz','V005_stz','V009_stz']

basico_final_float = basico02
basico_final_bin = basico02

for i in drop_float:
    basico_final_float = basico_final_float.drop(i, 1)
for i in drop_bin:
    basico_final_bin = basico_final_bin.drop(i, 1)
    
path_completo = path_end + "basico_completo.csv"
path_float = path_end + "basico_float.csv"
path_bin = path_end + "basico_bin.csv"

basico02.to_csv(path_completo, sep=';', encoding='latin-1')
basico_final_float.to_csv(path_float, sep=';', encoding='latin-1')
basico_final_bin.to_csv(path_bin, sep=';', encoding='latin-1')










