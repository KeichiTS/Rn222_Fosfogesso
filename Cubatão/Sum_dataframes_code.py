# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 12:29:40 2023

@author: KeichiTS
"""

import pandas as pd
import glob

# Specify the path to the directory containing your text files
directory_path = 'C:/Users/KeichiTS/Documents/MEGA/Pessoais/Rn222_Fosfogesso/Cubatão/Simulated_data/'

# Define a list to store DataFrames from all matching files
data_frames = []

# Define the file name pattern to match (e.g., '20*.txt' for all files starting with '20')
file_pattern = '*.txt'

# Use glob to get a list of file paths matching the pattern
file_paths = glob.glob(directory_path + file_pattern)

# Loop through each file and read it into a DataFrame
for file_path in file_paths:
    # Read the file and add a new 'YEARMONTHDAY' column based on the file name
    file_name = file_path.split('/')[-1]  # Get the file name from the full path
    year_month_day = file_name[:-4]  # Remove the '.txt' extension
    df = pd.read_csv(file_path, delimiter=r"\s+")
    df['YEARMONTHDAY'] = year_month_day  # Add the 'YEARMONTHDAY' column
    data_frames.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Now, 'combined_df' contains the data from all the matching files concatenated into a single DataFrame