# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:59:42 2023

@author: KeichiTS
"""
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Load world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Load your data
teste = pd.read_csv('C:/Users/KeichiTS/Documents/MEGA/Pessoais/Rn222_Fosfogesso/Cubatão/Simulated_data/101022.txt', delimiter=r"\s+")
# Create a Seaborn heatmap
heatmap_data = teste.pivot('LAT', 'LON', 'Rn2200005')

# Create a Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the world map boundaries
world.boundary.plot(ax=ax, linewidth=1)

# Overlay the Seaborn heatmap on top of the world map
heatmap = sns.heatmap(heatmap_data, cmap='viridis', cbar=False, ax=ax)

# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Heatmap of Rn2200005 Concentrations on World Map')

# Adjust the colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = plt.colorbar(heatmap.get_children()[0], cax=cax)  # Use the heatmap object to create the colorbar
cbar.set_label('Rn2200005 Concentrations')

# Show the plot
plt.show()