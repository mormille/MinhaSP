#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 14:23:42 2017

@author: luizhenriquemormille
"""

import pandas as pd

#caminho para a pasta com os arquivos dos estados
path = 'treated_data/'
#estado que será processado
state1 = 'sp_capital/'
state2 = 'sp_interior/'
#a sigla do estado para colocar no arquivo final
uf1 = 'sp1'
uf2 = 'sp2'
#nome do arquivo Básico daquele estado
file1 = 'basico_float.csv'
file2 = 'domicilio_float.csv'
file3 = 'responsavel_float.csv'
#pasta onde os arquivos serão salvos
path_end = 'treated_data/sp_completo/SP'
#caminho completo para salvar os arquivos
 

#carregando o arquivo
pathbase_cap1 = path + state1 + uf1 + file1
pathbase_cap2 = path + state1 + uf1 + file2
pathbase_cap3 = path + state1 + uf1 + file3
pathbase_int1 = path + state2 + uf2 + file1
pathbase_int2 = path + state2 + uf2 + file2
pathbase_int3 = path + state2 + uf2 + file3

cap1 = pd.read_csv(pathbase_cap1, sep = ";", encoding = 'latin-1')
cap2 = pd.read_csv(pathbase_cap2, sep = ";", encoding = 'latin-1')
cap3 = pd.read_csv(pathbase_cap3, sep = ";", encoding = 'latin-1')
int1 = pd.read_csv(pathbase_int1, sep = ";", encoding = 'latin-1')
int2 = pd.read_csv(pathbase_int2, sep = ";", encoding = 'latin-1')
int3 = pd.read_csv(pathbase_int3, sep = ";", encoding = 'latin-1')

frames1 = [cap1, int1]
frames2 = [cap2, int2]
frames3 = [cap3, int3]

complete1 = pd.concat(frames1)
complete2 = pd.concat(frames2)
complete3 = pd.concat(frames3)

complete1 = complete1.drop('Unnamed: 0',1)
complete2 = complete2.drop('Unnamed: 0',1)
complete3 = complete3.drop('Unnamed: 0',1)

path_basico = path_end + "basico_float.csv"
path_domicilio = path_end + "domicilio_float.csv"
path_responsavel = path_end + "responsavel_float.csv"

complete1.to_csv(path_basico, sep=';', encoding='latin-1')
complete2.to_csv(path_domicilio, sep=';', encoding='latin-1')
complete3.to_csv(path_responsavel, sep=';', encoding='latin-1')