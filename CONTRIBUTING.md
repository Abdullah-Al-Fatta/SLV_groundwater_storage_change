# Contributing to SLV Groundwater Depletion Analysis

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the San Luis Valley groundwater depletion analysis repository.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/slv-groundwater-depletion.git
   cd slv-groundwater-depletion
   ```
3. **Set up the development environment:**
   ```bash
   conda env create -f environment.yml
   conda activate slv-groundwater
   ```
4. **Create a new branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **Bug fixes:** Fix errors in existing code
2. **New features:** Add new analysis capabilities
3. **Documentation:** Improve or expand documentation
4. **Data processing:** Enhance data cleaning or preprocessing
5. **Visualization:** Create new plots or improve existing ones
6. **Testing:** Add unit tests or integration tests
7. **Performance:** Optimize computational efficiency

### Reporting Issues

Before creating an issue:
- Check if the issue already exists
- Provide a clear, descriptive title
- Include steps to reproduce the problem
- Specify your environment (OS, Python version, package versions)
- Include error messages and stack traces

### Suggesting Enhancements

For feature requests:
- Explain the use case
- Describe the expected behavior
- Provide examples if possible
- Consider implementation complexity

## Development Workflow

### 1. Branch Naming

Use descriptive branch names:
- `feature/add-kriging-optimization`
- `bugfix/fix-coordinate-projection`
- `docs/update-installation-guide`
- `refactor/modularize-pumping-analysis`

### 2. Commit Messages

Write clear, descriptive commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text if necessary. Wrap it to about 72
characters. The blank line separating the summary from the body is
critical.

- Bullet points are okay
- Use present tense: "Fix bug" not "Fixed bug"
- Reference issues: "Fixes #123"
```

Good examples:
```
Add bootstrap uncertainty quantification to storativity estimation

Implement bootstrap resampling (n=1000 iterations) to estimate
confidence intervals for storativity and recharge coefficients.
Adds new function bootstrap_storativity() to regression analysis.

Fixes #42
```

### 3. Keep Your Fork Updated

Regularly sync with the main repository:

```bash
git remote add upstream https://github.com/original-owner/slv-groundwater-depletion.git
git fetch upstream
git checkout main
git merge upstream/main
```

## Coding Standards

### Python Style Guide

Follow PEP 8 guidelines:

```python
# Good
def calculate_storage_change(head_change, area, storativity):
    """
    Calculate storage change from head change.
    
    Parameters
    ----------
    head_change : float
        Change in hydraulic head (meters)
    area : float
        Aquifer area (square meters)
    storativity : float
        Aquifer storativity (dimensionless)
    
    Returns
    -------
    float
        Storage change (cubic meters)
    """
    return head_change * area * storativity


# Bad
def calc(h,a,s):
    return h*a*s
```

### Key Principles

1. **Use descriptive variable names:**
   ```python
   # Good
   mean_hydraulic_head = well_data.groupby('year')['head_elevation_m'].mean()
   
   # Bad
   mhh = df.groupby('y')['h'].mean()
   ```

2. **Add docstrings to all functions:**
   - Use NumPy/SciPy documentation format
   - Include Parameters, Returns, and Examples sections

3. **Use type hints:**
   ```python
   from typing import Dict, List, Tuple
   
   def process_pumping_data(
       pumping_data: gpd.GeoDataFrame, 
       study_region: gpd.GeoDataFrame
   ) -> pd.DataFrame:
       """Process pumping data for study region."""
       pass
   ```

4. **Avoid hardcoded paths:**
   ```python
   # Good
   from pathlib import Path
   DATA_DIR = Path(__file__).parent.parent / 'data'
   pumping_file = DATA_DIR / 'pumping' / 'pumping_data.csv'
   
   # Bad
   pumping_file = r'D:\OneDrive - Colostate\...\pumping_data.csv'
   ```

5. **Use constants for magic numbers:**
   ```python
   # Good
   ACRE_FEET_TO_CUBIC_METERS = 1233.48
   pumping_m3 = pumping_af * ACRE_FEET_TO_CUBIC_METERS
   
   # Bad
   pumping_m3 = pumping_af * 1233.48
   ```

## Testing

### Writing Tests

All new functions should have associated tests:

```python
import pytest
import numpy as np
from scripts.storage_change_calc import calculate_storage_change

def test_storage_change_calculation():
    """Test basic storage change calculation."""
    head_change = -1.0  # meters
    area = 1e9  # square meters
    storativity = 0.001
    
    result = calculate_storage_change(head_change, area, storativity)
    expected = -1e6  # cubic meters
    
    assert np.isclose(result, expected)

def test_storage_change_zero_head():
    """Test with no head change."""
    result = calculate_storage_change(0, 1e9, 0.001)
    assert result == 0

def test_storage_change_invalid_inputs():
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError):
        calculate_storage_change(-1, -1e9, 0.001)  # Negative area
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_storage_change.py

# Run with coverage
pytest --cov=scripts tests/
```

## Documentation

### Updating Documentation

When making changes, update relevant documentation:

1. **Code comments:** Explain complex logic
2. **Docstrings:** Update function documentation
3. **README.md:** Update if adding new features
4. **docs/*.md:** Update methodology or data descriptions
5. **CHANGELOG.md:** Add entry for significant changes

### Documentation Style

- Use Markdown for all documentation files
- Include code examples where helpful
- Add diagrams or equations when needed (use LaTeX syntax)
- Keep language clear and concise

Example equation in Markdown:
```markdown
The storage change is calculated as:

$$\Delta S = S \times A \times \Delta h$$

Where:
- $\Delta S$ is storage change (m³)
- $S$ is storativity (dimensionless)
- $A$ is area (m²)
- $\Delta h$ is head change (m)
```

## Submitting Changes

### Pull Request Process

1. **Update your branch:**
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/your-feature
   git rebase main
   ```

2. **Run tests and checks:**
   ```bash
   pytest tests/
   flake8 scripts/
   black scripts/ --check
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature
   ```

4. **Create a Pull Request:**
   - Go to GitHub and create a new PR
   - Use a descriptive title
   - Reference any related issues
   - Provide a clear description of changes
   - Include screenshots for UI changes
   - List any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Related Issues
Fixes #123
Related to #456

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe testing performed:
- Unit tests added/updated
- Manual testing performed
- Edge cases considered

## Screenshots (if applicable)
Add screenshots of visualizations or outputs

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No hardcoded file paths
- [ ] Commit messages are clear
```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

### After Your PR is Merged

- Delete your feature branch
- Update your local main branch
- Celebrate! 🎉

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Email the maintainer: [your.email@colostate.edu]

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Publication acknowledgments (for significant contributions)
- CONTRIBUTORS.md file

Thank you for contributing to groundwater research!
