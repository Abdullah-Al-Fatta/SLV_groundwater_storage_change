# Configuration File for SLV Groundwater Analysis
# Copy this file to 'config.py' and update paths for your system

import os
from pathlib import Path

# Base directory (automatically detected)
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
SHAPEFILE_DIR = DATA_DIR / 'shapefiles'
PUMPING_DIR = DATA_DIR / 'pumping'
WATER_LEVEL_DIR = DATA_DIR / 'water_levels'
CLIMATE_DIR = DATA_DIR / 'climate'
SUBSIDENCE_DIR = DATA_DIR / 'subsidence'

# Output directories
FIGURES_DIR = BASE_DIR / 'figures'
RESULTS_DIR = BASE_DIR / 'results'

# Create directories if they don't exist
for directory in [DATA_DIR, FIGURES_DIR, RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ==================== FILE PATHS ====================

# Shapefiles
RESPONSE_AREAS_SHP = SHAPEFILE_DIR / 'Response_Areas_2014_1_21.shp'

# Watershed shapefiles (for precipitation extraction)
WATERSHEDS = {
    'Alamosa_La_Jara': SHAPEFILE_DIR / 'slv_watersheds' / 'Alamosa_La_Jara_watershed.shp',
    'Conejos': SHAPEFILE_DIR / 'slv_watersheds' / 'conejos_watershed.shp',
    'Rio_Grande': SHAPEFILE_DIR / 'slv_watersheds' / 'rio_grande_watershed.shp',
    'Saguache': SHAPEFILE_DIR / 'slv_watersheds' / 'Saguache_watershed.shp',
    'Subdistrict_1': SHAPEFILE_DIR / 'slv_watersheds' / 'subdistrict1_watershed.shp',
    'Trinchera': SHAPEFILE_DIR / 'slv_watersheds' / 'Trinchera_watershed.shp',
}

# InSAR boundary shapefiles
INSAR_BOUNDARIES = {
    'Alamosa': SHAPEFILE_DIR / 'Alamosa___La_Jara.shp',
    'Saguache': SHAPEFILE_DIR / 'Saguache_InSAR_Boundary.shp',
    'Subdistrict_1': SHAPEFILE_DIR / 'Subdistrict_1_RA.shp',
}

# Pumping data
PUMPING_DATA = PUMPING_DIR / '20250805_merged_diversion_records.csv'
PUMPING_DATA_OLD = PUMPING_DIR / 'pumping_data.csv'

# Water level data
WATER_LEVEL_DATA = WATER_LEVEL_DIR / '20251030_merged_wl_data.csv'

# Climate data
PRECIPITATION_DATA = CLIMATE_DIR / 'combined_precipitation_waterYear_20250922.csv'
WATERSHED_AREA_DATA = SHAPEFILE_DIR / 'slv_watersheds' / 'area.csv'

# Subsidence data
SUBSIDENCE_RASTER = SUBSIDENCE_DIR / 'geotiff_map_fine.tiff'

# Surface water diversion data
DIVERSION_DATA = DATA_DIR / 'Diversion_data_m3.csv'

# Storage change results
STORAGE_CHANGE_DATA = DATA_DIR / '20251110_final_storage_change_data.csv'
STORAGE_CHANGE_WITH_SUBSIDENCE = DATA_DIR / '20251110_final_storage_change_data_with_subsidence.csv'

# ==================== ANALYSIS PARAMETERS ====================

# Coordinate reference systems
CRS_WGS84 = 'EPSG:4326'  # Lat/Lon
CRS_UTM13N = 'EPSG:32613'  # UTM Zone 13N (meters)
CRS_NAD83_UTM13N = 'EPSG:26913'  # NAD83 UTM Zone 13N

# Unit conversions
ACRE_FEET_TO_M3 = 1233.48
FEET_TO_METERS = 0.3048
MM_TO_METERS = 0.001

# Response area names
RESPONSE_AREAS = [
    'Alamosa / La Jara',
    'Conejos',
    'Closed Basin Project',
    'Costilla',
    'Rio Grande Alluvium',
    'Saguache',
    'San Luis',
    'Subdistrict 1 RA',
    'Trinchera',
]

# Analysis time period
START_YEAR = 2009
END_YEAR = 2024

# InSAR analysis parameters
INSAR_START_YEAR = 2015
INSAR_END_YEAR = 2022
INSAR_OBSERVATION_PERIOD = 8  # years

# Subsidence to storage conversion factor
# Assumes: Skeletal specific storage * compressible thickness ≈ 0.001
SUBSIDENCE_CONVERSION_FACTOR = 0.001

# Regression parameters
BOOTSTRAP_ITERATIONS = 1000
CONFIDENCE_LEVEL = 0.95

# Plotting parameters
FIGURE_DPI = 300
FIGURE_FORMAT = 'png'

# ==================== GOOGLE EARTH ENGINE ====================

# Earth Engine asset names (if applicable)
EE_PRISM_COLLECTION = "OREGONSTATE/PRISM/AN81m"
EE_PRISM_BAND = 'ppt'

# ==================== VALIDATION PARAMETERS ====================

# Quality control thresholds
MAX_HEAD_CHANGE_PER_YEAR = 5.0  # meters (flag outliers)
MIN_WELLS_PER_REGION = 5
MIN_MEASUREMENTS_PER_YEAR = 3

# Expected parameter ranges (for validation)
STORATIVITY_RANGE = (1e-6, 0.3)
RECHARGE_COEFF_RANGE = (0.0, 0.3)

# ==================== OUTPUT OPTIONS ====================

# Save intermediate results
SAVE_INTERMEDIATE = True
SAVE_FIGURES = True

# Figure output directories
STORAGE_FIGURES = FIGURES_DIR / 'storage_change'
DIVERSION_FIGURES = FIGURES_DIR / 'diversions'
REGRESSION_FIGURES = FIGURES_DIR / 'regression'
SUBSIDENCE_FIGURES = FIGURES_DIR / 'subsidence'

for fig_dir in [STORAGE_FIGURES, DIVERSION_FIGURES, REGRESSION_FIGURES, SUBSIDENCE_FIGURES]:
    fig_dir.mkdir(parents=True, exist_ok=True)

# ==================== LOGGING ====================

# Log file location
LOG_FILE = BASE_DIR / 'analysis.log'
LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# ==================== HELPER FUNCTIONS ====================

def get_path(path):
    """Convert Path object to string for compatibility with older code."""
    return str(path)

def check_file_exists(filepath, description="File"):
    """Check if a file exists and raise error if not."""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"{description} not found: {filepath}")
    return True

def validate_config():
    """Validate that all required paths exist."""
    required_files = {
        'Response areas shapefile': RESPONSE_AREAS_SHP,
        'Pumping data': PUMPING_DATA,
        'Water level data': WATER_LEVEL_DATA,
        'Precipitation data': PRECIPITATION_DATA,
    }
    
    missing_files = []
    for description, filepath in required_files.items():
        if not Path(filepath).exists():
            missing_files.append(f"{description}: {filepath}")
    
    if missing_files:
        print("⚠️  Warning: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease update the paths in config_example.py and save as config.py")
        return False
    
    print("✓ Configuration validated successfully!")
    return True

# ==================== USAGE ====================

if __name__ == "__main__":
    print("SLV Groundwater Analysis Configuration")
    print("=" * 50)
    print(f"Base directory: {BASE_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Figures directory: {FIGURES_DIR}")
    print()
    validate_config()
