# Quantifying Groundwater Depletion in an Agricultural Region Using Integrated In-Situ and Satellite-Based Approaches: Insights from the San Luis Valley, CO

[![DOI](https://img.shields.io/badge/DOI-10.xxxx%2Fxxxxxx-blue)](https://doi.org/10.xxxx/xxxxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

This repository contains Python scripts and datasets for quantifying groundwater storage change in the San Luis Valley (SLV), Colorado, using an integrated approach combining in-situ measurements and satellite-based remote sensing. The study employs water-level observations, pumping records, InSAR-derived land subsidence data, and climate variables to characterize groundwater depletion across multiple subdistricts.

**Key Features:**
- Water balance modeling with time-varying recharge coefficients
- InSAR-based subsidence analysis for fine-grained aquifer compaction
- Multivariate regression for storativity and recharge estimation
- Integration of PRISM precipitation
- Comparative analysis across nine response areas in the SLV

## Study Area

The San Luis Valley is a hydrologic basin in south-central Colorado covering approximately 8,000 km². The study focuses on groundwater systems within the Rio Grande Water Conservation District, encompassing:

- **Alamosa/La Jara**: Confined aquifer system
- **Saguache**: Northern portion with mixed confined/unconfined conditions
- **Subdistrict 1 RA**: Eastern region with significant subsidence
- **Additional areas**: Conejos, Costilla, Rio Grande Alluvium, San Luis, Trinchera, Closed Basin Project

## Repository Structure

```
slv-groundwater-depletion/
│
├── scripts/                              # Python analysis scripts
│   ├── storage_change_calc.py           # Main storage change estimation
│   ├── storage_change_calc_from_subsidence.py  # InSAR-based analysis
│   ├── storativity_precip_coeff_inflow_determination.py  # Regression analysis
│   ├── percent_pumping_from_storage_change.py  # Pumping contribution analysis
│   └── diversion_plots.py               # Surface water diversion visualization
│
├── data/                                 # Input datasets (see DATA.md)
│   ├── shapefiles/                      # Response areas and watershed boundaries
│   ├── pumping/                         # Groundwater pumping records
│   ├── water_levels/                    # USGS monitoring well data
│   ├── climate/                         # PRISM precipitation data
│   └── subsidence/                      # InSAR displacement rasters
│
├── figures/                              # Output visualizations
│   ├── storage_change/                  # Storage change time series
│   ├── diversions/                      # Surface water plots
│   └── regression/                      # Statistical model outputs
│
├── docs/                                 # Documentation
│   ├── DATA.md                          # Data sources and processing
│   ├── METHODS.md                       # Detailed methodology
│   └── API.md                           # Script function reference
│
├── tests/                                # Unit tests
│   └── test_storativity_precip_coeff_inflow_determination.py
│
├── requirements.txt                      # Python dependencies
├── environment.yml                       # Conda environment file
├── .gitignore                           # Git ignore rules
├── LICENSE                              # MIT License
└── README.md                            # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Anaconda or Miniconda (recommended)
- Google Earth Engine account (for precipitation data extraction)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/slv-groundwater-depletion.git
cd slv-groundwater-depletion
```

2. **Create conda environment:**
```bash
conda env create -f environment.yml
conda activate slv-groundwater
```

Or use pip:
```bash
pip install -r requirements.txt
```

3. **Configure Google Earth Engine (for precipitation analysis):**
```bash
earthengine authenticate
```

4. **Update file paths:**
Edit the file paths in each script to match your local directory structure. All scripts use absolute paths that need to be modified.

## Quick Start

### 1. Estimate Storage Change from Water Levels

```bash
python scripts/storage_change_calc.py
```

This script:
- Clips monitoring wells to response area boundaries
- Calculates annual mean hydraulic head changes
- Integrates pumping data to estimate storage change
- Produces storage change time series for each subdistrict

**Key outputs:**
- `20251110_final_storage_change_data.csv`
- Storage change plots by subdistrict

### 2. Calculate Subsidence-Derived Storage Change

```bash
python scripts/storage_change_calc_from_subsidence.py
```

This script:
- Masks InSAR subsidence rasters using subdistrict polygons
- Converts vertical displacement to volumetric storage change
- Combines fine-grained and coarse-grained storage estimates

**Key outputs:**
- Percentage contribution of subsidence to total storage loss
- Cumulative storage change plots

### 3. Determine Aquifer Properties

```bash
python scripts/storativity_precip_coeff_inflow_determination.py
```

This script:
- Extracts PRISM precipitation data for each watershed
- Performs multivariate OLS regression: ΔS = S·A·Δh - α·P + Q
- Estimates storativity, precipitation coefficient, and net inflow
- Uses bootstrap resampling for uncertainty quantification

**Key outputs:**
- Storativity estimates for each subdistrict
- Precipitation recharge coefficients
- Regression diagnostics and confidence intervals

### 4. Analyze Pumping Contributions

```bash
python scripts/percent_pumping_from_storage_change.py
```

This script:
- Aggregates annual pumping volumes by subdistrict
- Compares pumping to independently estimated storage change
- Quantifies closure of the water budget

### 5. Visualize Diversions

```bash
python scripts/diversion_plots.py
```

Creates stacked bar plots of surface water diversions over time.

## Data Requirements

The analysis requires the following datasets (see `docs/DATA.md` for details):

1. **Shapefiles:**
   - Response area boundaries (`Response_Areas_2014_1_21.shp`)
   - Watershed polygons for precipitation extraction
   - InSAR coverage boundaries

2. **Groundwater Pumping:**
   - Annual pumping records by well location (acre-feet)
   - Converted to cubic meters in scripts

3. **Water Level Data:**
   - USGS National Water Information System (NWIS) data
   - Monitoring well measurements (daily to monthly)

4. **Climate Data:**
   - PRISM monthly precipitation (water-year totals)
   - Extracted via Google Earth Engine

5. **InSAR Subsidence:**
   - GeoTIFF raster of mean vertical displacement (2015-2022)
   - Sentinel-1 derived displacement maps

6. **Surface Water Diversions:**
   - Monthly diversion records (cubic meters)
   - Used to adjust pumping in Subdistrict 1

## Methodology

The analysis employs a water balance approach:

```
ΔS = S·A·Δh - α·P + Q - R
```

Where:
- **ΔS**: Change in groundwater storage (m³)
- **S**: Storativity (dimensionless)
- **A**: Aquifer area (m²)
- **Δh**: Change in hydraulic head (m)
- **α**: Precipitation recharge coefficient
- **P**: Precipitation volume (m³)
- **Q**: Net groundwater inflow (m³)
- **R**: Pumping (m³)

### Key Steps:

1. **Hydraulic Head Analysis:** Calculate mean annual head change from kriged water-level surfaces
2. **Precipitation Processing:** Extract water-year precipitation totals for each watershed
3. **Regression Analysis:** Estimate S, α, and Q using multivariate OLS with bootstrap
4. **Storage Estimation:** Compute annual storage change incorporating all terms
5. **Subsidence Integration:** Add fine-grained compaction from InSAR analysis
6. **Validation:** Compare independent estimates and assess budget closure

See `docs/METHODS.md` for detailed methodology.

## Results

### Storage Change Estimates (2015-2022):

| Subdistrict | Total Storage Loss (m³) | Subsidence Contribution (%) |
|-------------|--------------------------|------------------------------|
| Alamosa/La Jara | -XXX × 10⁶ | XX% |
| Saguache | -XXX × 10⁶ | XX% |
| Subdistrict 1 RA | -XXX × 10⁶ | XX% |

### Estimated Aquifer Properties:

| Subdistrict | Storativity | Recharge Coefficient (α) |
|-------------|-------------|--------------------------|
| Alamosa/La Jara | X.XX ± X.XX | X.XX ± X.XX |
| Saguache | X.XX ± X.XX | X.XX ± X.XX |
| Subdistrict 1 RA | X.XX ± X.XX | X.XX ± X.XX |

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{alfatta2025slv,
  title={Quantifying Groundwater Depletion in an Agricultural Region Using Integrated In-Situ and Satellite-Based Approaches: Insights from the San Luis Valley, Colorado},
  author={Al Fatta, Abdullah and [Co-authors]},
  journal={Journal of Hydrology},
  year={2025},
  volume={XXX},
  pages={XXX-XXX},
  doi={10.xxxx/xxxxx}
}
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Colorado State University** - Department of Civil and Environmental Engineering
- **Rio Grande Water Conservation District** - Pumping and water-level data
- **USGS** - National Water Information System (NWIS) data
- **NASA** - InSAR data from ASF DAAC
- **PRISM Climate Group** - Precipitation data

## Contact

**Abdullah Al Fatta**  
Ph.D. Candidate, Civil Engineering  
Colorado State University  
Email: abdullah.al_fatta@colostate.edu]  
LinkedIn: https://www.linkedin.com/in/abdullahalfatta

## Related Publications

1. Al Fatta, Abdullah and Smith, Ryan and Vajedian, Sanaz and Schreuder, Willem and Butler, James J., Quantifying Groundwater Depletion in an Agricultural Region Using Integrated In-Situ and Satellite-Based Approaches: Insights from the San Luis Valley, CO. Available at SSRN: http://dx.doi.org/10.2139/ssrn.5987334

## Project Status

🚧 **Active Development** - This repository is associated with ongoing doctoral research. Updates are made regularly as analysis progresses.

---

**Keywords:** groundwater depletion, InSAR, subsidence, water balance, San Luis Valley, aquifer storage, hydrogeology, remote sensing, Python
