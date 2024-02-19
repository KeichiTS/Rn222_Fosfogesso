# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 23:46:57 2024

@author: KeichiTS
"""

import pandas as pd
import numpy as np

# Leitura do arquivo CSV
df = pd.read_csv('summed_data.csv')

lat_origem, lon_origem = -19.980428531205444, -47.87719937858118

# Define as fronteiras das regiões
lat_border = lat_origem + 0.5
lon_border = lon_origem + 0.5

# Conta o número de pontos em cada região
noroeste = df[(df['LAT'] > lat_origem) & (df['LON'] < lon_origem)]
nordeste = df[(df['LAT'] > lat_origem) & (df['LON'] > lon_origem)]
sudeste = df[(df['LAT'] < lat_origem) & (df['LON'] > lon_origem)]
sudoeste = df[(df['LAT'] < lat_origem) & (df['LON'] < lon_origem)]

# Calcula o percentual de pontos em cada região
total_pontos = len(df)
percentual_noroeste = len(noroeste) / total_pontos * 100
percentual_nordeste = len(nordeste) / total_pontos * 100
percentual_sudeste = len(sudeste) / total_pontos * 100
percentual_sudoeste = len(sudoeste) / total_pontos * 100

# Exibe os percentuais
print("Percentual de pontos ao Noroeste: {:.2f}%".format(percentual_noroeste))
print("Percentual de pontos ao Nordeste: {:.2f}%".format(percentual_nordeste))
print("Percentual de pontos ao Sudeste: {:.2f}%".format(percentual_sudeste))
print("Percentual de pontos ao Sudoeste: {:.2f}%".format(percentual_sudoeste))

# 3. Calcular a distância de cada ponto ao ponto de origem
df['distancia'] = np.sqrt((df['LAT'] - lat_origem) ** 2 + (df['LON'] - lon_origem) ** 2)

# 4. Filtrar os pontos que estão dentro do raio especificado a partir do ponto de origem
raio = 4.5  # Raio em graus de latitude ou longitude
pontos_dentro_raio = df[(df['LAT'] >= lat_origem - raio) & (df['LAT'] <= lat_origem + raio) &
                        (df['LON'] >= lon_origem - raio) & (df['LON'] <= lon_origem + raio)]

# 5. Calcular a concentração total de radônio dentro da área específica
concentracao_total_area = pontos_dentro_raio['Total_Rn2200010'].sum()

# 6. Calcular a concentração total de radônio em todo o conjunto de dados
concentracao_total_todos_pontos = df['Total_Rn2200010'].sum()

# 7. Calcular o percentual de concentração na área em relação à concentração total de radônio em todo o conjunto de dados
percentual_concentracao_area = (concentracao_total_area / concentracao_total_todos_pontos) * 100

print(f"A concentração total de radônio dentro do raio de {raio} graus a partir da origem é: {concentracao_total_area}")
print(f"O percentual de concentração na área em relação à concentração total de radônio em todo o conjunto de dados é: {percentual_concentracao_area:.2f}%")