# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 12:27:47 2023

@author: abdullah al fatta

"""

###############################################################################################################################################################
##   Masking a raster file using a shapefile and calculate the mean value of the pixels within the masked area and calc percent contribution from subsidence
##################################################################################################################################################################

import fiona
import rasterio
import rasterio.mask
import geopandas as gpd
import numpy.ma as ma
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_mean_area(shapefile_path, raster_path):
    with fiona.open(shapefile_path, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open(raster_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    masked_array = ma.masked_where(out_image == -9999, out_image)
    mean_value = ma.mean(masked_array)

    gdf = gpd.read_file(shapefile_path)
    wshed_proj = gdf.to_crs(epsg='32613')
    area = wshed_proj.geometry.area.iloc[0]

    return mean_value, area

shapefile_paths = [
    "D:/OneDrive - Colostate/Al Fatta Smith/Code/3 2 2023/updated_codes/Journal of Hydrology/Datasets/shapefiles/Alamosa___La_Jara.shp",
    # "D:/OneDrive - Colostate/Al Fatta Smith/Code/3 2 2023/updated_codes/Journal of Hydrology/Datasets/shapefiles/Saguache.shp",
    "D:/OneDrive - Colostate/Al Fatta Smith/Code/3 2 2023/updated_codes/Journal of Hydrology/Datasets/shapefiles/Saguache_InSAR_Boundary.shp",
    "D:/OneDrive - Colostate/Al Fatta Smith/Code/3 2 2023/updated_codes/Journal of Hydrology/Datasets/shapefiles/Subdistrict_1_RA.shp",
]

raster_path = "D:/OneDrive - Colostate/Al Fatta Smith/Pumping and water-level data/required_data/subsidence_data/geotiff_map_fine.tiff"

results = []

for shapefile in shapefile_paths:
    mean, area = calculate_mean_area(shapefile, raster_path)
    watershed_name = os.path.splitext(os.path.basename(shapefile))[0]
    results.append((watershed_name, mean, area))

df_subsidence = pd.DataFrame(results, columns=["subdistrict", "Mean Value", "Area (sq meters)"])
df_subsidence['storage_change_subsidence'] = df_subsidence['Mean Value'] * df_subsidence['Area (sq meters)'] * 0.001/8
df_subsidence['storage_change_subsidence_total'] = df_subsidence['Mean Value'] * df_subsidence['Area (sq meters)'] * 0.001
print(df_subsidence)

# df_subsidence.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\df_subsidence.csv')



'''
#####################################################
Percentage Calculation
#####################################################

'''

df_storage_data = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\20251110_final_storage_change_data.csv')


df_storage_data = df_storage_data[(df_storage_data['YEAR'] > 2014) & (df_storage_data['YEAR'] <= 2022) ]
df_storage_data = df_storage_data[['Alamosa / La Jara', 'Saguache', 'Subdistrict 1 RA']]

# Sum all rows for each column
df_storage_data = df_storage_data.sum()

# Sum of each numeric column except the first one
df_storage_data = df_storage_data.reset_index()
df_storage_data.columns = ['subdistrict', 'storage']
df_storage_data['avg_storage'] = df_storage_data['storage']/7
                 
                 
# Define the mapping of old values to new values
replacement_dict = {
    'Alamosa / La Jara': 'Alamosa___La_Jara',
    'Saguache': 'Saguache_InSAR_Boundary',
    'Subdistrict 1 RA': 'Subdistrict_1_RA',
}

# Replace the values in the 'subdistrict' column
df_storage_data['subdistrict'] = df_storage_data['subdistrict'].replace(replacement_dict)

# Merging the DataFrames on the 'subdistrict' column
df_merged_storage = pd.merge(df_subsidence, df_storage_data, on='subdistrict')
df_merged_storage['total'] = df_merged_storage['storage_change_subsidence_total'] + df_merged_storage['storage']
df_merged_storage['percentage'] = df_merged_storage['storage_change_subsidence_total']/df_merged_storage['total'] * 100

print(df_merged_storage)

'''
###########################
Plotting
###########################
'''

storage_data_with_subsidence = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\20251110_final_storage_change_data_with_subsidence.csv')

# making first row zero
storage_data_with_subsidence.iloc[0, 1:] = 0

# # adding a new column having cumulative of storage
storage_data_with_subsidence['total_storage'] = storage_data_with_subsidence['Alamosa / La Jara'] +  storage_data_with_subsidence['Saguache'] + storage_data_with_subsidence['Subdistrict 1 RA']
storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3'] = storage_data_with_subsidence['Alamosa / La Jara'].cumsum()
storage_data_with_subsidence['Saguache_cumulative_storage_m3'] = storage_data_with_subsidence['Saguache'].cumsum()
storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3'] = storage_data_with_subsidence['Subdistrict 1 RA'].cumsum()
storage_data_with_subsidence['cumulative_storage_m3'] = storage_data_with_subsidence['total_storage'].cumsum()
storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3_subsidence'] = storage_data_with_subsidence['Alamosa_La_Jara_subsidence'].cumsum()
storage_data_with_subsidence['Saguache_cumulative_storage_m3_subsidence'] = storage_data_with_subsidence['Saguache_subsidence'].cumsum()
storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3_subsidence'] = storage_data_with_subsidence['Subdistrict_1_RA_subsidence'].cumsum()
storage_data_with_subsidence['Alamosa_combined'] = storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3'] + storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3_subsidence']
storage_data_with_subsidence['Saguache_combined'] = storage_data_with_subsidence['Saguache_cumulative_storage_m3'] + storage_data_with_subsidence['Saguache_cumulative_storage_m3_subsidence']
storage_data_with_subsidence['Subdistrct_1_RA_combined'] = storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3'] + storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3_subsidence']
storage_data_with_subsidence['Total_subsidence'] = storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3_subsidence'] + storage_data_with_subsidence['Saguache_cumulative_storage_m3_subsidence'] + storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3_subsidence']
storage_data_with_subsidence['Total_storage_m3'] = storage_data_with_subsidence['cumulative_storage_m3'] + storage_data_with_subsidence['Total_subsidence'] 



# Create plot
fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Alamosa_combined'], label='Alamosa/La Jara ')
ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Alamosa_La_Jara_cumulative_storage_m3_subsidence'], label= 'Alamosa/La Jara Fine-grained', linestyle='-')
# ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Saguache_combined'], label= 'Saguache Total')
ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Saguache_cumulative_storage_m3_subsidence'], label= 'Saguache Fine-grained', linestyle='-')
# ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Subdistrct_1_RA_combined'], label= 'Subdistrict 1 RA Total')
ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Subdistrict_1_RA_cumulative_storage_m3_subsidence'], label= 'Subdistrict_1_RA Fine-grained', linestyle='-')
ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Total_subsidence'],  label= 'Total Storage Loss from Fine-grained', linestyle = '-')
# ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['cumulative_storage_m3'],  label= 'Cumulative Storage Change from coarse-grained layer', linewidth = 3, linestyle = '--')
# ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Total_storage_m3'],  label= 'Cumulative Storage Change from both fine- and coarsed-grained layer', linewidth = 3, linestyle = '-')

# Set axis labels and title
ax.set_xlabel('Year', fontsize=16)
ax.set_ylabel('Cumulative Change in Storage, $m^3$', fontsize=16)
ax.set_title('')


# Set fontsize for x and y-axis ticks
ax.tick_params(axis='both', labelsize=16)

# Tilt x-axis labels to 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
#ax.set_xlim(2012, 2024)

# Add legend
ax.legend()
ax.legend(loc= 'lower left', fontsize = 12)  # Legend at lower left corner
# Set the background color to white
ax.set_facecolor('white')

# Set the axes spines color to black (or any desired color)
ax.spines['top'].set_color('black')
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')


# plt.savefig(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\storage_change_subdistricts_fine_grained.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()


# Create plot
fig, ax = plt.subplots(figsize=(10, 5))

# Add markers to distinguish overlapping lines

ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Alamosa_combined'], 
        label='Alamosa/La Jara (fine- and coarse-grained)', linewidth=1.5)

ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Saguache_combined'], 
            label='Saguache (fine- and coarse-grained)', linewidth=1.5)

ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Subdistrct_1_RA_combined'], 
        label='Subdistrict 1 (fine- and coarse-grained)', linewidth=1.5)

ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['cumulative_storage_m3'],  
        label='Total Storage Change from coarse-grained layers', linewidth=2)

ax.plot(storage_data_with_subsidence['YEAR'], storage_data_with_subsidence['Total_storage_m3'],  
        label='Total Storage Change from both fine- and coarse-grained layers', linewidth=3)

# Set labels and title
ax.set_xlabel('Year', fontsize=16)
ax.set_ylabel('Cumulative Storage Change, $m^3$', fontsize=16)
ax.legend(loc='lower left', fontsize=10)

# Improve tick formatting
ax.tick_params(axis='both', labelsize=16)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

# Set background and spine colors
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_color('black')

# Save the plot
# save_path = r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\storage_change_subdistricts.png'
# plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
