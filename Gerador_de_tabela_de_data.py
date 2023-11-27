# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:54:31 2023

@author: KeichiTS
"""

import pandas as pd
from datetime import datetime, timedelta

# Definindo a data inicial
data_atual = datetime(1992, 1, 1, 0, 0)

# Criando uma lista para armazenar os dados
dados = []

# Gerando os dados até junho de 2023
while data_atual <= datetime(1993, 12, 31, 0, 0):
    dados.append([
        f"{data_atual.year} {data_atual.month} {data_atual.day} {data_atual.hour} {data_atual.minute}"
    ])
    data_atual += timedelta(days=1)  # Incrementando um dia

# Criando um DataFrame do pandas
df = pd.DataFrame(dados, columns=['Data'])

# Escrevendo o DataFrame no arquivo Excel
df.to_excel('dados_1992-1993.xlsx', index=False)

print("Arquivo Excel gerado com sucesso: dados_1991.xlsx")