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
v01: Lendo as variáveis termofísicas da planta de cogeração.
v02: Calculando as vazões da planta.
v03: Lendo os dados tratados agora com a freq. da bomba de alta da caldeira.
"""
"Importando as bibliotecas"
import numpy as np
from CoolProp.CoolProp import PropsSI

"Lendo as variáveis termodinâmicas e de operação da planta"
termo_var = np.load('data/data.npy')

"Inicializando as matrizes para todas as variáveis termodinâmicas"
n_var = 10
[linD, colD] = termo_var.shape
T = np.zeros((linD, n_var))  # Inicializando a matriz das temperaturas
P = np.zeros((linD, n_var))  # Inicializando a matriz das pressões
h = np.zeros((linD, n_var))  # Inicializando a matriz das entalpia
s = np.zeros((linD, n_var))  # Inicializando a matriz das entropia
rho = np.zeros((linD, n_var))  # Inicializando a matriz das densidades
m_dot = np.zeros((linD, n_var))  # Inicializando a matriz das vazões mássicas
V_dot = np.zeros((linD, n_var))  # Inicializando a matriz das vazões volumétricas
H = np.zeros((linD, n_var))  # Inicializando a matriz das alturas de elevações
F = np.zeros((linD, n_var))  # Inicializando a matriz das frequencias dos motores

"Ajustando os dados para a leitura no PropsSI"
T[:, 4] = termo_var[:, 12] + 273.15  # Temperatura da água de resfriamento na saída 01 do condensador [K]
T[:, 2] = termo_var[:, 6] + 273.15  # Temperatura da água condensada na saída do condensador [K]
P[:, 6] = termo_var[:, 2] * 1e3  # Pressão na saída da torre direcionada para o condensador [Pa]
F[:, 0] = termo_var[:, 19]  # Frequencia da bomba 01 de re-circulação da torre
F[:, 1] = termo_var[:, 20]  # Frequencia da bomba 02 de re-circulação da torre
F[:, 2] = termo_var[:, 23]  # Frequencia da bomba de alta da caldeira
F[:, 3] = termo_var[:, 21]  # Frequencia do ventilador 01
F[:, 4] = termo_var[:, 22]  # Frequencia do ventilador 02


"Dados da planta"
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

# Dados de catalogo dos equipamentos
V_dot_bomba_alta = 0.012777778  # Vazão de catalogo da bomba a 60 Hz [m^3/s]
V_dot_bomba_rec = 0.41725  # Vazão de catalogo da bomba a 60 Hz [m^3/s]

# Eficiencia isentrópica da turbina
eta_ise_t = 0.7337

"Obtendo as vazões de vapor/condensado e água de re-circulação/resfriamento"
V_dot[:, 0] = V_dot_bomba_alta * (F[:, 2] / 60)  # Vazão de vapor/condensado
V_dot[:, 1] = 2 * V_dot_bomba_rec * (F[:, 0] / 60)  # Vazão de água de re-circulação

"SEÇÃO 00 - ENTRADA DA TURBINA"
T[:, 0] = termo_var[:, 17] + 273.15  # Temperatura da água na entrada da turbina [K]
P[:, 0] = termo_var[:, 5] * 1e3  # Pressão do vapor na entrada da turbina [Pa]
h[:, 0] = PropsSI('H', 'P', P[:, 0], 'T', T[:, 0], 'Water')  # Entalpia na entrada da turbina [J/kg-K]
s[:, 0] = PropsSI('S', 'P', P[:, 0], 'T', T[:, 0], 'Water')  # Entropia na entrada da turbina [J/K]

"SEÇÃO 01 - SAÍDA DA TURBINA"
# Processo Isentrópico
P[:, 1] = termo_var[:, 3] * 1e3  # Pressão de saturação na saída da turbina [Pa]
h[:, 1] = PropsSI('H', 'P', P[:, 1], 'S', s[:, 0], 'Water')  # Entalpia isentrópica na saída da turbina [J/kg-K]

# Processo Real. Calculando a entalpia real na saída da turbina por meio da eficiência isentrópica
h[:, 1] = h[:, 0] - ((h[:, 0] - h[:, 1]) * eta_ise_t)  # Obtendo a entalpia real [j/kg-k]
T[:, 1] = PropsSI('T', 'P', P[:, 1], 'H', h[:, 1], 'Water')  # Temperatura na saída da turbina [K]
s[:, 1] = PropsSI('S', 'P', P[:, 1], 'H', h[:, 1], 'Water')  # Entropia na saída da turbina [J/K]

"SEÇÃO 03 - ENTRADA DO CONDENSADOR"
T[:, 3] = termo_var[:, 10] + 273.15  # Temperatura da água de resfriamento na entrada 01 do condensador [K]
P[:, 3] = termo_var[:, 1] * 1e3  # Pressão na entrada 01 do condensador lado frio (água da torre de resfriamento) [Pa]
rho[:, 3] = PropsSI('D', 'P', P[:, 1], 'H', h[:, 1], 'Water')  # Densidade na entrada 01 do condensador [kg/m^3]

"""Resolvendo Dentro do Condensador"""
m_dot[:, 3] = V_dot[:, 1] * rho[:, 3]
