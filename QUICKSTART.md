# Quick Start Guide

Get up and running with the San Luis Valley groundwater depletion analysis in 15 minutes.

## Prerequisites

- Python 3.8 or higher
- Git
- Google Earth Engine account (for precipitation analysis)
- 10 GB free disk space (for datasets)

## Step 1: Clone and Setup (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/slv-groundwater-depletion.git
cd slv-groundwater-depletion

# Create conda environment (recommended)
conda env create -f environment.yml
conda activate slv-groundwater

# OR use pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Configure Paths (3 minutes)

```bash
# Copy example config
cp config_example.py config.py

# Edit config.py to update file paths
# Use your favorite text editor
nano config.py  # or vim, emacs, vscode, etc.
```

**Key paths to update:**
```python
# Change these in config.py
DATA_DIR = Path('/your/path/to/data')
SHAPEFILE_DIR = DATA_DIR / 'shapefiles'
# ... update other paths as needed
```

## Step 3: Download Data (5 minutes)

### Required Data:

1. **Shapefiles** (included in repository):
   - Response area boundaries
   - Watershed polygons

2. **Pumping Data** (contact RGWCD or use example data):
   ```bash
   # Place in data/pumping/
   cp /path/to/pumping_data.csv data/pumping/
   ```

3. **Water Level Data** (download from USGS):
   ```python
   # Use USGS NWIS web service
   from dataretrieval import nwis
   
   # Example for San Luis Valley
   site_list = ['384725105580701', '384634105553801', ...]  # USGS site numbers
   wl_data = nwis.get_gwlevels(sites=site_list, start='2009-01-01')
   wl_data.to_csv('data/water_levels/usgs_water_levels.csv')
   ```

4. **Optional - InSAR Data** (large files, see DATA.md):
   - Not included in repository
   - Available from NASA ASF DAAC
   - Contact authors for processed rasters

## Step 4: Run Your First Analysis (2 minutes)

### Example 1: Diversion Plots

```bash
# Simple visualization - no external data needed
python scripts/diversion_plots.py
```

**Expected output:**
- Figure showing annual diversions by month
- Figure showing total monthly diversions

### Example 2: Storage Change Calculation

```bash
# Calculate storage change from water levels
python scripts/storage_change_calc.py
```

**What it does:**
1. Loads monitoring well data
2. Clips wells to response areas
3. Calculates annual mean head changes
4. Estimates storage change
5. Produces time-series plots

**Expected output:**
```
Processing Alamosa / La Jara...
  Wells found: 45
  Years analyzed: 2009-2024
  Mean storativity: 0.00082
  
Processing Saguache...
  Wells found: 32
  Years analyzed: 2009-2024
  Mean storativity: 0.00095
  
[... continues for each subdistrict]

Figures saved to: figures/storage_change/
```

## Basic Workflow

### Complete Analysis Pipeline:

```bash
# 1. Process diversions
python scripts/diversion_plots.py

# 2. Calculate storage from water levels
python scripts/storage_change_calc.py

# 3. Add subsidence component (if InSAR data available)
python scripts/storage_change_calc_from_subsidence.py

# 4. Determine aquifer properties
python scripts/storativity_precip_coeff_inflow_determination.py

# 5. Analyze pumping contributions
python scripts/percent_pumping_from_storage_change.py
```

## Quick Examples

### Example: Calculate Storage for One Subdistrict

```python
import pandas as pd
import geopandas as gpd
from scripts.storage_change_calc import process_pumping_data, process_water_level_data

# Load data
pumping = gpd.read_file('data/pumping/pumping_data.shp')
alamosa = gpd.read_file('data/shapefiles/Alamosa.shp')

# Process
result = process_pumping_data(pumping, alamosa)
print(result)
```

### Example: Extract Precipitation

```python
import ee
from scripts.storativity_precip_coeff_inflow_determination import calculate_annual_rainfall

ee.Initialize()

rainfall = calculate_annual_rainfall(
    'data/shapefiles/slv_watersheds/Alamosa_La_Jara_watershed.shp',
    start_year=2010,
    end_year=2020
)
print(rainfall)
```

### Example: Simple Storage Calculation

```python
# Manual calculation
head_change = -0.5  # meters (decline)
area = 1e9  # square meters (1000 km²)
storativity = 0.001

storage_change = head_change * area * storativity
print(f"Storage loss: {storage_change:.2e} m³")
# Output: Storage loss: -5.00e+05 m³
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

```bash
# Solution: Install missing package
pip install <package-name>

# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 2: Google Earth Engine Authentication

```bash
# Solution: Authenticate
earthengine authenticate

# Then in Python
import ee
ee.Initialize()
```

### Issue 3: File Path Errors

```python
# Solution: Use absolute paths or Path objects
from pathlib import Path

data_file = Path(__file__).parent / 'data' / 'pumping_data.csv'
df = pd.read_csv(data_file)
```

### Issue 4: Coordinate System Mismatch

```python
# Solution: Reproject to common CRS
import geopandas as gpd

gdf1 = gpd.read_file('file1.shp')
gdf2 = gpd.read_file('file2.shp')

# Ensure both use WGS84
gdf1 = gdf1.to_crs(epsg=4326)
gdf2 = gdf2.to_crs(epsg=4326)
```

### Issue 5: Memory Error with Large Datasets

```python
# Solution: Process in chunks
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process chunk
    process_data(chunk)
```

## Verification

Check that everything is working:

```bash
# Run test suite (if available)
pytest tests/

# Run configuration validator
python config.py
```

Expected output:
```
✓ Configuration validated successfully!
✓ All required files found
✓ Python environment configured correctly
```

## Next Steps

1. **Read the documentation:**
   - [`DATA.md`](docs/DATA.md) - Understanding datasets
   - [`METHODS.md`](docs/METHODS.md) - Analysis methodology
   - [`API.md`](docs/API.md) - Function reference

2. **Explore the scripts:**
   - Add print statements to understand data flow
   - Modify parameters for your analysis
   - Create custom visualizations

3. **Customize the analysis:**
   - Focus on specific subdistricts
   - Add new climate variables
   - Integrate additional datasets

4. **Contribute:**
   - Report bugs via GitHub Issues
   - Submit improvements via Pull Requests
   - See [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Getting Help

- **GitHub Issues:** Report bugs or request features
- **Discussions:** Ask questions in GitHub Discussions
- **Email:** contact the maintainer for specific questions
- **Documentation:** Check docs/ directory for detailed guides

## Useful Commands

```bash
# List all available datasets
ls -lh data/

# Check Python package versions
pip list | grep -E 'pandas|geopandas|rasterio'

# View script help (if implemented)
python scripts/storage_change_calc.py --help

# Generate a requirements file for your environment
pip freeze > my_requirements.txt
```

## Example Output

After running the complete analysis, you should have:

```
figures/
├── storage_change/
│   ├── Alamosa_storage_timeseries.png
│   ├── Saguache_storage_timeseries.png
│   └── all_subdistricts_comparison.png
├── diversions/
│   └── monthly_diversions.png
├── regression/
│   ├── storativity_estimates.png
│   └── regression_diagnostics.png
└── subsidence/
    └── cumulative_subsidence_storage.png

results/
├── storage_change_summary.csv
├── storativity_estimates.csv
└── pumping_contribution_analysis.csv
```

## Troubleshooting Checklist

- [ ] Python version ≥ 3.8
- [ ] All dependencies installed
- [ ] Google Earth Engine authenticated (if needed)
- [ ] File paths updated in config.py
- [ ] Required data files present
- [ ] Shapefiles have .shp, .shx, .dbf, .prj files
- [ ] Coordinate systems are consistent
- [ ] Sufficient disk space available

---

**You're ready to go!** 🚀

For detailed analysis instructions, see the full [README.md](README.md).

For methodology details, see [METHODS.md](docs/METHODS.md).
