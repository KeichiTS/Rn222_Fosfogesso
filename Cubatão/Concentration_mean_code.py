# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:59:42 2023

@author: KeichiTS
"""
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
import numpy as np


# Load world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Load your data
teste = pd.read_csv('C:/Users/KeichiTS/Documents/MEGA/Pessoais/Rn222_Fosfogesso/Cubatão/Simulated_data/101022.txt', delimiter=r"\s+")
#df['Ln_Values'] = np.log(df['Values'])

teste['Rn2200005'] = teste['Rn2200005']*10e+12
teste['Rn2200005'] = np.log(teste['Rn2200005'])


# Create a Seaborn heatmap with a colorbar
heatmap_data = teste.pivot('LAT', 'LON', 'Rn2200005')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the world map boundaries
world.boundary.plot(ax=ax, linewidth=1)

# Overlay the Seaborn heatmap on top of the world map and add a colorbar
heatmap = sns.heatmap(heatmap_data, cmap='cividis', cbar=True, ax=ax)

# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Heatmap of Rn2200005 Concentrations on World Map')

# Set colorbar label
heatmap.collections[0].colorbar.set_label('Rn2200005 Concentrations')

# Show the plot
plt.show()