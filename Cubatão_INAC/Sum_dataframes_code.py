# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 12:29:40 2023

@author: KeichiTS
"""
import matplotlib.pyplot as plt
import pandas as pd
import glob
import seaborn as sns
import numpy as np
from mpl_toolkits.basemap import Basemap

# Specify the path to the directory containing your text files
directory_path = 'Simulated_data/'

# Define a list to store DataFrames from all matching files
data_frames = []

# Define the file name pattern to match (e.g., '20*.txt' for all files starting with '20')
#The pattern of the files is YYMMDD. i.e. 10*.txt 
file_pattern = '20*.txt'

# Use glob to get a list of file paths matching the pattern
file_paths = glob.glob(directory_path + file_pattern)

# Loop through each file and read it into a DataFrame
for file_path in file_paths:
    file_name = file_path.split('/')[-1]  # Get the file name from the full path
    year_month_day = file_name[:-4]  # Remove the '.txt' extension
    df = pd.read_csv(file_path, delimiter=r"\s+")
    data_frames.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Filter the DataFrame to include only rows with HR = 12 or HR = 00 
combined_df = combined_df[combined_df['HR'] == 12]

# Group by 'LAT' and 'LON' and sum the 'Rn2200005' values
#summed_data = combined_df.groupby(['LAT', 'LON'])['Rn2200010'].sum().reset_index()
summed_data = combined_df.groupby(['LAT', 'LON'])['Rn2200010'].mean().reset_index()


# Rename the column to something meaningful like 'Rn2200010'
summed_data.rename(columns={'Rn2200010': 'Total_Rn2200010'}, inplace=True)



# Define o limite mínimo de concentração
limite_minimo = 0.0002  # Ajuste conforme necessário

# Filtra as concentrações muito baixas
summed_data_filtrado = summed_data[summed_data['Total_Rn2200010'] > limite_minimo]

# Get the latitude and longitude range
lat_min, lat_max = summed_data_filtrado['LAT'].min() - 0, summed_data_filtrado['LAT'].max() + 0
lon_min, lon_max = summed_data_filtrado['LON'].min() - 0, summed_data_filtrado['LON'].max() + 0


# Ajuste os limites de latitude e longitude para centralizar o plot
# Adicione ou subtraia valores dos limites mínimos e máximos conforme necessário
#lat_center = (lat_min + lat_max) / 2
#lon_center = (lon_min + lon_max) / 2

lat_center = -23.8333336014725
lon_center = -46.38574757419513

lat_min, lat_max = lat_center - .5, lat_center + .5
lon_min, lon_max = lon_center - .5 , lon_center + .5

# Create a pivot table for Seaborn heatmap
heatmap_data = summed_data_filtrado.pivot('LAT', 'LON', 'Total_Rn2200010')

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 8))

# Create a Basemap instance for the world
m = Basemap(projection='mill', llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='i')

# Draw coastlines and political boundaries
m.drawcoastlines()
m.drawcountries()

# Draw gridlines
m.drawparallels(np.arange(lat_min, lat_max, .2), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(lon_min, lon_max, .2), labels=[0,0,0,1], fontsize=10)

# Convert lat/lon to map coordinates
x, y = m(summed_data_filtrado['LON'].values, summed_data_filtrado['LAT'].values)

# Create the heatmap using scatter plot
sc = m.scatter(x, y, c=summed_data_filtrado['Total_Rn2200010'].values, cmap='tab20c', s=500, edgecolor='none', marker='s')

# Add colorbar
cbar = m.colorbar(sc, location='bottom', pad="5%")
cbar.set_label('Rn2200010 Concentrations')

# Define o número de intervalos desejados na colorbar
num_intervalos = 6

# Adiciona ticks à colorbar
cbar.set_ticks(np.linspace(summed_data_filtrado['Total_Rn2200010'].min(), summed_data_filtrado['Total_Rn2200010'].max(), num_intervalos))


# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Heatmap of mean Rn222 concentrations in the atmosphere (Bq/m³) within a 10-meter column between 2018-2022')

# Show the plot
plt.show()

# Especifique o caminho do arquivo onde você deseja salvar o DataFrame
caminho_arquivo_csv = 'summed_data.csv'

# Salve o DataFrame em um arquivo CSV
summed_data.to_csv(caminho_arquivo_csv, index=False)