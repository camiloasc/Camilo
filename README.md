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