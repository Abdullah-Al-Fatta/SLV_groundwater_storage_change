# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository structure
- Core analysis scripts for storage change estimation
- InSAR subsidence analysis workflow
- Multivariate regression for storativity determination
- Comprehensive documentation (README, DATA.md, METHODS.md)
- Python environment configuration files
- Unit test framework

## [1.0.0] - 2025-01-XX

### Added
- `storage_change_calc.py`: Main storage change estimation from water levels
- `storage_change_calc_from_subsidence.py`: InSAR-based storage analysis
- `storativity_precip_coeff_inflow_determination.py`: Regression-based aquifer property estimation
- `percent_pumping_from_storage_change.py`: Pumping contribution analysis
- `diversion_plots.py`: Surface water diversion visualization
- Complete dataset processing pipeline
- Bootstrap uncertainty quantification
- Google Earth Engine integration for PRISM data extraction

### Documentation
- Comprehensive README with installation and usage instructions
- Detailed methodology documentation
- Data sources and processing documentation
- Contributing guidelines
- MIT License

### Infrastructure
- Conda environment specification
- Requirements.txt for pip installation
- .gitignore configured for Python and geospatial data
- GitHub repository structure

## Development Notes

### Planned Features
- [ ] Modularize scripts into reusable functions
- [ ] Add configuration file for file paths
- [ ] Implement automated testing suite
- [ ] Create Jupyter notebook tutorials
- [ ] Add interactive visualization dashboard
- [ ] Integrate additional climate datasets (GridMET, SNODAS)
- [ ] Implement kriging optimization for head interpolation
- [ ] Add time-series analysis for trend detection
- [ ] Create automated report generation

### Known Issues
- Hardcoded file paths in all scripts (need to be updated by users)
- Limited error handling in data loading functions
- InSAR raster file not included (too large for Git)
- Some scripts require specific column names in input data

### Future Enhancements
- Docker containerization for reproducibility
- CI/CD pipeline with GitHub Actions
- Automated data downloading from USGS NWIS
- Web-based interface for visualization
- Integration with MODFLOW for groundwater modeling
- Machine learning for pumping prediction

---

## Version History

- **v1.0.0** - Initial release (January 2025)
  - Core functionality for PhD dissertation research
  - Manuscript submitted to Journal of Hydrology
