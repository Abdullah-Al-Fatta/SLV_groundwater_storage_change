"""
Created on Wed Aug  6 15:46:54 2025

@author: Abdullah Al Fatta
"""

import ee
import geemap
import pandas as pd
import geopandas as gpd


# Initialize and authenticate the Earth Engine module.
if not ee.data._credentials:
    ee.Authenticate()
    ee.Initialize()

def calculate_annual_rainfall(path_to_watershed, start_year, end_year):
    # Load the PRISM precipitation dataset.
    prism = ee.ImageCollection("OREGONSTATE/PRISM/AN81m").select('ppt')

    # Read the shapefile with geopandas
    gdf = gpd.read_file(path_to_watershed)

    # Ensure the shapefile is in WGS84 (important for Earth Engine)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)

    # Now convert it to an EE object
    watershed = geemap.gdf_to_ee(gdf)

    # Define a function to calculate yearly rainfall totals.
    def yearly_rainfall(year):
        start_date = ee.Date.fromYMD(year-1, 10, 1) #starting from previous year
        # start_date = ee.Date.fromYMD(year, 1, 1) #starting from january year
        end_date = start_date.advance(1, 'year')
        filtered = prism.filter(ee.Filter.date(start_date, end_date))
        total = filtered.reduce(ee.Reducer.sum())
        stats = total.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=watershed.geometry(),
            scale=1000
        )
        return {
            'Year': year,
            'Precipitation': stats.get('ppt_sum').getInfo()
        }

    # Generate a list of years and calculate rainfall for each year.
    years = range(start_year, end_year + 1)
    rainfall_data = [yearly_rainfall(year) for year in years]

    # Convert the results into a DataFrame.
    return pd.DataFrame(rainfall_data)


# List of paths to the shapefiles for different watersheds
watersheds_paths = [
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\Alamosa_La_Jara_watershed.shp",
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\conejos_watershed.shp",
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\rio_grande_watershed.shp",
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\Saguache_watershed.shp",
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\subdistrict1_watershed.shp",
    r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\Trinchera_watershed.shp"
]

# Process each watershed and store results
all_results = {}
for path in watersheds_paths:
    watershed_name = path.split('\\')[-1].replace('.shp', '')  # Extracts the name from the path
    df = calculate_annual_rainfall(path, 1994, 2024)
    all_results[watershed_name] = df
    print(f'Results for {watershed_name}:')
    print(df)

# Combine all results into a single DataFrame if needed
combined_df = pd.concat(all_results, keys=all_results.keys())
print(combined_df)

combined_df = combined_df.reset_index(drop=True)

# combined_df.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\combined_precipitation_waterYear_20250922.csv')

'''# reading precip data after downloading the data (no need to run the above code)'''
# combined_df = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\combined_precipitation_waterYear_20250922.csv')

# subseting the dataframe for individual subdistricts
df_Alamosa = combined_df.loc[0:30].copy()
df_conejos = combined_df.loc[31:61].copy()
df_rio_grande = combined_df.loc[62:92].copy()
df_Saguache = combined_df.loc[93:123].copy()
df_subdistricts_1RA = combined_df.loc[124:154].copy()
df_Trinchera = combined_df.loc[155:185].copy()


##################################################################
# converting the mean value into volume by multiplying the area
#################################################################

subdistricts_watershed_area = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\area.csv')

# Alamosa
df_Alamosa['Precip_m3'] = df_Alamosa['Precipitation'] *  subdistricts_watershed_area['Area_m2'].iloc[0] * 1/1000
# Closed_Basin_Project
df_conejos['Precip_m3'] = df_conejos['Precipitation'] *  subdistricts_watershed_area['Area_m2'].iloc[1] * 1/1000
# Rio Grande Alluvium
df_rio_grande['Precip_m3'] = df_rio_grande['Precipitation'] * subdistricts_watershed_area['Area_m2'].iloc[2] * 1/1000
# Saguache
df_Saguache['Precip_m3'] = df_Saguache['Precipitation'] * subdistricts_watershed_area['Area_m2'].iloc[3] * 1/1000
# Subdistricts_1RA
df_subdistricts_1RA['Precip_m3'] = df_subdistricts_1RA['Precipitation'] * subdistricts_watershed_area['Area_m2'].iloc[4] * 1/1000
# Trinchera
df_Trinchera['Precip_m3'] = df_Trinchera['Precipitation'] * subdistricts_watershed_area['Area_m2'].iloc[5] * 1/1000

# rename 'Year' to 'YEAR'
df_Alamosa = df_Alamosa.rename(columns={'Year':'YEAR'})
df_conejos = df_conejos.rename(columns={'Year':'YEAR'})
df_rio_grande = df_rio_grande.rename(columns={'Year':'YEAR'})
df_Saguache = df_Saguache.rename(columns={'Year':'YEAR'})
df_subdistricts_1RA = df_subdistricts_1RA.rename(columns={'Year':'YEAR'})
df_Trinchera = df_Trinchera.rename(columns={'Year':'YEAR'})


#Import the necessary libraries:
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import geopandas as gpd
import pyproj
import numpy as np




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
    gdf = gdf[gdf['irr_year'] >= 2009]

    return gdf

'''## importing pumping data ####'''

# load the CSV file into a pandas dataframe
pumping_old = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\pumping_data.csv')
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
water_level_data_Closed_Basin_Project = process_water_level_data(water_level_nov, Closed_Basin_Project)
water_level_data_Conejos = process_water_level_data(water_level_mar, Conejos)  #march
water_level_data_Costilla =process_water_level_data(water_level_nov, Costilla)
water_level_data_Rio_Grande_Alluvium = process_water_level_data(water_level_nov, Rio_Grande_Alluvium)
water_level_data_Saguache = process_water_level_data_Sag(water_level_sag, Saguache)
water_level_data_San_Luis = process_water_level_data(water_level_nov, San_Luis)
water_level_data_Subdistrict_1_RA = process_water_level_data_Sub1(water_level_nov, Subdistrict)
water_level_data_Trinchera = process_water_level_data(water_level_nov, Trinchera)


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
pumping_data_Alamosa_La_Jara_2009 = pumping_data_Alamosa_La_Jara[pumping_data_Alamosa_La_Jara['irr_year'] >= 2009]
#pumping_data_Blanca_Wildlife_Area_2009 = pumping_data_Blanca_Wildlife_Area[pumping_data_Blanca_Wildlife_Area['irr_year'] >= 2009]
pumping_data_Closed_Basin_Project_2009 = pumping_data_Closed_Basin_Project[pumping_data_Closed_Basin_Project['irr_year'] >= 2009]
pumping_data_Conejos_2009 = pumping_data_Conejos[pumping_data_Conejos['irr_year'] >= 2009]
pumping_data_Costilla_2009 = pumping_data_Costilla[pumping_data_Costilla['irr_year'] >= 2009]
pumping_data_Rio_Grande_Alluvium_2009 = pumping_data_Rio_Grande_Alluvium[pumping_data_Rio_Grande_Alluvium['irr_year'] >= 2009]
pumping_data_Saguache_2009 = pumping_data_Saguache[pumping_data_Saguache['irr_year'] >= 2009]
pumping_data_San_Luis_2009 = pumping_data_San_Luis[pumping_data_San_Luis['irr_year'] >= 2009]
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA[pumping_data_Subdistrict_1_RA['irr_year'] >= 2009]
pumping_data_Trinchera_2009 = pumping_data_Trinchera[pumping_data_Trinchera['irr_year'] >= 2009]


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

# loading diversion data
# diversion data from Rio Grande Water Conservation Districts
diversion = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Diversion_Data_from_RGWCD.csv')

# filter after 2009
diversion = diversion[(diversion['year'] >= 2009) & (diversion['year'] < 2025)]
# AF to m2
diversion['total_m3'] = diversion['total_sum'] * 1233
# rename 'irr_year' to 'YEAR'
diversion = diversion.rename(columns={'year':'YEAR'})


#add diversion data to pumping_data_Subdistrict_1_RA_2009
pumping_data_Subdistrict_1_RA_2009 = pd.merge(pumping_data_Subdistrict_1_RA_2009, diversion, on='YEAR', how='left')
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA_2009.dropna(axis='rows')
# substracting diversion data for Subdistrct 1 RA
pumping_data_Subdistrict_1_RA_2009['ann_amt_m3'] = pumping_data_Subdistrict_1_RA_2009['ann_amt_m3'] - pumping_data_Subdistrict_1_RA_2009['total_m3']


# Select last 13 years of water level data
water_level_data_Alamosa_La_Jara_2009 = water_level_data_Alamosa_La_Jara[water_level_data_Alamosa_La_Jara['YEAR'] >= 2009]
#water_level_data_Blanca_Wildlife_Area_2009 = water_level_data_Blanca_Wildlife_Area[water_level_data_Blanca_Wildlife_Area['YEAR'] >= 2009]
water_level_data_Closed_Basin_Project_2009 = water_level_data_Closed_Basin_Project[water_level_data_Closed_Basin_Project['YEAR'] >= 2009]
water_level_data_Conejos_2009 = water_level_data_Conejos[water_level_data_Conejos['YEAR'] >= 2009]
water_level_data_Costilla_2009 = water_level_data_Costilla[water_level_data_Costilla['YEAR'] >= 2009]
water_level_data_Rio_Grande_Alluvium_2009 = water_level_data_Rio_Grande_Alluvium[water_level_data_Rio_Grande_Alluvium['YEAR'] >= 2009]
water_level_data_Saguache_2009 = water_level_data_Saguache[water_level_data_Saguache['YEAR'] >= 2009]
water_level_data_San_Luis_2009 = water_level_data_San_Luis[water_level_data_San_Luis['YEAR'] >= 2009]
water_level_data_Subdistrict_1_RA_2009 = water_level_data_Subdistrict_1_RA[water_level_data_Subdistrict_1_RA['YEAR'] >= 2009]
water_level_data_Trinchera_2009 = water_level_data_Trinchera[water_level_data_Trinchera['YEAR'] >= 2009]


# merging pumping and water level data together
Alamosa_La_Jara = pd.merge(water_level_data_Alamosa_La_Jara_2009,pumping_data_Alamosa_La_Jara_2009, on ='YEAR', how = 'left')
#Blanca_Wildlife_Area = pd.merge(water_level_data_Blanca_Wildlife_Area_2009,pumping_data_Blanca_Wildlife_Area_2009, on ='YEAR', how = 'left' )
Closed_Basin_Project = pd.merge(water_level_data_Closed_Basin_Project_2009,pumping_data_Closed_Basin_Project_2009, on ='YEAR', how = 'left' )
Conejos = pd.merge(water_level_data_Conejos_2009,pumping_data_Conejos_2009, on ='YEAR', how = 'left' )
Costilla = pd.merge(water_level_data_Costilla_2009,pumping_data_Costilla_2009, on ='YEAR', how = 'left' )
Rio_Grande_Alluvium = pd.merge(water_level_data_Rio_Grande_Alluvium_2009,pumping_data_Rio_Grande_Alluvium_2009, on ='YEAR', how = 'left' )
Saguache = pd.merge(water_level_data_Saguache_2009,pumping_data_Saguache_2009, on ='YEAR', how = 'left' )
San_Luis = pd.merge(water_level_data_San_Luis_2009,pumping_data_San_Luis_2009, on ='YEAR', how = 'left' )
Subdistrict_1_RA = pd.merge(water_level_data_Subdistrict_1_RA_2009,pumping_data_Subdistrict_1_RA_2009, on ='YEAR', how = 'left' )
Trinchera = pd.merge(water_level_data_Trinchera_2009,pumping_data_Trinchera_2009, on ='YEAR', how = 'left' )



# merging precip and water level/pumping data together
Alamosa_La_Jara = pd.merge(Alamosa_La_Jara,df_Alamosa, on ='YEAR', how = 'left')
Conejos = pd.merge(Conejos,df_conejos, on ='YEAR', how = 'left' )
Rio_Grande_Alluvium = pd.merge(Rio_Grande_Alluvium,df_rio_grande, on ='YEAR', how = 'left' )
Saguache = pd.merge(Saguache,df_Saguache, on ='YEAR', how = 'left' )
Subdistrict_1_RA = pd.merge(Subdistrict_1_RA,df_subdistricts_1RA, on ='YEAR', how = 'left' )
Trinchera = pd.merge(Trinchera,df_Trinchera, on ='YEAR', how = 'left' )

Alamosa_La_Jara['hydraulic_head_change_m'] = Alamosa_La_Jara['hydraulic_head_change_m'].shift(-1)
Conejos['hydraulic_head_change_m'] = Conejos['hydraulic_head_change_m'].shift(-1)
Saguache['hydraulic_head_change_m'] = Saguache['hydraulic_head_change_m'].shift(-1)
Subdistrict_1_RA['hydraulic_head_change_m'] = Subdistrict_1_RA['hydraulic_head_change_m'].shift(-1)

# Removing rows if the column 'ann_amt_m3' has NaN values (and keep other NaNs)
Alamosa_La_Jara = Alamosa_La_Jara.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])
Conejos = Conejos.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])
Rio_Grande_Alluvium = Rio_Grande_Alluvium.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])
Saguache = Saguache.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])
Subdistrict_1_RA = Subdistrict_1_RA.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])
Trinchera = Trinchera.dropna(subset=['hydraulic_head_change_m', 'ann_amt_m3'])

Alamosa_La_Jara = Alamosa_La_Jara[(Alamosa_La_Jara['YEAR'] >2009) & (Alamosa_La_Jara['YEAR'] <2024)]
Conejos = Conejos[(Conejos['YEAR'] >2009) & (Conejos['YEAR'] <2024)]
Saguache = Saguache[(Saguache['YEAR'] >2009) & (Saguache['YEAR'] <2024)]
Subdistrict_1_RA = Subdistrict_1_RA[(Subdistrict_1_RA['YEAR'] >2009) & (Subdistrict_1_RA['YEAR'] <2024)]



# ###################################################
# ### Area
# ###################################################

# obtain area of each region

# change projection to "EPSG:32613" which is "WGS 84 / UTM zone 13N" to get area in m2
area = merged_gdf.to_crs('EPSG:32613')
area['Area_m2'] = area.area

Area = pd.read_csv(r"D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\shapefiles\slv_watersheds\ResponseArea.csv")

# add a new column for site name
Alamosa_La_Jara['Area'] = Area.iloc[0, 8]
Conejos['Area'] = Area.iloc[1, 8]
Rio_Grande_Alluvium['Area'] = Area.iloc[2, 8]
Saguache['Area'] = Area.iloc[3, 8]
Subdistrict_1_RA['Area'] = Area.iloc[4, 8]
Trinchera['Area'] = Area.iloc[5, 8]


'''# calculate head change into area'''
Alamosa_La_Jara['area_into_head_change'] = Alamosa_La_Jara['hydraulic_head_change_m'] * Alamosa_La_Jara['Area'] *-1
Conejos['area_into_head_change'] = Conejos['hydraulic_head_change_m'] * Conejos['Area']*-1
Rio_Grande_Alluvium['area_into_head_change'] = Rio_Grande_Alluvium['hydraulic_head_change_m'] * Rio_Grande_Alluvium['Area']*-1
Saguache['area_into_head_change'] = Saguache['hydraulic_head_change_m'] * Saguache['Area']*-1
Subdistrict_1_RA['area_into_head_change'] = Subdistrict_1_RA['hydraulic_head_change_m'] * Subdistrict_1_RA['Area']*-1
Trinchera['area_into_head_change'] = Trinchera['hydraulic_head_change_m'] * Trinchera['Area']*-1

Alamosa_La_Jara['net_inflow'] = 1
Conejos['net_inflow'] = 1
Rio_Grande_Alluvium['net_inflow'] = 1
Saguache['net_inflow'] = 1
Subdistrict_1_RA['net_inflow'] = 1
Trinchera['net_inflow'] = 1

# keeping needed columns
Alamosa_La_Jara_calc = Alamosa_La_Jara[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()
Conejos_calc = Conejos[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()
Rio_Grande_Alluvium_calc = Rio_Grande_Alluvium[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()
Saguache_calc = Saguache[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()
Subdistrict_1_RA_calc = Subdistrict_1_RA[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()
Trinchera_calc = Trinchera[['area_into_head_change', 'Precip_m3', 'net_inflow', 'ann_amt_m3']].copy()

# 30 year average of precipitation [fetching from df_.... dataframes]
Alamosa_La_Jara_calc['Precip_m3_avg'] = df_Alamosa['Precip_m3'].mean()
Conejos_calc['Precip_m3_avg'] = df_conejos['Precip_m3'].mean()
Rio_Grande_Alluvium_calc['Precip_m3_avg'] = df_rio_grande['Precip_m3'].mean()
Saguache_calc['Precip_m3_avg'] = df_Saguache['Precip_m3'].mean()
Subdistrict_1_RA_calc['Precip_m3_avg'] = df_subdistricts_1RA['Precip_m3'].mean()
Trinchera_calc['Precip_m3_avg'] = df_Trinchera['Precip_m3'].mean()

# Deviation from the average precipitation
Alamosa_La_Jara_calc['Precip_m3_deviation'] = Alamosa_La_Jara_calc['Precip_m3'] - Alamosa_La_Jara_calc['Precip_m3_avg']
Conejos_calc['Precip_m3_deviation'] = Conejos_calc['Precip_m3'] - Conejos_calc['Precip_m3_avg']
Rio_Grande_Alluvium_calc['Precip_m3_deviation'] = Rio_Grande_Alluvium_calc['Precip_m3'] - Rio_Grande_Alluvium_calc['Precip_m3_avg']
Saguache_calc['Precip_m3_deviation'] = Saguache_calc['Precip_m3'] - Saguache_calc['Precip_m3_avg']
Subdistrict_1_RA_calc['Precip_m3_deviation'] = Subdistrict_1_RA_calc['Precip_m3'] - Subdistrict_1_RA_calc['Precip_m3_avg'] 
Trinchera_calc['Precip_m3_deviation'] = Trinchera_calc['Precip_m3'] - Trinchera_calc['Precip_m3_avg']


Alamosa_La_Jara_calc['Precip_m3_deviation'] = Alamosa_La_Jara_calc['Precip_m3_deviation']
Conejos_calc['Precip_m3_deviation'] = Conejos_calc['Precip_m3_deviation']
Rio_Grande_Alluvium_calc['Precip_m3_deviation'] = Rio_Grande_Alluvium_calc['Precip_m3_deviation']
Saguache_calc['Precip_m3_deviation'] = Saguache_calc['Precip_m3_deviation']
Subdistrict_1_RA_calc['Precip_m3_deviation'] = Subdistrict_1_RA_calc['Precip_m3_deviation']
Trinchera_calc['Precip_m3_deviation'] = Trinchera_calc['Precip_m3_deviation']

Alamosa_La_Jara_calc['ann_amt_m3'] = Alamosa_La_Jara_calc['ann_amt_m3']
Conejos_calc['ann_amt_m3'] = Conejos_calc['ann_amt_m3']
Rio_Grande_Alluvium_calc['ann_amt_m3'] = Rio_Grande_Alluvium_calc['ann_amt_m3']
Saguache_calc['ann_amt_m3'] = Saguache_calc['ann_amt_m3']
Subdistrict_1_RA_calc['ann_amt_m3'] = Subdistrict_1_RA_calc['ann_amt_m3']
Trinchera_calc['ann_amt_m3'] = Trinchera_calc['ann_amt_m3']




#############################################################
#################   Alamosa La Jara      ###################
'''Formula: ∆hA×S - I - P×C= -(Pumping-Diversion)'''
#############################################################


import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_breuschpagan

# Independent variables (add a constant column for the intercept)
Alamosa_La_Jara_A = Alamosa_La_Jara_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Alamosa_La_Jara_A = sm.add_constant(Alamosa_La_Jara_A)  # Adds a constant term to the predictor

# Dependent variable
Alamosa_La_Jara_b = Alamosa_La_Jara_calc['ann_amt_m3'].values

# Fit OLS model
model_Alamosa = sm.OLS(Alamosa_La_Jara_b, Alamosa_La_Jara_A)
results_Alamosa = model_Alamosa.fit()
results_Alamosa.params
# Print the results
print(results_Alamosa.summary())



### bootstrapping

import numpy as np
import statsmodels.api as sm
import pandas as pd

# Set the number of bootstrap samples
n_iterations = 1000  # Number of bootstrap samples
bootstrap_estimates = []

# Independent variables (add a constant column for the intercept)
Alamosa_La_Jara_A = Alamosa_La_Jara_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Alamosa_La_Jara_A = sm.add_constant(Alamosa_La_Jara_A)  # Adds a constant term to the predictor

# Dependent variable
Alamosa_La_Jara_b = Alamosa_La_Jara_calc['ann_amt_m3'].values

# Bootstrap process
for i in range(n_iterations):
    # Step 1: Generate a bootstrap sample of size 30 (resample the data with replacement)
    indices = np.random.choice(np.arange(len(Alamosa_La_Jara_b)), size=12, replace=True)
    X_resampled = Alamosa_La_Jara_A[indices]
    y_resampled = Alamosa_La_Jara_b[indices]
    
    # Step 2: Fit the OLS model on the resampled data
    model_bootstrap = sm.OLS(y_resampled, X_resampled)
    results_bootstrap = model_bootstrap.fit()
    
    # Step 3: Store the estimated parameters from the resampled data
    bootstrap_estimates.append(results_bootstrap.params)

# Convert bootstrap estimates into a DataFrame
bootstrap_estimates_df = pd.DataFrame(bootstrap_estimates)

# Calculate the 5th, 50th (median), and 95th percentiles, and the mean for each parameter
param_means = bootstrap_estimates_df.mean()    # Mean of the parameters
param_percentile_5 = bootstrap_estimates_df.quantile(0.05)   # 5th percentile
param_percentile_50 = bootstrap_estimates_df.quantile(0.50)  # 50th percentile (median)
param_percentile_95 = bootstrap_estimates_df.quantile(0.95)  # 95th percentile

# Combine the results into a single dataframe
Alamosa_La_Jara_results = pd.DataFrame({
    'Mean': param_means,
    '5th Percentile': param_percentile_5,
    '50th Percentile (Median)': param_percentile_50,
    '95th Percentile': param_percentile_95
})

# Print the resulting dataframe
print(Alamosa_La_Jara_results)




#############################################################
#################   Saguache      ###################
#############################################################

import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_breuschpagan


# Independent variables (add a constant column for the intercept)
Saguache_A = Saguache_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Saguache_A = sm.add_constant(Saguache_A)  # Adds a constant term to the predictor

# Dependent variable
Saguache_b = Saguache_calc['ann_amt_m3'].values

# Fit OLS model
model_Saguache = sm.OLS(Saguache_b, Saguache_A)
results_Saguache = model_Saguache.fit()

# Print the results
print(results_Saguache.summary())




### bootstrapping

import numpy as np
import statsmodels.api as sm
import pandas as pd

# Set the number of bootstrap samples
n_iterations = 1000  # Number of bootstrap samples
bootstrap_estimates = []

# Independent variables (add a constant column for the intercept)
Saguache_A = Saguache_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Saguache_A = sm.add_constant(Saguache_A)  # Adds a constant term to the predictor

# Dependent variable
Saguache_b = Saguache_calc['ann_amt_m3'].values

# Bootstrap process
for i in range(n_iterations):
    # Step 1: Generate a bootstrap sample (resample the data with replacement)
    indices = np.random.choice(np.arange(len(Saguache_b)), size=30, replace=True)
    X_resampled = Saguache_A[indices]
    y_resampled = Saguache_b[indices]
    
    # Step 2: Fit the OLS model on the resampled data
    model_bootstrap = sm.OLS(y_resampled, X_resampled)
    results_bootstrap = model_bootstrap.fit()
    
    # Step 3: Store the estimated parameters from the resampled data
    bootstrap_estimates.append(results_bootstrap.params)

# Convert bootstrap estimates into a DataFrame
bootstrap_estimates_df = pd.DataFrame(bootstrap_estimates)

# Calculate the 5th, 50th (median), and 95th percentiles, and the mean for each parameter
param_means = bootstrap_estimates_df.mean()    # Mean of the parameters
param_percentile_5 = bootstrap_estimates_df.quantile(0.05)   # 5th percentile
param_percentile_50 = bootstrap_estimates_df.quantile(0.50)  # 50th percentile (median)
param_percentile_95 = bootstrap_estimates_df.quantile(0.95)  # 95th percentile

# Combine the results into a single dataframe
Saguache_results = pd.DataFrame({
    'Mean': param_means,
    '5th Percentile': param_percentile_5,
    '50th Percentile (Median)': param_percentile_50,
    '95th Percentile': param_percentile_95
})

# Print the resulting dataframe
print(Saguache_results)

#############################################################
#################  Subdistricts 1       ###################
#############################################################


import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_breuschpagan


# Independent variables (add a constant column for the intercept)
Subdistrict_1_RA_A = Subdistrict_1_RA_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Subdistrict_1_RA_A = sm.add_constant(Subdistrict_1_RA_A)  # Adds a constant term to the predictor

# Dependent variable
Subdistrict_1_RA_b = Subdistrict_1_RA_calc['ann_amt_m3'].values

# Fit OLS model
model_Subdistrict_1 = sm.OLS(Subdistrict_1_RA_b, Subdistrict_1_RA_A)
results_Subdistrict_1 = model_Subdistrict_1.fit()

# Print the results
print(results_Subdistrict_1.summary())





import numpy as np
import statsmodels.api as sm
import pandas as pd

# Set the number of bootstrap samples
n_iterations = 1000  # Number of bootstrap samples
bootstrap_estimates = []

# Independent variables (add a constant column for the intercept)
Subdistrict_1_RA_A = Subdistrict_1_RA_calc[['area_into_head_change', 'net_inflow', 'Precip_m3_deviation']].values
Subdistrict_1_RA_A = sm.add_constant(Subdistrict_1_RA_A)  # Adds a constant term to the predictor

# Dependent variable
Subdistrict_1_RA_b = Subdistrict_1_RA_calc['ann_amt_m3'].values

# Bootstrap process
for i in range(n_iterations):
    # Step 1: Generate a bootstrap sample (resample the data with replacement)
    indices = np.random.choice(np.arange(len(Subdistrict_1_RA_b)), size=30, replace=True)
    X_resampled = Subdistrict_1_RA_A[indices]
    y_resampled = Subdistrict_1_RA_b[indices]
    
    # Step 2: Fit the OLS model on the resampled data
    model_bootstrap = sm.OLS(y_resampled, X_resampled)
    results_bootstrap = model_bootstrap.fit()
    
    # Step 3: Store the estimated parameters from the resampled data
    bootstrap_estimates.append(results_bootstrap.params)

# Convert bootstrap estimates into a DataFrame
bootstrap_estimates_df = pd.DataFrame(bootstrap_estimates)

# Calculate the 5th, 50th (median), and 95th percentiles, and the mean for each parameter
param_means = bootstrap_estimates_df.mean()    # Mean of the parameters
param_percentile_5 = bootstrap_estimates_df.quantile(0.05)   # 5th percentile
param_percentile_50 = bootstrap_estimates_df.quantile(0.50)  # 50th percentile (median)
param_percentile_95 = bootstrap_estimates_df.quantile(0.95)  # 95th percentile

# Combine the results into a single dataframe
Subdistrict_1_RA_results = pd.DataFrame({
    'Mean': param_means,
    '5th Percentile': param_percentile_5,
    '50th Percentile (Median)': param_percentile_50,
    '95th Percentile': param_percentile_95
})

# Print the resulting dataframe
print(Subdistrict_1_RA_results)





'''
#############################################################
######### 1. OLS Summary DataFrame (Publication Style) ######
#############################################################
'''

import pandas as pd
from statsmodels.iolib.summary2 import summary_col

# Define dictionary of models
models = {
    'Alamosa': results_Alamosa,
    'Saguache': results_Saguache,
    'Subdistrict 1': results_Subdistrict_1
}

# Create the summary object
summary_obj = summary_col(list(models.values()), 
                     stars=True, 
                     float_format='%0.4f',
                     model_names=list(models.keys()),
                     info_dict={'R-squared': lambda x: f"{x.rsquared:.4f}",
                                'Adj. R-squared': lambda x: f"{x.rsquared_adj:.4f}"})

# Convert the Summary object to an actual Pandas DataFrame
df_summary = summary_obj.tables[0]

# Define the mapping from generic numpy names to your actual variable names
# Note: 'const' is usually first. Check your X array order for x1, x2, x3.
rename_map = {
    'const': 'Intercept',
    'x1': 'Area into Head Change',
    'x2': 'Net Inflow',
    'x3': 'Precip Deviation'
}

# Rename the index
df_summary.rename(index=rename_map, inplace=True)

print("### OLS Publication Table ###")
print(df_summary)

'''
#############################################################
######### 2. Bootstrap Results DataFrame ####################
#############################################################
'''
# 1. Define the variable names (MUST include Intercept if sm.add_constant was used)
# This fixes the "Length mismatch" error (3 names vs 4 coefficients)
param_names = ['Intercept', 'Area into Head Change', 'Net Inflow', 'Precip Deviation']

# 2. Helper function to safely assign names even if Intercept is missing
def safe_assign_index(df, names):
    if len(df) == len(names):
        df.index = names
    elif len(df) == len(names) - 1:
        # If intercept is missing from results, use the last 3 names
        df.index = names[1:] 
    return df

# Apply naming
Alamosa_La_Jara_results = safe_assign_index(Alamosa_La_Jara_results, param_names)
Saguache_results = safe_assign_index(Saguache_results, param_names)
Subdistrict_1_RA_results = safe_assign_index(Subdistrict_1_RA_results, param_names)

# 3. Combine them into one DataFrame using a MultiIndex
df_bootstrap = pd.concat(
    [Alamosa_La_Jara_results, Saguache_results, Subdistrict_1_RA_results],
    keys=['Alamosa La Jara', 'Saguache', 'Subdistrict 1'],
    names=['Region', 'Parameter']
)

print("\n### Combined Bootstrap Results ###")
pd.set_option('display.max_rows', None)
print(df_bootstrap)

# Optional: Export both to CSV
# df_summary.to_csv("OLS_Comparison.csv")
# df_bootstrap.to_csv("Bootstrap_Comparison.csv")


'''
#############################################################
################# P Values ############
#############################################################
'''

# 1. Define the models and variable names
models = {
    'Alamosa': results_Alamosa,
    'Saguache': results_Saguache,
    'Subdistrict 1': results_Subdistrict_1
}

# Standardized names (Ensure 'Intercept' is first if you used sm.add_constant)
param_names = ['Intercept', 'Area into Head Change', 'Net Inflow', 'Precip Deviation']

# 2. Helper function to create a clean DataFrame for one model
def get_model_stats(result, names):
    # Extract Coef and P-value
    df = pd.DataFrame({
        'Coef': result.params,
        'P-Value': result.pvalues
    })
    
    # Handle naming (Safety check for 3 vs 4 variables)
    if len(df) == len(names):
        df.index = names
    elif len(df) == len(names) - 1:
        df.index = names[1:] # Skip intercept if missing
    else:
        df.index = [f"Var {i}" for i in range(len(df))]
        
    # Create a "Significance" column based on P-value
    df['Sig.'] = df['P-Value'].apply(lambda p: '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else '')))
    
    return df

# 3. Build the combined DataFrame
dfs = []
for region, res in models.items():
    dfs.append(get_model_stats(res, param_names))

# Concatenate with MultiIndex (Region -> Metric)
df_summary_pvals = pd.concat(dfs, axis=1, keys=models.keys())

# 4. Formatting for cleaner display
pd.set_option('display.float_format', '{:.4f}'.format)

print("### OLS Results with P-Values ###")
print(df_summary_pvals)

# 5. Optional: Add Model-Level Stats (R-Squared) at the bottom
r2_data = {
    (name, 'R-Squared'): res.rsquared 
    for name, res in models.items()
}
# Create a row for R2 and append (Note: requires matching columns)
# This step is optional if you only care about coefficients.

