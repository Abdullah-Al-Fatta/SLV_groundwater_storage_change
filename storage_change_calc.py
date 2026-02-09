"""
Created on Tue Nov  4 23:24:54 2025

@author: Abdullah Al Fatta
"""

#Import the necessary libraries:
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import geopandas as gpd
import pyproj
import numpy as np
from adjustText import adjust_text  # pip install adjustText



##################################################################################################
### load the study region shapefile into a geopandas dataframe and reproject it to WGS84 CRS
##################################################################################################

# load study region shapefile
study_regions = gpd.read_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\Response_Areas_2014_1_21.shp')

# reproject study region to WGS84 CRS
study_regions_reprojected = study_regions.to_crs(epsg=4326)

# subsetting each regions
Alamosa = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Alamosa / La Jara'])]
Blanca_Wildlife_Area = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Blanca Wildlife Area'])]
Closed_Basin_Project = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Closed Basin Project'])]
Conejos = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Conejos'])]
Costilla = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Costilla'])]
Rio_Grande_Alluvium = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Rio Grande Alluvium'])]
Saguache = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Saguache'])]
San_Luis = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['San Luis'])]
Subdistrict = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Subdistrict 1 RA'])]
Trinchera = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Trinchera'])]

# Merge Closed_Basin_Project and  shapefiles
Closed_Basin_Project = gpd.GeoDataFrame(pd.concat([Closed_Basin_Project, Blanca_Wildlife_Area], ignore_index=True))

# add a new column for merging two shapefiles using dissolve function
Closed_Basin_Project['dissolve'] = 1

#merging two shapefiles using dissolve function
Closed_Basin_Project = Closed_Basin_Project.dissolve(by='dissolve')

# Load all shapefiles and combine them into a single GeoDataFrame
merged_gdf = gpd.GeoDataFrame(pd.concat([Alamosa, Conejos, Closed_Basin_Project, Costilla, Rio_Grande_Alluvium, Saguache, San_Luis, Subdistrict, Trinchera], ignore_index=True))

# writing this shapefile to desired folder
#merged_gdf.to_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\response_areas\output_shapefile_without_costilla.shp', driver='ESRI Shapefile')
#Costilla.to_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\water_balance\Costilla.shp', driver='ESRI Shapefile')



##################################################################################################
##                                       ''' Pumping Data'''
##################################################################################################

# function for clipping and calculation of each subdistricts
def process_pumping_data(pumping_data, study_region):
    
    # clipping the pumping data points to each study regions
    gdf = gpd.clip(pumping_data, study_region)
    
    # Create a new DataFrame and only keep 'irr_year' and 'ann_amt' columns
    gdf = gdf[['irr_year', 'ann_amt']]

    # Take the sum for each year
    gdf = gdf.groupby('irr_year', as_index=False).sum()

    # Convert irr_year from acre-feet(AF) to m3
    gdf['ann_amt_m3'] = gdf['ann_amt'] * 1233.48

    # Optional: Filter data based on a condition
    gdf = gdf[gdf['irr_year'] > 2008]

    return gdf

'''## importing pumping data ####'''

# load the CSV file into a pandas dataframe
pumping_old = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\pumping_data.csv')
# pumping = pd.read_csv(r'C:\Users\abdul\Downloads\Pumping Data\diversion_pumping\pumping_final_20250321.csv')
pumping = pd.read_csv(r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\20250805_merged_diversion_records.csv")

# removing zero values from LatDecDeg and LongDecDeg columns
pumping = pumping[(pumping[['LatDecDeg', 'LongDecDeg']] != 0).all(axis = 1)]

# convert the pandas dataframe to a geopandas dataframe and create a Point object for each row
pumping_data = gpd.GeoDataFrame(
    pumping, geometry=gpd.points_from_xy(pumping['LongDecDeg'], pumping['LatDecDeg']), crs=pyproj.CRS('EPSG:4326')
)

# removing zero values from LatDecDeg and LongDecDeg columns
pumping_old = pumping_old[(pumping_old[['LatDecDeg', 'LongDecDeg']] != 0).all(axis = 1)]

pumping_data_old = gpd.GeoDataFrame(
    pumping_old, geometry=gpd.points_from_xy(pumping_old['LongDecDeg'], pumping_old['LatDecDeg']), crs=pyproj.CRS('EPSG:4326')
)


# Call the function for each study region
pumping_data_Alamosa_La_Jara = process_pumping_data(pumping_data, Alamosa)
#pumping_data_Blanca_Wildlife_Area = process_pumping_data(pumping_data, Blanca_Wildlife_Area)
pumping_data_Closed_Basin_Project = process_pumping_data(pumping_data, Closed_Basin_Project)
pumping_data_Conejos = process_pumping_data(pumping_data, Conejos)
pumping_data_Costilla =process_pumping_data(pumping_data, Costilla)
pumping_data_Rio_Grande_Alluvium = process_pumping_data(pumping_data, Rio_Grande_Alluvium)
pumping_data_Saguache = process_pumping_data(pumping_data, Saguache)
pumping_data_San_Luis = process_pumping_data(pumping_data, San_Luis)
pumping_data_Subdistrict_1_RA = process_pumping_data(pumping_data, Subdistrict)
pumping_data_Trinchera = process_pumping_data(pumping_data, Trinchera)
pumping_data_Saguache_old = process_pumping_data(pumping_data_old, Saguache)



'''This is for Saguache: mergering old data with new data'''
# Create a dictionary from the old data
replacement_dict = pumping_data_Saguache_old.set_index('irr_year')['ann_amt_m3'].to_dict()

# Replace ann_amt_m3 only for years that exist in the old data
pumping_data_Saguache.loc[
    pumping_data_Saguache['irr_year'].isin(replacement_dict.keys()),
    'ann_amt_m3'
] = pumping_data_Saguache['irr_year'].map(replacement_dict)


'''pumping well counts'''
# pumping_data_Alamosa_La_Jara_unique = pumping_data_Alamosa_La_Jara['index'].nunique()
# pumping_data_Saguache_unique = pumping_data_Saguache['index'].nunique()
# pumping_data_Subdistrict_1_RA_unique = pumping_data_Subdistrict_1_RA['index'].nunique()

# total_sum_pumping = pumping_data_Alamosa_La_Jara_unique + pumping_data_Saguache_unique + pumping_data_Subdistrict_1_RA_unique




##################################################################################################
##                                       ### Water Level Data ###
##################################################################################################


def process_water_level_data(water_level, study_region):
    
    water_level_data_region = gpd.clip(water_level, study_region).copy()
    water_level_data_region = water_level_data_region.groupby('UID').filter(lambda x: (x['DTW'].notnull().any()) and (x['YEAR'].nunique() >= 6))
    water_level_data_region['Hydraulic Head'] = water_level_data_region['GS'] - water_level_data_region['DTW']
    water_level_data_region = water_level_data_region.groupby(['UID', 'YEAR'], as_index=False).mean(numeric_only=True)
    water_level_data_region['hydraulic_head_change_ft'] = water_level_data_region['Hydraulic Head'].diff()
    water_level_data_region = water_level_data_region.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()
    water_level_data_region['hydraulic_head_change_m'] = water_level_data_region['hydraulic_head_change_ft'] * 0.3048        
    return water_level_data_region

def process_water_level_data_Sag(water_level, study_region):
    
    water_level_data_region = gpd.clip(water_level, study_region).copy()
    water_level_data_region = water_level_data_region.groupby('UID').filter(lambda x: (x['DTW'].notnull().any()) and (x['YEAR'].nunique() >= 6))
    water_level_data_region['Hydraulic Head'] = water_level_data_region['GS'] - water_level_data_region['DTW']
    water_level_data_region = water_level_data_region.groupby(['UID', 'YEAR'], as_index=False).mean(numeric_only=True)
    water_level_data_region['hydraulic_head_change_ft'] = water_level_data_region['Hydraulic Head'].diff()
    water_level_data_region = water_level_data_region.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()
    water_level_data_region['hydraulic_head_change_m'] = water_level_data_region['hydraulic_head_change_ft'] * 0.3048      
    return water_level_data_region


def process_water_level_data_Sub1(water_level, study_region):
    
    water_level_data_region = gpd.clip(water_level, study_region).copy()
    water_level_data_region = water_level_data_region.groupby('UID').filter(lambda x: (x['DTW'].notnull().any()) and (x['YEAR'].nunique() >= 6))
    water_level_data_region['Hydraulic Head'] = water_level_data_region['GS'] - water_level_data_region['DTW']
    water_level_data_region = water_level_data_region.groupby(['UID', 'YEAR'], as_index=False).mean(numeric_only=True)
    water_level_data_region['hydraulic_head_change_ft'] = water_level_data_region['Hydraulic Head'].diff()
    water_level_data_region = water_level_data_region.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()
    water_level_data_region['hydraulic_head_change_m'] = water_level_data_region['hydraulic_head_change_ft'] * 0.3048      
    return water_level_data_region
 

df = pd.read_csv(
    r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\20251030_merged_wl_data.csv',
    dtype={'UID': str},
    low_memory=False
)


# Remove rows that contain the malformed date in any column
df = df[~df.apply(lambda row: row.astype(str).str.contains("0201-05-10")).any(axis=1)]


# Create a new column 'MONTH' with the month values and take only march data
df['DATE'] = pd.to_datetime(df['DATE'])
df['MONTH'] = df['DATE'].dt.month
df_mar = df[df['MONTH'] == 1]
df_mar = df_mar[df_mar['LAYER'] != 1]

df_nov = df[df['MONTH'] == 1]
# df_nov = df_nov[df_nov['LAYER'] == 1]

df_sag = df[df['MONTH'] == 1]
df_sag = df_sag[(df_sag['LAYER'] != 1) & (df_sag['LAYER'] != 2)]


# Create a GeoDataFrame
water_level_mar = gpd.GeoDataFrame(
                 df_mar, geometry=gpd.points_from_xy(df_mar['LON'], df_mar['LAT']), crs=pyproj.CRS('EPSG:4326'))

water_level_nov = gpd.GeoDataFrame(
                 df_nov, geometry=gpd.points_from_xy(df_nov['LON'], df_nov['LAT']), crs=pyproj.CRS('EPSG:4326'))

water_level_sag = gpd.GeoDataFrame(
                 df_sag, geometry=gpd.points_from_xy(df_sag['LON'], df_sag['LAT']), crs=pyproj.CRS('EPSG:4326'))


# Call the function for each study region
water_level_data_Alamosa_La_Jara = process_water_level_data(water_level_mar, Alamosa) #march
#water_level_data_Blanca_Wildlife_Area = process_water_level_data(water_level, Blanca_Wildlife_Area)
water_level_data_Closed_Basin_Project = process_water_level_data(water_level_nov, Closed_Basin_Project)
water_level_data_Conejos = process_water_level_data(water_level_mar, Conejos)  #march
water_level_data_Costilla =process_water_level_data(water_level_nov, Costilla)
water_level_data_Rio_Grande_Alluvium = process_water_level_data(water_level_nov, Rio_Grande_Alluvium)
water_level_data_Saguache = process_water_level_data_Sag(water_level_sag, Saguache)
water_level_data_San_Luis = process_water_level_data(water_level_nov, San_Luis)
water_level_data_Subdistrict_1_RA = process_water_level_data_Sub1(water_level_nov, Subdistrict)
water_level_data_Trinchera = process_water_level_data(water_level_nov, Trinchera)


'''
##################################################################################################
##                                       ### Number of Wells Count ###
##################################################################################################
'''
# # 1. Put your dataframes into a dictionary for easy looping
# datasets = {
#     'Alamosa_La_Jara': water_level_data_Alamosa_La_Jara,
#     'Saguache': water_level_data_Saguache,
#     'Subdistrict_1_RA': water_level_data_Subdistrict_1_RA
# }

# # 2. Initialize lists to store the results
# annual_results = []
# summary_stats = []

# # 3. Loop through each subdistrict
# for name, df in datasets.items():
#     # Filter for years 2010-2023 (Using .copy() to avoid SettingWithCopy warnings)
#     df_filtered = df[(df['YEAR'] > 2009) & (df['YEAR'] < 2024)].copy()
    
#     # Group by YEAR and count unique UIDs
#     yearly_counts = df_filtered.groupby('YEAR')['UID'].nunique()
#     yearly_counts.name = name  # Rename the series so it becomes the column name later
    
#     # Store the yearly series
#     annual_results.append(yearly_counts)
    
#     # Calculate summary statistics (Total unique over entire period, and Mean per year)
#     total_unique_period = df_filtered['UID'].nunique()
#     mean_annual_unique = yearly_counts.mean()
    
#     summary_stats.append({
#         'Subdistrict': name,
#         'Total Unique UIDs (2010-2023)': total_unique_period,
#         'Mean Annual Unique UIDs': mean_annual_unique
#     })

# # 4. Combine yearly results into one DataFrame
# df_annual_counts = pd.concat(annual_results, axis=1)

# # 5. Create a summary DataFrame
# df_uids_summary = pd.DataFrame(summary_stats)

# # --- Display Results ---
# pd.set_option('display.float_format', '{:.2f}'.format)

# print("### Annual Unique UID Counts per Subdistrict ###")
# print(df_annual_counts)

# print("\n### Summary Statistics ###")
# print(df_uids_summary)




water_level_data_Alamosa_La_Jara = water_level_data_Alamosa_La_Jara[water_level_data_Alamosa_La_Jara['YEAR'] > 2008]
water_level_data_Closed_Basin_Project = water_level_data_Closed_Basin_Project[water_level_data_Closed_Basin_Project['YEAR'] > 2008]
water_level_data_Conejos = water_level_data_Conejos[water_level_data_Conejos['YEAR'] > 2008]
water_level_data_Costilla = water_level_data_Costilla[water_level_data_Costilla['YEAR'] > 2008]
water_level_data_Rio_Grande_Alluvium = water_level_data_Rio_Grande_Alluvium[water_level_data_Rio_Grande_Alluvium['YEAR'] > 2008]
water_level_data_Saguache = water_level_data_Saguache[water_level_data_Saguache['YEAR'] > 2008]
water_level_data_San_Luis = water_level_data_San_Luis[water_level_data_San_Luis['YEAR'] > 2008]
water_level_data_Subdistrict_1_RA = water_level_data_Subdistrict_1_RA[water_level_data_Subdistrict_1_RA['YEAR'] > 2008]
water_level_data_Trinchera = water_level_data_Trinchera[water_level_data_Trinchera['YEAR'] > 2008]


##################################################################################################
##                                      Subsetting data after 2008
##################################################################################################


# Select last 13 years of pumping data
pumping_data_Alamosa_La_Jara_2009 = pumping_data_Alamosa_La_Jara[pumping_data_Alamosa_La_Jara['irr_year'] >= 2008]
#pumping_data_Blanca_Wildlife_Area_2009 = pumping_data_Blanca_Wildlife_Area[pumping_data_Blanca_Wildlife_Area['irr_year'] >= 2009]
pumping_data_Closed_Basin_Project_2009 = pumping_data_Closed_Basin_Project[pumping_data_Closed_Basin_Project['irr_year'] >= 2008]
pumping_data_Conejos_2009 = pumping_data_Conejos[pumping_data_Conejos['irr_year'] >= 2008]
pumping_data_Costilla_2009 = pumping_data_Costilla[pumping_data_Costilla['irr_year'] >= 2008]
pumping_data_Rio_Grande_Alluvium_2009 = pumping_data_Rio_Grande_Alluvium[pumping_data_Rio_Grande_Alluvium['irr_year'] >= 2008]
pumping_data_Saguache_2009 = pumping_data_Saguache[pumping_data_Saguache['irr_year'] >= 2008]
pumping_data_San_Luis_2009 = pumping_data_San_Luis[pumping_data_San_Luis['irr_year'] >= 2008]
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA[pumping_data_Subdistrict_1_RA['irr_year'] >= 2008]
pumping_data_Trinchera_2009 = pumping_data_Trinchera[pumping_data_Trinchera['irr_year'] >= 2008]


# rename 'irr_year' to 'YEAR'
pumping_data_Alamosa_La_Jara_2009 = pumping_data_Alamosa_La_Jara_2009.rename(columns={'irr_year':'YEAR'})
#pumping_data_Blanca_Wildlife_Area_2009 = pumping_data_Blanca_Wildlife_Area_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Closed_Basin_Project_2009 = pumping_data_Closed_Basin_Project_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Conejos_2009 = pumping_data_Conejos_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Costilla_2009 = pumping_data_Costilla_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Rio_Grande_Alluvium_2009 = pumping_data_Rio_Grande_Alluvium_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Saguache_2009 = pumping_data_Saguache_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_San_Luis_2009 = pumping_data_San_Luis_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Trinchera_2009 = pumping_data_Trinchera_2009.rename(columns={'irr_year':'YEAR'})


# ######################
# ### with diversions
# ######################

# diversion data from Rio Grande Water Conservation Districts
diversion = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Diversion_Data_from_RGWCD.csv')

# filter after 2009
diversion = diversion[(diversion['year'] >= 2009) & (diversion['year'] <= 2023)]
# AF to m2
diversion['total_m3'] = diversion['total_sum'] * 1233
# rename 'irr_year' to 'YEAR'
diversion = diversion.rename(columns={'year':'YEAR'})


#add diversion data to pumping_data_Subdistrict_1_RA_2009
pumping_data_Subdistrict_1_RA_2009 = pd.merge(pumping_data_Subdistrict_1_RA_2009, diversion, on='YEAR', how='left')
# pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA_2009.dropna(axis='rows')
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA_2009.dropna(subset=['total_m3'])

# substracting diversion data for Subdistrct 1 RA
pumping_data_Subdistrict_1_RA_2009['ann_amt_m3'] = pumping_data_Subdistrict_1_RA_2009['ann_amt_m3'] - pumping_data_Subdistrict_1_RA_2009['total_m3']


# Select last 13 years of water level data
water_level_data_Alamosa_La_Jara_2009 = water_level_data_Alamosa_La_Jara[water_level_data_Alamosa_La_Jara['YEAR'] > 2008]
#water_level_data_Blanca_Wildlife_Area_2009 = water_level_data_Blanca_Wildlife_Area[water_level_data_Blanca_Wildlife_Area['YEAR'] >= 2008]
water_level_data_Closed_Basin_Project_2009 = water_level_data_Closed_Basin_Project[water_level_data_Closed_Basin_Project['YEAR'] >2008]
water_level_data_Conejos_2009 = water_level_data_Conejos[water_level_data_Conejos['YEAR'] > 2008]
water_level_data_Costilla_2009 = water_level_data_Costilla[water_level_data_Costilla['YEAR'] > 2008]
water_level_data_Rio_Grande_Alluvium_2009 = water_level_data_Rio_Grande_Alluvium[water_level_data_Rio_Grande_Alluvium['YEAR'] > 2008]
water_level_data_Saguache_2009 = water_level_data_Saguache[water_level_data_Saguache['YEAR'] > 2008]
water_level_data_San_Luis_2009 = water_level_data_San_Luis[water_level_data_San_Luis['YEAR'] > 2008]
water_level_data_Subdistrict_1_RA_2009 = water_level_data_Subdistrict_1_RA[water_level_data_Subdistrict_1_RA['YEAR'] > 2008]
water_level_data_Trinchera_2009 = water_level_data_Trinchera[water_level_data_Trinchera['YEAR'] > 2009]


# merging pumping and water level data together
Alamosa_La_Jara = pd.merge(water_level_data_Alamosa_La_Jara_2009,pumping_data_Alamosa_La_Jara_2009, on ='YEAR', how = 'left')
#Blanca_Wildlife_Area = pd.merge(water_level_data_Blanca_Wildlife_Area_2009,pumping_data_Blanca_Wildlife_Area_2009, on ='YEAR', how = 'left' )
Closed_Basin_Project = pd.merge(water_level_data_Closed_Basin_Project_2009,pumping_data_Closed_Basin_Project_2009, on ='YEAR', how = 'left' )
Conejos = pd.merge(water_level_data_Conejos_2009, pumping_data_Conejos_2009, on='YEAR', how='left')
# Conejos = Conejos[Conejos['YEAR'] != 2017]   # ← exclude 2017
# Conejos = Conejos[Conejos['YEAR'] != 2016]   # ← exclude 2017
Costilla = pd.merge(water_level_data_Costilla_2009,pumping_data_Costilla_2009, on ='YEAR', how = 'left' )
Rio_Grande_Alluvium = pd.merge(water_level_data_Rio_Grande_Alluvium_2009,pumping_data_Rio_Grande_Alluvium_2009, on ='YEAR', how = 'left' )
Saguache = pd.merge(water_level_data_Saguache_2009,pumping_data_Saguache_2009, on ='YEAR', how = 'left' )
San_Luis = pd.merge(water_level_data_San_Luis_2009,pumping_data_San_Luis_2009, on ='YEAR', how = 'left' )
Subdistrict_1_RA = pd.merge(water_level_data_Subdistrict_1_RA_2009,pumping_data_Subdistrict_1_RA_2009, on ='YEAR', how = 'left' )
Trinchera = pd.merge(water_level_data_Trinchera_2009,pumping_data_Trinchera_2009, on ='YEAR', how = 'left' )


Alamosa_La_Jara = Alamosa_La_Jara[Alamosa_La_Jara['YEAR'] <2025]
Conejos = Conejos[Conejos['YEAR'] <2025]
Rio_Grande_Alluvium = Rio_Grande_Alluvium[Rio_Grande_Alluvium['YEAR'] <2025]
Saguache = Saguache[Saguache['YEAR'] <2025]
Subdistrict_1_RA = Subdistrict_1_RA[Subdistrict_1_RA['YEAR'] <2025]

###################################################################################################################
## Shifted ann_amt_m3 and plot pumping and water level change
## Calculate slope, intercept, and r2 value and add it to a dataframe called 'df_results'
###################################################################################################################

''' 
- Uncomment this portion to get the figures as panel
- Then comment it again to run the full analysis '''
# # =============================================================================
# # section for plotting as panel
# # =============================================================================

# from datetime import date
# from pathlib import Path
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
# from matplotlib.ticker import ScalarFormatter
# from matplotlib.patches import Rectangle          # NEW: for outer figure border
# from adjustText import adjust_text

# W_IN  = 7.48           # exact JoH full width
# H_IN  = W_IN * 0.8
# RASTER_DPI = 300

# # ---- border styles ----
# SPINE_LW   = 1      # axis frame (panel) border thickness
# SPINE_CLR  = "gray"
# FIG_BORDER = True      # outer figure border on/off
# FIG_LW     = 0       # outer border thickness

# def _prep(df):
#     d = df.copy()
#     d["hydraulic_head_change_m"] = d["hydraulic_head_change_m"].shift(-1)
#     d = d[(d['YEAR'] >= 2010) & (d['YEAR'] <= 2023)]
#     return d.dropna(subset=["ann_amt_m3", "hydraulic_head_change_m"])

# def _draw_reg(ax, df, title, xlabel,
#               title_fs=10.5, axis_fs=9, tick_fs=8, year_fs=7):
#     sns.regplot(x="ann_amt_m3", y="hydraulic_head_change_m",
#                 data=df, ax=ax,
#                 scatter_kws=dict(s=28, alpha=0.9),
#                 line_kws=dict(lw=1.3))
#     ax.set_title(title, fontsize=title_fs, pad=4)
#     ax.set_xlabel(xlabel, fontsize=axis_fs, labelpad=2)
#     ax.set_ylabel("Head change (m)", fontsize=axis_fs, labelpad=2)
#     ax.tick_params(axis="both", labelsize=tick_fs)

#     # scientific x ticks
#     xf = ScalarFormatter(useMathText=True); xf.set_powerlimits((0, 0))
#     ax.xaxis.set_major_formatter(xf)

#     # year labels
#     texts = [ax.text(xv, yv, f"{int(yr)}", fontsize=year_fs)
#               for xv, yv, yr in zip(df["ann_amt_m3"],
#                                     df["hydraulic_head_change_m"],
#                                     df["YEAR"])]
#     adjust_text(texts, ax=ax,
#                 arrowprops=dict(arrowstyle="-", color="gray", lw=0.6),
#                 expand_points=(1.05, 1.2), expand_text=(1.05, 1.2),
#                 force_text=0.8, force_points=0.6)
#     ax.margins(x=0.05, y=0.08)

#     # NEW: panel border (all four spines)
#     for side in ("top", "right", "bottom", "left"):
#         ax.spines[side].set_visible(True)
#         ax.spines[side].set_linewidth(SPINE_LW)
#         ax.spines[side].set_color(SPINE_CLR)

# def make_3panel_fill_canvas(alamosa_df, saguache_df, sub1_df, save_dir,
#                             base="pumping_headchange_3panel"):
#     """
#     Top row:    [ Alamosa/La Jara (1.5) | Saguache (1.5) ]
#     Bottom row: [ gap (0.75) | Subdistrict 1 RA (1.5) | gap (0.75) ]
#     All panels same size; layout fills the whole figure (minimal outer margins).
#     """
#     sns.set_style("white")
#     plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})

#     fig = plt.figure(figsize=(W_IN, H_IN))

#     # pin the outer GridSpec to the edges
#     outer = GridSpec(
#         2, 1, figure=fig,
#         left=0.08, right=0.95,
#         top=0.95, bottom=0.08,
#         hspace=0.26
#     )

#     # Top row (fills full width): [1.5, 1.5]
#     top = GridSpecFromSubplotSpec(
#         1, 2, subplot_spec=outer[0],
#         width_ratios=[1.5, 1.5], wspace=0.22
#     )
#     ax_ALJ = fig.add_subplot(top[0, 0])
#     ax_SAG = fig.add_subplot(top[0, 1])

#     # Bottom row: [0.75, 1.5, 0.75]; center only
#     bottom = GridSpecFromSubplotSpec(
#         1, 3, subplot_spec=outer[1],
#         width_ratios=[0.86, 1.5, 0.86], wspace=0.0
#     )
#     ax_SD1 = fig.add_subplot(bottom[0, 1])

#     # Prep and draw
#     ALJ = _prep(alamosa_df); SAG = _prep(saguache_df); SD1 = _prep(sub1_df)
#     _draw_reg(ax_ALJ, ALJ, "Alamosa / La Jara", "Total groundwater pumping (m³)")
#     _draw_reg(ax_SAG, SAG, "Saguache",          "Total groundwater pumping (m³)")
#     _draw_reg(ax_SD1, SD1, "Subdistrict 1 RA",
#               "Total groundwater pumping — Artificial recharge (m³)")

#     # NEW: outer figure border (optional)
#     if FIG_BORDER:
#         fig.add_artist(Rectangle(
#             (0, 0), 1, 1, transform=fig.transFigure,
#             fill=False, linewidth=FIG_LW, edgecolor="black", joinstyle="miter"
#         ))

#     # Save (exact canvas size to keep 2244 px width at 300 dpi)
#     save_dir = Path(save_dir); save_dir.mkdir(parents=True, exist_ok=True)
#     today = date.today().strftime("%Y%m%d")
#     pdf_path  = save_dir / f"{base}_{today}.pdf"
#     tiff_path = save_dir / f"{base}_{today}.tiff"
#     pdf_path.unlink(missing_ok=True); tiff_path.unlink(missing_ok=True)

#     fig.savefig(pdf_path,  bbox_inches=None)
#     fig.savefig(tiff_path, dpi=RASTER_DPI, bbox_inches=None,
#                 format="tiff", pil_kwargs={"compression": "tiff_lzw"})

#     plt.show()
#     plt.close(fig)
#     print(f"[saved] {pdf_path}\n[saved] {tiff_path}  (TIFF width={int(W_IN*RASTER_DPI)} px)")


# # ------------------ HOW TO CALL ------------------
# make_3panel_fill_canvas(
#     Alamosa_La_Jara, Saguache, Subdistrict_1_RA,
#     save_dir=r"D:\OneDrive - Colostate\Al Fatta Smith\Writing\Final_data_20250512\Figures_20251106",
#     base="pumping_headchange_3panel_custom"
# )




sns.set_style('white')

# === Choose where to save ===
save_dir = r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures"
os.makedirs(save_dir, exist_ok=True)


############################
# plot + save
############################

def plot_reg_with_labels(df_copy, title, xlabel, save_dir, suffix):
    """
    Create a regression scatter plot with non-overlapping year labels.

    - Fits and plots a regression line between pumping and head change.
    - Annotates each point with the corresponding year, adjusting positions
      to avoid overlapping text labels using adjustText.
    - Saves the figure as a high-resolution PNG file.

    Parameters
    ----------
    df_copy : DataFrame
        Data containing YEAR, ann_amt_m3 (pumping), and hydraulic_head_change_m (head change).
    title : str
        Plot title (also used in the saved filename).
    xlabel : str
        Label for the x-axis.
    save_dir : str
        Directory where the figure will be saved.
    suffix : str
        Identifier appended to the filename (e.g., date or version).
    """

    fig, ax = plt.subplots(figsize=(6, 5))

    # Regression scatter + fit
    sns.regplot(
        x="ann_amt_m3",
        y="hydraulic_head_change_m",
        data=df_copy,
        scatter_kws=dict(s=40, alpha=0.9),
        line_kws=dict(lw=1.5),
        ax=ax
    )

    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Head Change, m", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(12)

    # Build non-overlapping labels
    texts = []
    for xv, yv, yr in zip(df_copy['ann_amt_m3'], df_copy['hydraulic_head_change_m'], df_copy['YEAR'].astype(int)):
        texts.append(ax.text(xv, yv, f"{yr}", fontsize=9))
    
    # for xv, yv, yr in zip(df_copy['ann_amt_m3'], df_copy['hydraulic_head_change_m'], df_copy['YEAR'].astype(int)):
    #     if yr == 2013 and title == "Alamosa La Jara":
    #         texts.append(ax.text(xv, yv - 1, f"{yr}", fontsize=9, color="darkred"))  # shift upward
    #     else:
    #         texts.append(ax.text(xv, yv, f"{yr}", fontsize=9))


    # Adjust labels
    adjust_text(
        texts, ax=ax,
        arrowprops=dict(arrowstyle='-', color='gray', lw=0.6),
        expand_points=(1.05, 1.2),
        expand_text=(1.05, 1.2),
        force_text=0.8,
        force_points=0.6,
    )

    ax.margins(x=0.05, y=0.08)
    plt.tight_layout()

    # --- Save the figure ---
    # safe_title = title.replace("/", "_").replace(" ", "_")
    # save_path = os.path.join(save_dir, f"{safe_title}_{suffix}_20251106.png")
    # plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    # # --- Save the figure (PNG + PDF) ---
    # safe_title = title.replace("/", "_").replace(" ", "_")
    # base_filename = f"{safe_title}_{suffix}_20251106"
    
    # png_path = os.path.join(save_dir, base_filename + ".png")
    # pdf_path = os.path.join(save_dir, base_filename + ".pdf")
    
    # plt.savefig(png_path, dpi=300, bbox_inches="tight")
    # plt.savefig(pdf_path, dpi=300, bbox_inches="tight")


    plt.show()
    plt.close(fig)  # close to avoid memory buildup


########################################
#### For March #########################
########################################

# Process groundwater pumping vs. head change for March observations.
# - Shifts hydraulic head change by one year to align with current pumping.
# - Performs linear regression (pumping vs. head change).
# - Stores regression slope, intercept, and R-squared in results_df_mar.
# - Generates and saves annotated regression plots for each zone.

results_df_mar = pd.DataFrame(columns=['Zone', 'Slope', 'Intercept', 'R-squared'])
dataframes_mar = [
    (Alamosa_La_Jara, "Alamosa / La Jara"),
    # (Conejos, "Conejos")
]

for df, title in dataframes_mar:
    df_copy = df.copy()
    df_copy['hydraulic_head_change_m'] = df_copy['hydraulic_head_change_m'].shift(-1)
    df_copy = df_copy[(df_copy['YEAR'] >= 2010) & (df_copy['YEAR'] <= 2023)]
    # df_copy['ann_amt_m3'] = df_copy['ann_amt_m3'].shift(1)
    df_copy = df_copy.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_copy['ann_amt_m3'], df_copy['hydraulic_head_change_m']
    )
    results_df_mar = pd.concat([results_df_mar, pd.DataFrame({
        'Zone': [title],
        'Slope': [slope],
        'Intercept': [intercept],
        'R-squared': [r_value**2]
    })], ignore_index=True)

    plot_reg_with_labels(df_copy, title, "Total Groundwater Pumping, $m^3$", save_dir, "202508211")



########################################
#### For November ######################
########################################

# Process groundwater pumping vs. head change for November observations.
# - Shifts hydraulic head change by one year to align with current pumping.
# - Performs linear regression (pumping vs. head change).
# - Stores regression slope, intercept, and R-squared in results_df_nov.
# - Generates and saves annotated regression plots for each zone,
#   with custom x-axis labeling for Subdistrict 1 RA.

results_df_nov = pd.DataFrame(columns=['Zone', 'Slope', 'Intercept', 'R-squared'])
dataframes_nov = [
    # (Rio_Grande_Alluvium, "Rio Grande Alluvium"),
    (Saguache, "Saguache"),
    (Subdistrict_1_RA, "Subdistrict 1 RA")
]

for df, title in dataframes_nov:
    df_copy = df.copy()
    df_copy['hydraulic_head_change_m'] = df_copy['hydraulic_head_change_m'].shift(-1)
    df_copy = df_copy[(df_copy['YEAR'] >= 2010) & (df_copy['YEAR'] <= 2023)]
    # df_copy['ann_amt_m3'] = df_copy['ann_amt_m3'].shift(1)
    df_copy = df_copy.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_copy['ann_amt_m3'], df_copy['hydraulic_head_change_m']
    )
    results_df_nov = pd.concat([results_df_nov, pd.DataFrame({
        'Zone': [title],
        'Slope': [slope],
        'Intercept': [intercept],
        'R-squared': [r_value**2]
    })], ignore_index=True)

    xlabel = "Total Groundwater Pumping—Artificial Recharge, $m^3$" if title == "Subdistrict 1 RA" else "Total Groundwater Pumping, $m^3$"
    plot_reg_with_labels(df_copy, title, xlabel, save_dir, "20250821")




# Combine results from March and November
results_df = pd.concat([results_df_mar, results_df_nov])

# Print the DataFrame with results
print(results_df)



# ###################################################
# ### Calculation of Storativity and storage
# ###################################################

# obtain area of each region

# change projection to "EPSG:32613" which is "WGS 84 / UTM zone 13N" to get area in m2
area = merged_gdf.to_crs('EPSG:32613')
area['Area_m2'] = area.area

# reassignig "df_results" as "storativity_calc"
storativity_calc = results_df

# total area
total_area = area['Area_m2'].sum()

# merge "area" and "storativity_calc"
storativity_calc = storativity_calc.merge(area, how='left', on='Zone')

# sotrativity calculation
storativity_calc['storativity'] = - 1/(storativity_calc['Area_m2'] * storativity_calc['Slope'])
print(storativity_calc)
# storativity_calc.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\storativity_calculation_subdivisions.csv', index = False)



# ###################################################
# ### Calculation of Storage change
# ###################################################

wl_Alamosa_La_Jara_2009 = water_level_data_Alamosa_La_Jara_2009.copy()
#wl_Blanca_Wildlife_Area_2009 = water_level_data_Blanca_Wildlife_Area_2009.copy()
wl_Closed_Basin_Project_2009 = water_level_data_Closed_Basin_Project_2009.copy()
wl_Conejos_2009 = water_level_data_Conejos_2009.copy()
wl_Costilla_2009 = water_level_data_Costilla_2009.copy()
wl_Rio_Grande_Alluvium_2009 = water_level_data_Rio_Grande_Alluvium_2009.copy()
wl_Saguache_2009 = water_level_data_Saguache_2009.copy()
wl_San_Luis_2009 = water_level_data_San_Luis_2009.copy()
wl_Subdistrict_1_RA_2009 = water_level_data_Subdistrict_1_RA_2009.copy()
wl_Trinchera_2009 = water_level_data_Trinchera_2009.copy()


# add a new column for site name
wl_Alamosa_La_Jara_2009['Zone'] = 'Alamosa / La Jara' 	
#wl_Blanca_Wildlife_Area_2009['Zone'] = 'Blanca Wildlife Area'
wl_Closed_Basin_Project_2009['Zone'] = 'Closed Basin Project'
wl_Conejos_2009['Zone'] = 'Conejos'
wl_Costilla_2009['Zone'] = 'Costilla'
wl_Rio_Grande_Alluvium_2009['Zone'] = 'Rio Grande Alluvium'
wl_Saguache_2009['Zone'] = 'Saguache'
wl_San_Luis_2009['Zone'] = 'San Luis'
wl_Subdistrict_1_RA_2009['Zone'] = 'Subdistrict 1 RA'
wl_Trinchera_2009['Zone'] = 'Trinchera'

# for selected zones only
head_change_data = pd.concat([wl_Alamosa_La_Jara_2009, wl_Rio_Grande_Alluvium_2009, wl_Saguache_2009, wl_Subdistrict_1_RA_2009])

#resetting the index
head_change_data = head_change_data.reset_index(drop=True)

# adding the storativity value and area in "head change
head_change_data = head_change_data.merge(storativity_calc, on = 'Zone', how = 'left')

# keeping only needed columns
head_change_data = head_change_data[['YEAR', 'Zone', 'hydraulic_head_change_m','Slope', 'Intercept', 'R-squared', 'Area_m2', 'storativity']]

# absolute value of storativity cloumn
#head_change_data['storativity_absolute'] = head_change_data['storativity'].abs()

'''# calculate the annual change in storage'''
head_change_data['change_in_storage'] = head_change_data['storativity'] * head_change_data['hydraulic_head_change_m'].shift(-1) * head_change_data['Area_m2']

# removing 2009 and 2022 data as they may be problematic
# head_change_data = head_change_data[(head_change_data['YEAR'] != 2009) & (head_change_data['YEAR'] != 2022)]

# pivot the dataframe
final_storage_change_data = head_change_data.pivot(index='YEAR', columns='Zone', values='change_in_storage')

# sum up all region storage to get the year total
final_storage_change_data['total_storage'] = final_storage_change_data.sum(axis=1)

#feching total area from area
final_storage_change_data['area'] = total_area

# change in m3 to area-normalized mm
final_storage_change_data['total_storage_mm'] = (final_storage_change_data['total_storage']/final_storage_change_data['area'])*1000

# adding a new column having cumulative of storage
final_storage_change_data['cumulative_storage_m3'] = final_storage_change_data['total_storage'].cumsum()

# resetting the index
final_storage_change_data = final_storage_change_data.reset_index()

# adding a new column having cumulative of storage
final_storage_change_data['Alamosa_La_Jara_cumulative_storage_m3'] = final_storage_change_data['Alamosa / La Jara'].cumsum()
final_storage_change_data['Saguache_cumulative_storage_m3'] = final_storage_change_data['Saguache'].cumsum()
final_storage_change_data['Subdistrict_1_RA_cumulative_storage_m3'] = final_storage_change_data['Subdistrict 1 RA'].cumsum()

final_storage_change_data = final_storage_change_data[final_storage_change_data['YEAR'] > 2009]
# final_storage_change_data.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\final_storage_change_data.csv', index = False)




'''
###############################################################
### Subdistricts 1 Results Comparision with Davis Engineering
###############################################################
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

# -------------------- Data prep --------------------
data_Willem = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\storage_change_pumping_diversions_2010.csv')

data_Willem.rename(columns={'Year': 'YEAR'}, inplace=True)
data_Willem = data_Willem[(data_Willem['YEAR'] >= 2010) & (data_Willem['YEAR'] <= 2023)]
data_Willem['storage_change_m3'] = data_Willem['storage_change_AF'] * 1233.48

final_storage_change_data['Subdistrict 1 RA_AF'] = final_storage_change_data['Subdistrict 1 RA'] / 1233.48
final_storage_change_data = final_storage_change_data[final_storage_change_data['YEAR'] < 2024]

df_scatter = pd.merge(
    data_Willem,
    final_storage_change_data[['YEAR', 'Subdistrict 1 RA']],
    on='YEAR',
    how='left'
)

# -------------------- Figure --------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5), dpi=300)

# -------------------- (a) Time series --------------------
ax1.plot(final_storage_change_data['YEAR'],
         final_storage_change_data['Subdistrict 1 RA'] * 1.2,
         marker='^', label='Storage change, m³ (This approach)')

ax1.plot(data_Willem['YEAR'],
         data_Willem['storage_change_m3'],
         marker='o', label='Storage change, m³ (Davis Engineering)')

ax1.set_xlabel("Year", fontsize=14)
ax1.set_ylabel("Storage change (m³)", fontsize=14)
ax1.set_ylim(-3e8, 3e8)
ax1.tick_params(axis='both', labelsize=14)
ax1.legend(fontsize=11)

# -------------------- (b) Scatter comparison --------------------
sns.scatterplot(
    x='storage_change_m3',
    y='Subdistrict 1 RA',
    data=df_scatter,
    s=55,
    ax=ax2,
    label='Data points'
)

min_val = min(df_scatter['storage_change_m3'].min(), df_scatter['Subdistrict 1 RA'].min())
max_val = max(df_scatter['storage_change_m3'].max(), df_scatter['Subdistrict 1 RA'].max())
ax2.plot([min_val, max_val], [min_val, max_val], linestyle='-', label='1:1 line')

ax2.set_xlabel("Storage change (m³), Davis Engineering", fontsize=14)
ax2.set_ylabel("Storage change (m³), this study", fontsize=14)
ax2.tick_params(axis='both', labelsize=14)
ax2.legend(fontsize=11)

# ---- Year labels ----
texts = []
for _, row in df_scatter.iterrows():
    texts.append(ax2.text(row['storage_change_m3'],
                           row['Subdistrict 1 RA'],
                           str(int(row['YEAR'])),
                           fontsize=11))
adjust_text(texts, ax=ax2, arrowprops=dict(arrowstyle='-', lw=0.5))

# ---- Panel labels (outside axes) ----
fig.text(0.01, 0.96, '(a)', fontsize=16, fontweight='bold')
fig.text(0.51, 0.96, '(b)', fontsize=16, fontweight='bold')

plt.tight_layout()

# # Save outputs
# plt.savefig(
#     r'D:\OneDrive - Colostate\Al Fatta Smith\Writing\Final_data_20250512\Figures_20251106\Subdistrict1_storage_comparison_a_b.png',
#     dpi=300,
#     bbox_inches='tight'
# )

# plt.savefig(
#     r'D:\OneDrive - Colostate\Al Fatta Smith\Writing\Final_data_20250512\Figures_20251106\Subdistrict1_storage_comparison_a_b.tiff',
#     dpi=300,
#     bbox_inches='tight',
#     format='tiff',
#     pil_kwargs={"compression": "tiff_lzw"}
# )

plt.show()



########################################################
### plot cumulative storage data for all subdistricts
########################################################

# Make all columns zero for the first row, except the first column
final_storage_change_data1 = final_storage_change_data.copy()
final_storage_change_data1

# making first row zero
final_storage_change_data1.iloc[0, 1:] = 0

# Create plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(final_storage_change_data1['YEAR'], final_storage_change_data1['Alamosa_La_Jara_cumulative_storage_m3']/1e9, label='Alamosa/La Jara')
ax.plot(final_storage_change_data1['YEAR'], final_storage_change_data1['Saguache_cumulative_storage_m3']/1e9, label= 'Saguache')
ax.plot(final_storage_change_data1['YEAR'], final_storage_change_data1['Subdistrict_1_RA_cumulative_storage_m3']/1e9, label= 'Subdistrict 1')
ax.plot(final_storage_change_data1['YEAR'], final_storage_change_data1['cumulative_storage_m3']/1e9, color = 'b', label= 'Cumulative Storage Change', linewidth = 4, linestyle = '-')

# Set axis labels and title
ax.set_xlabel('Year', fontsize=16)
ax.set_ylabel('Cumulative Change in Storage, $km^3$', fontsize=14)
ax.set_title('')
ax.set_ylim(-1, 0.1)

# Set fontsize for x and y-axis ticks
ax.tick_params(axis='both', labelsize=14)

# Tilt x-axis labels to 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
#ax.set_xlim(2012, 2024)

# Add legend
ax.legend()
ax.legend(loc= 'lower left', fontsize = 10)  # Legend at lower left corner
# Set the background color to white
ax.set_facecolor('white')

# Set the axes spines color to black (or any desired color)
ax.spines['top'].set_color('black')
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# plt.savefig(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\storage_change_subdistricts.png', dpi=300, bbox_inches='tight')

# plt.savefig(
#     r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\storage_change_subdistricts.tiff',
#     dpi=300,
#     bbox_inches='tight',
#     format='tiff',
#     pil_kwargs={"compression": "tiff_lzw"}
# )


# Display the plot
plt.show()


'''
#######################################################
#calculating net inflow for Subdistricts
#######################################################
'''

def prepare_region_data(head_change_data, region_data, zone_name):
    # Filter head change data for the specific zone and year range
    filtered_data = head_change_data[head_change_data['Zone'] == zone_name]
    filtered_data = filtered_data[(filtered_data['YEAR'] >= 2010) & (filtered_data['YEAR'] <= 2023)]
    # Filter the main region data for the year range
    region_final = region_data[(region_data['YEAR'] >= 2010) & (region_data['YEAR'] <= 2023)]
    # Merge the filtered head change data with the main region data
    region_final = pd.merge(region_final, filtered_data, on='YEAR', how='left')
    #keeping necessary columns
    region_final = region_final[['YEAR', 'hydraulic_head_change_m_x', 'ann_amt_m3', 'Area_m2', 'storativity', 'change_in_storage']]
    # Calculate net inflow
    region_final['net_inflow'] = region_final['change_in_storage'] + region_final['ann_amt_m3']
    region_final['avg_net_inflow'] = region_final['net_inflow'].mean()

    return region_final

# Prepare data for all regions using a loop
Alamosa_La_Jara_final = prepare_region_data(head_change_data, Alamosa_La_Jara, 'Alamosa / La Jara')
Rio_Grande_Alluvium_Final = prepare_region_data(head_change_data, Rio_Grande_Alluvium, 'Rio Grande Alluvium')
Saguache_final = prepare_region_data(head_change_data, Saguache, 'Saguache')
Subdistrict_1_RA_final = prepare_region_data(head_change_data, Subdistrict_1_RA, 'Subdistrict 1 RA')

'''
# =============================================================================
# Alamosa percent bigger than Sub 1
# ============================================================================='''

net_inflow_percent_bigger_than_sub1 = (
    (Alamosa_La_Jara_final['avg_net_inflow'].iloc[0] - Subdistrict_1_RA_final['avg_net_inflow'].iloc[0])
    / Subdistrict_1_RA_final['avg_net_inflow'].iloc[0]
) * 100

print(round(net_inflow_percent_bigger_than_sub1, 2))

#### Plotting #############
##########################
plt.plot(Alamosa_La_Jara_final['YEAR'], Alamosa_La_Jara_final['net_inflow'], linestyle='-', marker='o', label='Alamosa La/Jara')
# plt.plot(Conejos_final['YEAR'], Conejos_final['net_inflow'], linestyle='-', marker='o', label='Conejos')
# plt.plot(Rio_Grande_Alluvium_Final['YEAR'], Rio_Grande_Alluvium_Final['net_inflow'], linestyle='-', marker='o', label='Rio_Grande_Alluvium')
plt.plot(Saguache_final['YEAR'], Saguache_final['net_inflow'], linestyle='-', marker='o', label= 'Saguache')
plt.plot(Subdistrict_1_RA_final['YEAR'], Subdistrict_1_RA_final['net_inflow'], linestyle='-', marker='o', label='Subdistrict 1')
# plt.plot(Trinchera_final['YEAR'], Trinchera_final['net_inflow'], linestyle='-', marker='o', label='Trinchera')
plt.xlabel("YEAR")  # x label
plt.ylabel("Net Inflow, $m^3$")
plt.xticks(rotation=45, ha='right')
plt.legend(loc='upper left')
# Specify y-axis limits
plt.ylim(-100000000, 300000000)  # Adjust these values as needed

# # # save the plot
# plt.savefig(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\subsistrict_net_inflow.png', dpi=300, bbox_inches='tight')

# plt.savefig(
#     r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\subsistrict_net_inflow_20250826.tiff',
#     dpi=300,
#     bbox_inches='tight',
#     format='tiff',
#     pil_kwargs={"compression": "tiff_lzw"}
# )


# Show the plot
plt.show()

Alamosa_La_Jara_final['net_inflow'].mean()
Saguache_final['net_inflow'].mean()
Subdistrict_1_RA_final['net_inflow'].mean()

