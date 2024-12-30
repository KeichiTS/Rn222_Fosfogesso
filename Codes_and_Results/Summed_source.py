# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 11:40:21 2024

@author: KeichiTS
"""

import matplotlib.pyplot as plt
import pandas as pd
import glob
import seaborn as sns
import numpy as np
from mpl_toolkits.basemap import Basemap

# Specify the path to the directory containing your CSV files
directory_path = 'C:/Users/KeichiTS/Documents/MEGA/Pessoais/Rn222_Fosfogesso/Codes_and_Results/'

# Define a list to store DataFrames from all matching files
data_frames = []

# Define the file name pattern to match (e.g., '20*.csv' for all files starting with '20')
file_pattern = '*.csv'


# Use glob to get a list of file paths matching the pattern
file_paths = glob.glob(directory_path + file_pattern)

# Loop through each file and read it into a DataFrame
for file_path in file_paths:
    file_name = file_path.split('/')[-1]  # Get the file name from the full path
    year_month_day = file_name[:-4]  # Remove the '.csv' extension
    df = pd.read_csv(file_path)  # Read CSV
    data_frames.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Group by 'LAT' and 'LON' and sum the 'Total_Rn2200100' values
summed_data = combined_df.groupby(['LAT', 'LON'])['Total_Rn2200100'].sum().reset_index()

# Rename the column to something meaningful
summed_data.rename(columns={'Total_Rn2200100': 'Total_Rn2200100_Sum'}, inplace=True)

# Optional: If you want to apply any scaling (e.g., multiply by a factor)
# summed_data['Total_Rn2200100_Sum'] *= scaling_factor  # Uncomment and replace 'scaling_factor' if needed

summed_data['Total_Rn2200100_Sum'] *= 5.97

# Optional: Apply a log transformation
summed_data['Total_Rn2200100_Sum'] = np.log(summed_data['Total_Rn2200100_Sum'])

# Define a minimum concentration threshold (ignore values below this threshold)
limite_minimo = -100  # Adjust this value as needed
#limite_minimo = 0

# Filter out values below the defined threshold
summed_data_filtrado = summed_data[summed_data['Total_Rn2200100_Sum'] > limite_minimo]

# Get the latitude and longitude range for the plot
lat_min, lat_max = summed_data_filtrado['LAT'].min() - .2, summed_data_filtrado['LAT'].max() + .2
lon_min, lon_max = summed_data_filtrado['LON'].min() - .2, summed_data_filtrado['LON'].max() + .2

# Create a pivot table for Seaborn heatmap
heatmap_data = summed_data_filtrado.pivot(index='LAT', columns='LON', values='Total_Rn2200100_Sum')

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 8))

# Create a Basemap instance
m = Basemap(projection='mill', llcrnrlat=lat_min, urcrnrlat=lat_max, 
            llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='i')

# Draw coastlines and political boundaries
m.drawcoastlines()
m.drawcountries()

# Draw gridlines (parallels and meridians)
m.drawparallels(np.arange(lat_min, lat_max, 10), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(lon_min, lon_max, 10), labels=[0,0,0,1], fontsize=10)

# Convert lat/lon to map coordinates
x, y = m(summed_data_filtrado['LON'].values, summed_data_filtrado['LAT'].values)

# Create the heatmap using scatter plot
sc = m.scatter(x, y, c=summed_data_filtrado['Total_Rn2200100_Sum'].values, cmap='tab20b', 
               s=750, edgecolor='none', marker='s')

# Add colorbar
cbar = m.colorbar(sc, location='bottom', pad="2%")
#cbar.set_label('Concentração de Rn-222 em Log')
cbar.set_label('Concentração de Rn-222 (28 dias)')


# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Mapa de Calor de concentração de Rn-222 (Bq/m³) ao Redor do Mundo - Acumulado (28 dias)')

# Show the plot
plt.show()

# Specify the path to the file where you want to save the DataFrame
caminho_arquivo_csv = 'jaguda_data_filtered_combined.csv'

# Save the filtered DataFrame to a CSV file
summed_data_filtrado.to_csv(caminho_arquivo_csv, index=False)