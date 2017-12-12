#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 01:52:21 2017

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
file = 'Domicilio01_SP1.csv'
#pasta onde os arquivos serão salvos
end_dir = 'treated_data/'
#caminho completo para salvar os arquivos
path_end = end_dir + state + uf 

#carregando o arquivo
pathbase = path + state + file
domicilio = pd.read_csv(pathbase, sep = ";", encoding = 'latin-1')

non_used =['Situacao_setor', 'V001', 'V004',
       'V009', 'V010', 'V011',
       'V013', 'V014', 'V015', 'V016', 'V018', 'V019', 'V020',
       'V021', 'V022', 'V023', 'V024', 'V025', 'V026', 'V027', 'V028',
       'V029', 'V030', 'V031', 'V032', 'V033', 'V036',
       'V037', 'V038', 'V039', 'V040', 'V041', 'V042', 'V044',
       'V045', 'V046', 'V047', 'V048', 'V049', 'V050', 'V051', 'V052',
       'V053', 'V054', 'V055', 'V056', 'V057', 'V058', 'V059',
       'V062', 'V063', 'V064', 'V065', 'V066', 'V067', 'V068',
       'V069', 'V070', 'V071', 'V072', 'V073', 'V074', 'V075', 'V076',
       'V077', 'V078', 'V079', 'V080', 'V081', 'V082', 'V083', 'V084',
       'V085', 'V086', 'V087', 'V088', 'V089', 'V090', 'V091', 'V092',
       'V093', 'V094', 'V095', 'V096', 'V097', 'V098', 'V099', 'V100',
       'V101', 'V102', 'V103', 'V104', 'V105', 'V106', 'V107', 'V108',
       'V109', 'V110', 'V111', 'V112', 'V113', 'V114', 'V115', 'V116',
       'V117', 'V118', 'V119', 'V120', 'V121', 'V122', 'V123', 'V124',
       'V125', 'V126', 'V127', 'V128', 'V129', 'V130', 'V131', 'V132',
       'V133', 'V134', 'V135', 'V136', 'V137', 'V138', 'V139', 'V140',
       'V141', 'V142', 'V143', 'V144', 'V145', 'V146', 'V147', 'V148',
       'V149', 'V150', 'V151', 'V152', 'V153', 'V154', 'V155', 'V156',
       'V157', 'V158', 'V159', 'V160', 'V161', 'V162', 'V163', 'V164',
       'V165', 'V166', 'V167', 'V168', 'V169', 'V170', 'V171', 'V172',
       'V173', 'V174', 'V175', 'V176', 'V177', 'V178', 'V179', 'V180',
       'V181', 'V182', 'V183', 'V184', 'V185', 'V186', 'V187', 'V188',
       'V189', 'V190', 'V191', 'V192', 'V193', 'V194', 'V195', 'V196',
       'V197', 'V198', 'V199', 'V200', 'V201', 'V202', 'V203', 'V204',
       'V205', 'V206', 'V207', 'V208', 'V209', 'V210', 'V211', 'V212',
       'V213', 'V214', 'V215', 'V216', 'V217', 'V218', 'V219', 'V220',
       'V221', 'V222', 'V223', 'V224', 'V225', 'V226', 'V227', 'V228',
       'V229', 'V230', 'V231', 'V232', 'V233', 'V234', 'V235', 'V236',
       'V237', 'V238', 'V239', 'V240', 'V241', 'Unnamed: 243']

def final_df(drops, df):
    final = df
    for i in drops:
         final = final.drop(i, 1)
    return final

domicilio01 = final_df(non_used, domicilio)
domicilio02 = domicilio01.dropna(axis=0, how='any')

def standardize(column):
    if column.dtype == 'O':
        column = pd.to_numeric(column.str.replace(',','.'), errors='force')
    scaler = preprocessing.StandardScaler()
    fit = scaler.fit(column)
    stz_column = fit.transform(column)
    return stz_column

domicilio02['dom_V002_stz'] = standardize(domicilio02['V002'])

base = 'V002'

bins_v002 = [1, 100, 200, 300, 500, 3000]
label_v002 = ['1 - 100', '101 - 200', '201 - 300', '301 - 500', 'mais de 500']

faixas_1 = [-1,0,0.1,1]
legenda_1 = ['0% das pessoas', '1% - 10%', '10% - 100%']

faixas_2 = [-1,0.1,0.25,0.5,1]
legenda_2 = ['0% - 10%', '11% - 25%','26% - 50%','51% - 100%']

faixas_3 = [-1,0.25,0.5, 0.75, 1]
legenda_3 = ['0% - 25%','26% - 50%','51% - 75%','76% - 100%']

faixas_4 = [-1,0.5,0.75,0.9999999999,1]
legenda_4 = ['0% - 50%', '51% - 75%','76% - 99%','100% das pessoas']

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

domicilio02['dom_V002_bin'] = bins(domicilio, 'V002', bins_v002, label_v002)

domicilio02['dom_V003/002_pct'], domicilio02['dom_V003/002_bin'] = pct_bin(domicilio02,'V003', faixas_3, legenda_3, base)
domicilio02['dom_V005/002_pct'], domicilio02['dom_V005/002_bin'] = pct_bin(domicilio02,'V005', faixas_3, legenda_3, base)
domicilio02['dom_V006/002_pct'], domicilio02['dom_V006/002_bin'] = pct_bin(domicilio02,'V006', faixas_3, legenda_3, base)
domicilio02['dom_V007/002_pct'], domicilio02['dom_V007/002_bin'] = pct_bin(domicilio02,'V007', faixas_3, legenda_3, base)
domicilio02['dom_V008/002_pct'], domicilio02['dom_V008/002_bin'] = pct_bin(domicilio02,'V008', faixas_3, legenda_3, base)

domicilio02['dom_V012/002_pct'], domicilio02['dom_V012/002_bin'] = pct_bin(domicilio02,'V012', faixas_4, legenda_4, base)
domicilio02['dom_V017/002_pct'], domicilio02['dom_V017/002_bin'] = pct_bin(domicilio02,'V017', faixas_4, legenda_4, base)
domicilio02['dom_V034/002_pct'], domicilio02['dom_V034/002_bin'] = pct_bin(domicilio02,'V034', faixas_4, legenda_4, base)
domicilio02['dom_V035/002_pct'], domicilio02['dom_V035/002_bin'] = pct_bin(domicilio02,'V035', faixas_4, legenda_4, base)
domicilio02['dom_V043/002_pct'], domicilio02['dom_V043/002_bin'] = pct_bin(domicilio02,'V043', faixas_4, legenda_4, base)

domicilio02['dom_V060/002_pct'], domicilio02['dom_V060/002_bin'] = pct_bin(domicilio02,'V060', faixas_2, legenda_2, base)
domicilio02['dom_V061/002_pct'], domicilio02['dom_V061/002_bin'] = pct_bin(domicilio02,'V061', faixas_2, legenda_2, base)

drop_float = ['V002', 'V003', 'V005', 'V006', 'V007', 'V008', 'V012',
       'V017', 'V034', 'V035', 'V043', 'V060', 'V061','dom_V003/002_bin',
       'dom_V002_bin','dom_V005/002_bin','dom_V006/002_bin', 
       'dom_V007/002_bin','dom_V008/002_bin','dom_V012/002_bin', 
       'dom_V017/002_bin','dom_V034/002_bin', 'dom_V035/002_bin',
       'dom_V043/002_bin','dom_V060/002_bin', 'dom_V061/002_bin']

drop_bin = ['V002', 'V003', 'V005', 'V006', 'V007', 'V008', 'V012',
       'V017', 'V034', 'V035', 'V043', 'V060', 'V061', 'dom_V002_stz',
       'dom_V003/002_pct','dom_V005/002_pct','dom_V006/002_pct',
       'dom_V007/002_pct','dom_V008/002_pct','dom_V012/002_pct',
       'dom_V017/002_pct','dom_V034/002_pct', 'dom_V035/002_pct',
       'dom_V043/002_pct','dom_V060/002_pct', 'dom_V061/002_pct',]

domicilio_final_float = domicilio02
domicilio_final_bin = domicilio02

for i in drop_float:
    domicilio_final_float = domicilio_final_float.drop(i, 1)
for i in drop_bin:
    domicilio_final_bin = domicilio_final_bin.drop(i, 1)
    
path_completo = path_end + "domicilio_completo.csv"
path_float = path_end + "domicilio_float.csv"
path_bin = path_end + "domicilio_bin.csv"

domicilio02.to_csv(path_completo, sep=';', encoding='latin-1')
domicilio_final_float.to_csv(path_float, sep=';', encoding='latin-1')
domicilio_final_bin.to_csv(path_bin, sep=';', encoding='latin-1')



