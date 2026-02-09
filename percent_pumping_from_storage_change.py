"""
Created on Wed Sep 24 10:34:49 2025

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
    # gdf = gdf[gdf['irr_year'] > 2009]

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

plt.plot(pumping_data_Alamosa_La_Jara['irr_year'], pumping_data_Alamosa_La_Jara['ann_amt_m3'])
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


# merging pumping and water level data together
Alamosa_La_Jara = pumping_data_Alamosa_La_Jara_2009.copy()
Saguache = pumping_data_Saguache_2009.copy()
Subdistrict_1_RA = pumping_data_Subdistrict_1_RA_2009.copy()

# year constraint
Alamosa_La_Jara = Alamosa_La_Jara[Alamosa_La_Jara['YEAR'] <2024]
Saguache = Saguache[Saguache['YEAR'] <2024]
Subdistrict_1_RA = Subdistrict_1_RA[Subdistrict_1_RA['YEAR'] <2024]

'''
# =============================================================================
# # Comparision with storage change
# =============================================================================
'''

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Load & filter storage-change table ---
final_storage_change_data = pd.read_csv(
    r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\20251110_final_storage_change_data.csv'
)
final_storage_change_data = final_storage_change_data[final_storage_change_data['YEAR'] < 2024]

# --- Ensure pumping data are filtered ---
Alamosa_La_Jara  = Alamosa_La_Jara[Alamosa_La_Jara['YEAR'] < 2024]
Saguache         = Saguache[Saguache['YEAR'] < 2024]
Subdistrict_1_RA = Subdistrict_1_RA[Subdistrict_1_RA['YEAR'] < 2024]

# --- Output folder ---
out_dir = Path(r'D:\OneDrive - Colostate\Al Fatta Smith\Writing\Final_data_20250512\Figures_20251106\Storage_vs_pumping')
out_dir.mkdir(parents=True, exist_ok=True)

# --- Areas to plot (title, storage-col, pumping-df, y-limits) ---
areas = [
    ('Alamosa / La Jara', 'Alamosa / La Jara', Alamosa_La_Jara,  (-1e8, 2.5e8)),
    ('Saguache',          'Saguache',          Saguache,         (-0.5e8, 1e8)),
    ('Subdistrict 1 RA',  'Subdistrict 1 RA',  Subdistrict_1_RA, (-3e8, 6e8)),
]

# --- Make 3-panel figure ---
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(9, 12), sharex=True)

for ax, (title, storage_col, pump_df, (ymin, ymax)) in zip(axes, areas):
    ax.plot(final_storage_change_data['YEAR'], final_storage_change_data[storage_col],
            '-o', label='Storage change (m³)')
    ax.plot(pump_df['YEAR'], pump_df['ann_amt_m3'],
            '-o', label='Pumping (m³)')
    ax.set_title(title)
    ax.set_ylabel("m³")
    ax.set_ylim(ymin, ymax)
    ax.legend(loc='upper left')

# Common x-axis label
axes[-1].set_xlabel("Year")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# # --- Save ---
# base = "storage_vs_pumping_3panel_customY"
# fig.savefig(out_dir / f"{base}_20250916.png",  dpi=300, bbox_inches='tight')
# fig.savefig(out_dir / f"{base}_20250916.tiff", dpi=300, bbox_inches='tight',
#             format='tiff', pil_kwargs={"compression": "tiff_lzw"})

plt.show()
plt.close(fig)



# =============================================================================
# Final - 20250929_avg_storage_vs_avg_pumping_final
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from pathlib import Path

# ==== layout & typography ====
FULL_WIDTH_IN = 9
FIG_HEIGHT_IN = 4.4
TITLE_FS = 16
TITLE_Y  = 1.06       # force-aligned titles
LABEL_FS = 14
TICK_FS  = 14
ANN_FS   = 12
BAR_WIDTH = 0.70
SHARED_YMAX_PAD = 1.25

# ==== output ====
OUT_DIR = Path(r'D:\OneDrive - Colostate\Al Fatta Smith\Code\3 2 2023\updated_codes\Journal of Hydrology\Datasets\Figures\Storage_vs_pumping')
BASE    = "avg_storage_vs_avg_pumping__final"
PREFIX  = "20251111_"

# --- helpers for multi-line labels ---
def storage_label_text(is_gain: bool) -> str:
    # Two lines: phrase on line 1, units on line 2
    return "Avg Gain\n(m³/yr)" if is_gain else "Avg Storage \nLoss(m³/yr)"

def pumping_label_text(key: str) -> str:
    if key == 'Subdistrict_1_RA':
        # Three lines for Subdistrict 1
        return "Avg Net \nPumping(m³/yr)"
    return "Avg Pumping\n(m³/yr)"

def sci_text(val: float, sig: int = 3) -> str:
    """Format number like 1.23×10^8 (LaTeX-ish) for bar annotations."""
    if not np.isfinite(val) or abs(val) < 1e-15:
        return r"$0$"
    v = abs(val)
    exp = int(np.floor(np.log10(v)))
    coeff = v / (10 ** exp)
    dec = max(0, sig - 1)
    return rf"${coeff:.{dec}f}\times10^{{{exp}}}$"

def _assert_has_cols(df: pd.DataFrame, cols, name: str):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")

def _ensure_year_int(df: pd.DataFrame) -> pd.DataFrame:
    if 'YEAR' in df.columns:
        df = df.copy()
        df['YEAR'] = df['YEAR'].astype(int)
    return df

def mean_pumping(df: pd.DataFrame, key: str, years: list[int]) -> float:
    """Return mean pumping across 'years'. Subdistrict 1 uses Net Pumping when available."""
    dfi = df.set_index('YEAR')
    # Choose series
    if key == 'Subdistrict_1_RA':
        if 'net_pumping_m3' in dfi.columns:
            s = dfi['net_pumping_m3']
        elif {'ann_amt_m3', 'diversions_m3'}.issubset(dfi.columns):
            s = dfi['ann_amt_m3'] - dfi['diversions_m3']
        else:
            _assert_has_cols(dfi.reset_index(), ['ann_amt_m3'], key)
            s = dfi['ann_amt_m3']
    else:
        # common column names
        for col in ('ann_amt_m3', 'pumping_m3', 'pump_m3', 'pumping'):
            if col in dfi.columns:
                s = dfi[col]
                break
        else:
            raise KeyError(f"No pumping column found in {key} (tried ann_amt_m3 / pumping_m3 / pump_m3 / pumping).")
    return float(s.reindex(years).astype(float).mean(skipna=True))

def build_and_save_figure(final_storage_change_data: pd.DataFrame,
                          Alamosa_La_Jara: pd.DataFrame,
                          Saguache: pd.DataFrame,
                          Subdistrict_1_RA: pd.DataFrame,
                          year_min: int | None = None,
                          year_max: int | None = None):
    """
    final_storage_change_data columns expected:
      'YEAR', 'Alamosa / La Jara', 'Saguache', 'Subdistrict 1 RA', ...
    """

    # ---- Normalize and filter years ----
    fs = _ensure_year_int(final_storage_change_data.copy())
    Alamosa_La_Jara  = _ensure_year_int(Alamosa_La_Jara)
    Saguache         = _ensure_year_int(Saguache)
    Subdistrict_1_RA = _ensure_year_int(Subdistrict_1_RA)

    # By default, keep all years < 2024 (matches your sample)
    if year_min is None:
        year_min = int(fs['YEAR'].min())
    if year_max is None:
        year_max = min(2023, int(fs['YEAR'].max()))

    fs = fs[(fs['YEAR'] >= year_min) & (fs['YEAR'] <= year_max)].copy()
    Alamosa_La_Jara  = Alamosa_La_Jara[(Alamosa_La_Jara['YEAR']  >= year_min) & (Alamosa_La_Jara['YEAR']  <= year_max)]
    Saguache         = Saguache[(Saguache['YEAR']                 >= year_min) & (Saguache['YEAR']         <= year_max)]
    Subdistrict_1_RA = Subdistrict_1_RA[(Subdistrict_1_RA['YEAR']>= year_min) & (Subdistrict_1_RA['YEAR'] <= year_max)]

    # ---- Map our keys to the storage columns in final_storage_change_data ----
    storage_col_map = {
        'Alamosa_La_Jara': 'Alamosa / La Jara',
        'Saguache':         'Saguache',
        'Subdistrict_1_RA': 'Subdistrict 1 RA',
    }
    _assert_has_cols(fs, ['YEAR'] + list(storage_col_map.values()), 'final_storage_change_data')

    # ---- Compute mean storage and mean pumping (aligned by intersection years per area) ----
    pump_dfs = {
        'Alamosa_La_Jara': Alamosa_La_Jara,
        'Saguache':         Saguache,
        'Subdistrict_1_RA': Subdistrict_1_RA,
    }

    storage_bar: dict[str, float] = {}
    storage_is_gain: dict[str, bool] = {}
    pump_means: dict[str, float] = {}

    for key, stor_col in storage_col_map.items():
        years_storage = set(fs['YEAR'])
        years_pump    = set(pump_dfs[key]['YEAR'])
        years = sorted(years_storage & years_pump) or sorted(years_storage | years_pump)

        # Mean storage change over these years
        s_mean = float(fs.set_index('YEAR')[stor_col].reindex(years).astype(float).mean(skipna=True))
        if s_mean < 0:
            storage_bar[key] = -s_mean     # loss magnitude
            storage_is_gain[key] = False
        else:
            storage_bar[key] =  s_mean     # gain magnitude
            storage_is_gain[key] = True

        # Mean pumping (net where applicable) over the same years
        pump_means[key] = mean_pumping(pump_dfs[key], key, years)

    # ---- Plot ----
    panels = [
        ('Alamosa / La Jara', 'Alamosa_La_Jara'),
        ('Saguache',          'Saguache'),
        ('Subdistrict 1',     'Subdistrict_1_RA'),
    ]

    all_vals = [*storage_bar.values(), *pump_means.values()]
    ymin = 0.0
    ymax = (max(all_vals) * SHARED_YMAX_PAD) if all_vals else 1.0

    fig, axes = plt.subplots(1, 3, figsize=(FULL_WIDTH_IN, FIG_HEIGHT_IN), constrained_layout=False)

    COLOR_STORAGE = "#4C78A8"
    COLOR_PUMPING = "#F58518"
    COLOR_GAIN_SAGUACHE = "#2E7D32"

    for ax, (title, key) in zip(axes, panels):
        vals = [float(storage_bar[key]), float(pump_means[key])]
        labels = [storage_label_text(storage_is_gain[key]), pumping_label_text(key)]
        x = np.array([0, 1], dtype=float)

        # storage color: green only if Saguache has gain
        storage_color = COLOR_GAIN_SAGUACHE if (key == 'Saguache' and storage_is_gain[key]) else COLOR_STORAGE

        bars = ax.bar(
            x, vals, width=BAR_WIDTH, alpha=0.9,
            color=[storage_color, COLOR_PUMPING],
            edgecolor='black', linewidth=0.6
        )

        # Titles / labels
        ax.set_title(title, fontsize=TITLE_FS, y=TITLE_Y)
        ax.set_ylabel("m³/yr", fontsize=LABEL_FS)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=LABEL_FS, linespacing=1.1)
        for tl in ax.get_xticklabels():
            tl.set_ha('center')

        # Y axis: scientific notation (consistent across panels)
        fmt = ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((0, 0))   # force sci notation
        ax.yaxis.set_major_formatter(fmt)
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        ax.tick_params(axis='y', labelsize=TICK_FS)

        ax.set_ylim(ymin, ymax)
        ax.axhline(0, color='k', lw=0.8)

        # Clean frame
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Bar-top annotations
        for rect, v in zip(bars, vals):
            ax.annotate(
                sci_text(v, sig=3),
                xy=(rect.get_x() + rect.get_width()/2, v),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=ANN_FS, clip_on=False
            )

    # spacing for multi-line x labels and even titles
    # plt.subplots_adjust(left=0.075, right=0.99, top=0.90, bottom=0.34, wspace=0.35)
    plt.subplots_adjust(left=0.075, right=0.99, top=0.88, bottom=0.42, wspace=0.40)

    # ---- Save ----
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path  = OUT_DIR / f"{PREFIX}{BASE}.pdf"
    tiff_path = OUT_DIR / f"{PREFIX}{BASE}.tiff"
    pdf_path.unlink(missing_ok=True)
    tiff_path.unlink(missing_ok=True)

    # fig.savefig(pdf_path, bbox_inches='tight')
    # fig.savefig(
    #     tiff_path, dpi=600, bbox_inches='tight',
    #     format='tiff', pil_kwargs={"compression": "tiff_lzw"}
    # )
    plt.show()

# === Usage ===
# Ensure these DataFrames exist: final_storage_change_data, Alamosa_La_Jara, Saguache, Subdistrict_1_RA
build_and_save_figure(final_storage_change_data, Alamosa_La_Jara, Saguache, Subdistrict_1_RA)

