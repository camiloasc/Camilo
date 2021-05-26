"""
Implementação de um Modelo Numérico para Solução de um Condensador Instalado na Unidade de Quixeré da Apodi

Código desenvolvido por:
Camilo Costa

Descrição Geral: Código para ler os dados do Matlab

Versões:
v01: Implementando a leitura.
"""

"""Leitura dos Dados"""
import scipy.io
import numpy as np

data = scipy.io.loadmat(r'data\data.mat')
termo_var = data['S2']
np.save(r'data\data.npy', termo_var)
