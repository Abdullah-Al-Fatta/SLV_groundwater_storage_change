"""
Setup script for SLV Groundwater Depletion Analysis
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="slv-groundwater-depletion",
    version="1.0.0",
    author="Abdullah Al Fatta",
    author_email="your.email@colostate.edu",
    description="Quantifying groundwater depletion using integrated in-situ and satellite approaches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/slv-groundwater-depletion",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/slv-groundwater-depletion/issues",
        "Documentation": "https://github.com/yourusername/slv-groundwater-depletion/tree/main/docs",
        "Source Code": "https://github.com/yourusername/slv-groundwater-depletion",
    },
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Hydrology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "geopandas>=0.10.0",
        "rasterio>=1.2.0",
        "fiona>=1.8.20",
        "shapely>=1.8.0",
        "pyproj>=3.2.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "adjustText>=0.7.3",
        "statsmodels>=0.13.0",
        "scikit-learn>=1.0.0",
        "earthengine-api>=0.1.300",
        "geemap>=0.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=3.0.0",
            "flake8>=4.0.0",
            "black>=22.0.0",
            "sphinx>=4.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipython>=7.30.0",
            "notebook>=6.4.0",
        ],
    },
    include_package_data=True,
    keywords=[
        "groundwater",
        "depletion",
        "InSAR",
        "subsidence",
        "hydrology",
        "water-balance",
        "san-luis-valley",
        "remote-sensing",
        "gis",
    ],
    entry_points={
        "console_scripts": [
            # Add command-line scripts here if needed
            # "slv-analyze=scripts.main:main",
        ],
    },
)
