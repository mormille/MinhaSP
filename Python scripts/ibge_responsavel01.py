#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 11:21:55 2017

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
file1 = 'responsavel01_SP2.csv'
file2 = 'responsavel02_SP2.csv'
#pasta onde os arquivos serão salvos
end_dir = 'treated_data/'
#caminho completo para salvar os arquivos
path_end = end_dir + state + uf 

#carregando o arquivo
pathbase1 = path + state + file1
pathbase2 = path + state + file2
responsavel01 = pd.read_csv(pathbase1, sep = ",", encoding = 'latin-1')
responsavel02 = pd.read_csv(pathbase2, sep = ",", encoding = 'latin-1')


non_used1 = ["Situacao_setor","V093","V094","V095","V096","V097","V098","V099",
             "V100","V101","V102","V103","V104","V105","V106","V107","V108"]

non_used2 = ["Situacao_setor","V002","V003","V004","V005","V006","V007","V008","V009","V010","V011","V012","V013",
             "V014","V015","V016","V017","V018","V019","V020","V021","V022","V023","V024","V025","V026","V027",
             "V028","V029","V030","V031","V032","V033","V034","V035","V036","V037","V038","V039","V040","V041",
             "V042","V043","V044","V045","V046","V047","V048","V049","V050","V051","V052","V053","V054","V055",
             "V056","V057","V058","V059","V060","V061","V062","V063","V064","V065","V066","V067","V068","V069",
             "V070","V071","V072","V073","V074","V075","V076","V077","V078","V079","V080","V081","V082","V083",
             "V084","V085","V086","V087","V088","V089","V090","V091","V092","V094","V095","V096","V097","V098",
             "V099","V100","V101","V102","V103","V104","V105","V106","V107","V108","V109","V110","V111","V112",
             "V113","V114","V115","V116","V117","V118","V119","V120","V121","V122","V123","V124","V125","V126",
             "V127","V128","V129","V130","V131","V132","V133","V134","V135","V136","V137","V138","V139","V140",
             "V141","V142","V143","V144","V145","V146","V147","V148","V149","V150","V151","V152","V153","V154",
             "V155","V156","V157","V158","V159","V160","V161","V162","V163","V164","V165","V166","V167","V168",
             "V169","V170","V171","V172","V173","V174","V175","V176","V177","V178","V179","V180","V181","V182",
             "V183","V184","V185","V186","V187","V188","V189","V190","V191","V192","V193","V194","V195","V196",
             "V197","V198","V199","V200","V201","V202","V203","V204","V205","V206","V207","V208","V209","V210",
             "V211","V212","V213","V214","V215","V216"]

def final_df(drops, df):
    final = df
    for i in drops:
         final = final.drop(i, 1)
    return final

responsavel012 = final_df(non_used1, responsavel01)
responsavel022 = final_df(non_used2, responsavel02)

responsavel022['rsp2_V001'] = responsavel022['V001']
responsavel022['rsp2_V093'] = responsavel022['V093']

responsavel022 = responsavel022.drop('V001',1)
responsavel022 = responsavel022.drop('V093',1)

responsavel03 = pd.merge(responsavel012, responsavel022, on='Cod_setor')

responsavel_final = responsavel03.dropna(axis=0, how='any')

def standardize(column):
    if column.dtype == 'O':
        column = pd.to_numeric(column.str.replace(',','.'), errors='force')
    scaler = preprocessing.StandardScaler()
    fit = scaler.fit(column)
    stz_column = fit.transform(column)
    return stz_column

def bins(df, atributo, faixas, label):
    if df[atributo].dtype == 'O':
        df[atributo] = pd.to_numeric(df[atributo].str.replace(',','.'), errors='force')
    bins = pd.cut(df[atributo], faixas, labels = label)
    return bins

def pct_bin (df, atributo, faixas, label, base):
    if df[atributo].dtype == 'O':
        df[atributo] = pd.to_numeric(df[atributo].str.replace(',','.'), errors='force')
    pct = df[atributo]/df[base]
    bins = pd.cut(pct, faixas, labels = label)
    return pct, bins

def sum_pct_bin(df, init, final, faixas, label, basis):
    att_list = []
    for i in range(init, final+1):
        if len(str(i)) == 1:
            v = 'V00' + str(i)
            att_list.append(v)
        elif len(str(i)) == 2:
            v = 'V0'+ str(i)
            att_list.append(v)
        else:
            v = 'V'+ str(i)
            att_list.append(v)
    sum_col = 0
    for i in att_list:
        if df[i].dtype == 'O':
            df[i] = pd.to_numeric(df[i].str.replace(',','.'), errors='force')
        sum_col = sum_col + df[i]
    pct = sum_col/df[basis]
    bins = pd.cut(pct, faixas, labels = label)
    scaler = preprocessing.StandardScaler()
    fit = scaler.fit(sum_col)
    stz_col = fit.transform(sum_col)
    return stz_col, pct, bins


for i in list(responsavel_final.columns.values):
    if responsavel_final[i].dtype == 'O':
        responsavel_final[i] = pd.to_numeric(responsavel_final[i].str.replace(',','.'), errors='force')

responsavel_final =responsavel_final.dropna(axis=0, how='any')

faixa = [-1, 50, 125, 250, 2000]
label = ['0 - 50','51 - 125', '126 - 250', 'mais de 250']

responsavel_final['rsp2_V001_bin'] = bins(responsavel_final, 'rsp2_V001', faixa, label)
responsavel_final['rsp2_V001_stz'] = standardize(responsavel_final['rsp2_V001'])
responsavel_final['rsp2_V093_stz'] = standardize(responsavel_final['rsp2_V093'])
responsavel_final['V001_stz'] = standardize(responsavel_final['V001'])

base1 = 'V001'
base2 = 'rsp2_V001'

faixas_1 = [-1,0,0.1,1]
legenda_1 = ['0% das pessoas', '1% - 10%', '10% - 100%']

faixas_2 = [-1,0.1,0.25,0.5,1]
legenda_2 = ['0% - 10%', '11% - 25%','26% - 50%','51% - 100%']

faixas_3 = [-1,0.25,0.5, 0.75, 1]
legenda_3 = ['0% - 25%','26% - 50%','51% - 75%','76% - 100%']

faixas_4 = [-1,0.5,0.75,0.9999999999,1]
legenda_4 = ['0% - 50%', '51% - 75%','76% - 99%','100% das pessoas']

responsavel_final['V001_pct'], responsavel_final['V001_bin'] = pct_bin(responsavel_final, 'V001', faixas_3, legenda_3, base2)

responsavel_final['V002-009_sum'], responsavel_final['V002-009_pct'], responsavel_final['V002-009_bin'] = sum_pct_bin(responsavel_final, 2, 9, faixas_1, legenda_1, base1)
responsavel_final['V010-021_stz'], responsavel_final['V010-021_pct'], responsavel_final['V010-021_bin'] = sum_pct_bin(responsavel_final, 10, 21, faixas_2, legenda_2, base1)
responsavel_final['V022-036_stz'], responsavel_final['V022-036_pct'], responsavel_final['V022-036_bin'] = sum_pct_bin(responsavel_final, 22, 36, faixas_3, legenda_3, base1)
responsavel_final['V037-051_stz'], responsavel_final['V037-051_pct'], responsavel_final['V037-051_bin'] = sum_pct_bin(responsavel_final, 37, 51, faixas_3, legenda_3, base1)
responsavel_final['V052-092_stz'], responsavel_final['V052-092_pct'], responsavel_final['V052-092_bin'] = sum_pct_bin(responsavel_final, 52, 92, faixas_2, legenda_2, base1)


drop_float = ['V001', 'V002', 'V003', 'V004', 'V005', 'V006', 'V007',
       'V008', 'V009', 'V010', 'V011', 'V012', 'V013', 'V014', 'V015',
       'V016', 'V017', 'V018', 'V019', 'V020', 'V021', 'V022', 'V023',
       'V024', 'V025', 'V026', 'V027', 'V028', 'V029', 'V030', 'V031',
       'V032', 'V033', 'V034', 'V035', 'V036', 'V037', 'V038', 'V039',
       'V040', 'V041', 'V042', 'V043', 'V044', 'V045', 'V046', 'V047',
       'V048', 'V049', 'V050', 'V051', 'V052', 'V053', 'V054', 'V055',
       'V056', 'V057', 'V058', 'V059', 'V060', 'V061', 'V062', 'V063',
       'V064', 'V065', 'V066', 'V067', 'V068', 'V069', 'V070', 'V071',
       'V072', 'V073', 'V074', 'V075', 'V076', 'V077', 'V078', 'V079',
       'V080', 'V081', 'V082', 'V083', 'V084', 'V085', 'V086', 'V087',
       'V088', 'V089', 'V090', 'V091', 'V092', 'rsp2_V001', 'rsp2_V093',
       'V001_bin', 'V010-021_bin','V022-036_bin','V037-051_bin',
       'V052-092_bin', 'V002-009_bin', 'rsp2_V001_bin']

drop_bin = ['V001', 'V002', 'V003', 'V004', 'V005', 'V006', 'V007',
       'V008', 'V009', 'V010', 'V011', 'V012', 'V013', 'V014', 'V015',
       'V016', 'V017', 'V018', 'V019', 'V020', 'V021', 'V022', 'V023',
       'V024', 'V025', 'V026', 'V027', 'V028', 'V029', 'V030', 'V031',
       'V032', 'V033', 'V034', 'V035', 'V036', 'V037', 'V038', 'V039',
       'V040', 'V041', 'V042', 'V043', 'V044', 'V045', 'V046', 'V047',
       'V048', 'V049', 'V050', 'V051', 'V052', 'V053', 'V054', 'V055',
       'V056', 'V057', 'V058', 'V059', 'V060', 'V061', 'V062', 'V063',
       'V064', 'V065', 'V066', 'V067', 'V068', 'V069', 'V070', 'V071',
       'V072', 'V073', 'V074', 'V075', 'V076', 'V077', 'V078', 'V079',
       'V080', 'V081', 'V082', 'V083', 'V084', 'V085', 'V086', 'V087',
       'V088', 'V089', 'V090', 'V091', 'V092', 'rsp2_V001', 'rsp2_V093',
       'rsp2_V001_stz', 'rsp2_V093_stz', 'V001_stz', 'V001_pct',
       'V010-021_stz', 'V010-021_pct','V022-036_stz', 'V022-036_pct', 
       'V037-051_stz','V037-051_pct', 'V052-092_stz', 'V052-092_pct',]


responsavel_final_float = responsavel_final
responsavel_final_bin = responsavel_final

for i in drop_float:
    responsavel_final_float = responsavel_final_float.drop(i, 1)
for i in drop_bin:
    responsavel_final_bin = responsavel_final_bin.drop(i, 1)
    
path_completo = path_end + "responsavel_completo.csv"
path_float = path_end + "responsavel_float.csv"
path_bin = path_end + "responsavel_bin.csv"

responsavel_final.to_csv(path_completo, sep=';', encoding='latin-1')
responsavel_final_float.to_csv(path_float, sep=';', encoding='latin-1')
responsavel_final_bin.to_csv(path_bin, sep=';', encoding='latin-1')


























