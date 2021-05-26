"""
Implementação de um Modelo Numérico para Solução de um Condensador Instalado na Unidade de Quixeré da Apodi

Código desenvolvido por:
Camilo Costa

Descrição Geral: Neste código foi implementado um modelo numérico para a solução da troca térmica em um condensador.
O modelo consiste do uso de coeficientes globais para região do condensado e do escoamento interno nos tubos. Para a
obtenção do fluxo de calor foi utilizado o método epsilon-NTU.

Modelo Físico: O trocador foi dividido em duas seções. A Seção 01 é a região mais acima onde o trocador recebe o
vapor saturado vindo da turbina e a Seção 02 fica mais abaixo onde o trocador recebe a água de refrigeração vindo da
torre de resfriamento.

Método de Solução Numérica: Para a solução do sistema linear criado foi implementado um método interativo afim de
avaliar a temperatura na saída do trocador validando a solução através da verificação do balanço de energia.

Versões:
v01: Lendo as variáveis e criando a matriz de vazão.
"""

"""Importando a Bibliotecas do Python e do CoolProp"""
import numpy as np
from CoolProp.CoolProp import PropsSI

"""Lendo as variáveis termodinâmicas e de operação da planta"""
termo_var = np.load(r'D:\Google Drive\UFC\Projeto APODI\Torre de Resfriamento\Códigos Computacionais\Tratamento dos '
                    r'Dados\Dados de Saída\Python\Dados.Cog.Trat_Sem.Vazao_v02.npy')

"""Inicializando as matrizes para todas as variáveis termodinâmicas"""
n_var = 10
[linD, colD] = termo_var.shape
T = np.zeros((linD, n_var))  # Inicializando a matriz das temperaturas
P = np.zeros((linD, n_var))  # Inicializando a matriz das pressões
h = np.zeros((linD, n_var))  # Inicializando a matriz das pressões
s = np.zeros((linD, n_var))  # Inicializando a matriz das entropia
m_dot = np.zeros((linD, n_var))  # Inicializando a matriz das vazões

"""Criando as classes para o condensador"""


class Cond:
    pass


Cond.T = np.zeros((linD, n_var))
Cond.P = np.zeros((linD, n_var))

"""Ajustando os dados para a leitura no PropsSI"""
Cond.T[:, 0] = termo_var[:, 6] + 273.15  # Temperatura da água condensada na saída do condensador [K]
Cond.T[:, 1] = termo_var[:, 10] + 273.15  # Temperatura da água de resfriamento na entrada 1 do condensador [K]
Cond.T[:, 2] = termo_var[:, 11] + 273.15  # Temperatura da água de resfriamento na entrada 2 do condensador [K]
Cond.T[:, 3] = termo_var[:, 12] + 273.15  # Temperatura da água de resfriamento na saída 1 do condensador [K]
Cond.T[:, 4] = termo_var[:, 13] + 273.15  # Temperatura da água de resfriamento na saída 2 do condensador [K]
Cond.P[:, 0] = termo_var[:, 1] * 1e3  # Pressão na entrada do condensador lado frio (água da torre de resfriamento) [Pa]
Cond.P[:, 1] = termo_var[:, 2] * 1e3  # Pressão na saída da torre direcionada para o condensador [Pa]
Cond.P[:, 2] = termo_var[:, 3] * 1e3  # Pressão interna no condensador lado quente (vapor-água condensada) [Pa]

"""Dados da Planta"""
# Caracteristicas geométricas do Condensador
A = 800  # Área de refrigeração [m²]
N_tubos = 2840  # Número de tubos
Esp_tubos = 0.0007  # Espessura dos tubos [m]
D_int = 0.02  # Diâmetro interno dos tubos [m]
D_ext = 0.0214  # Diâmetro externo dos tubos [m]
D_ext_casco = 2.4  # Diâmetro externo do casco [m]
D_int_casco = 2.22  # Diâmetro interno do casco [m]
D_vap = 1.016  # Diâmetro da passagem do vapor [m]
L = 4.562  # Comprimento de Troca [m]
S_L = 0.025  # Comprimento S_L arranjo escalonado [m]
S_T = 0.030  # Comprimento S_T arranjo escalonado [m]

# Propriedades termofísicas da tubulação
k_tubos = 16.2  # Condutividade térmica dos tubos [W/mK]

# Vazões de Projeto
m_dot_condensado = 0.01  # Vazão volumétrica de projeto do condensado [m³/s]
m_dot_agua = 0.72  # Vazão volumétrica de projeto da água [m³/s]

# Eficiencia isentrópica da turbina
eta_ise = 0.7337
