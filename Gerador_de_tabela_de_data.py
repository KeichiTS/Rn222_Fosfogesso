# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:54:31 2023

@author: KeichiTS
"""

import pandas as pd
from datetime import datetime, timedelta

ano = 1999

# Definindo a data inicial
data_atual = datetime(ano, 1, 1, 0, 0)

# Criando uma lista para armazenar os dados
dados = []

# Gerando os dados até a data final
while data_atual <= datetime(ano, 12, 31, 0, 0):
    dados.append([
        f"{data_atual.year} {data_atual.month} {data_atual.day} {data_atual.hour} {data_atual.minute}"
    ])
    data_atual += timedelta(days=1)  # Incrementando um dia

# Criando um DataFrame do pandas
df = pd.DataFrame(dados, columns=['Data'])

# Escrevendo o DataFrame no arquivo Excel
df.to_excel('dados_1999.xlsx', index=False)

print("Arquivo Excel gerado com sucesso: dados_1999.xlsx")