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
directory_path = 'C:/Users/KeichiTS/Documents/MEGA/Pessoais/Rn222_Fosfogesso/Uberaba_New/'

# Define a list to store DataFrames from all matching files
data_frames = []

# Define the file name pattern to match (e.g., '20*.txt' for all files starting with '20')
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
combined_df = combined_df[combined_df['HR'] == 00]

# Group by 'LAT' and 'LON' and sum the 'Rn2200010' values
summed_data = combined_df.groupby(['LAT', 'LON'])['Rn2200010'].sum().reset_index()

# Rename the column to something meaningful
summed_data.rename(columns={'Rn2200010': 'Total_Rn2200010'}, inplace=True)

# Scale the concentrations
summed_data['Total_Rn2200010'] *= 6670296.69

# Apply the log transformation
summed_data['Total_Rn2200010'] = np.log(summed_data['Total_Rn2200010'])

# Get the latitude and longitude range
lat_min, lat_max = summed_data['LAT'].min() - .02, summed_data['LAT'].max() + .02
lon_min, lon_max = summed_data['LON'].min() - .02, summed_data['LON'].max() + .02

# Create a pivot table for Seaborn heatmap
heatmap_data = summed_data.pivot(index='LAT', columns='LON', values='Total_Rn2200010')

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 8))

# Create a Basemap instance
m = Basemap(projection='mill', llcrnrlat=lat_min, urcrnrlat=lat_max, 
            llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='i')

# Draw coastlines and political boundaries
m.drawcoastlines()
m.drawcountries()

# Draw gridlines (parallels and meridians)
m.drawparallels(np.arange(lat_min, lat_max, 1), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(lon_min, lon_max, 1), labels=[0,0,0,1], fontsize=10)

# Convert lat/lon to map coordinates
x, y = m(summed_data['LON'].values, summed_data['LAT'].values)

# Create the heatmap using scatter plot
sc = m.scatter(x, y, c=summed_data['Total_Rn2200010'].values, cmap='tab20c', 
               s=800, edgecolor='none', marker='s')

# Add colorbar
cbar = m.colorbar(sc, location='bottom', pad="2%")
cbar.set_label('Rn2200010 Concentrations')

# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Heatmap of Rn2200010 Concentrations with Global Map')

# Show the plot
plt.show()
