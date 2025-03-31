# MLCosting

This is a prototype of a machine-learning-based API service that can classify load tiers of a dataset request. This demo is submitted to ECMWF Code4Earth as part of the proposal to the [Challenge 20](https://github.com/ECMWFCode4Earth/Challenges_2025/issues/12) - DSS MLCosting for requests.

## Overview

MLCosting is a Python application that provides API endpoints to:
1. Transform meteorological data requests into machine learning-ready features
2. Classify or estimate costs for data retrieval operations

The project currently supports [ERA5 reanalysis pressure level datasets](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=download) and provides a framework for extending to additional datasets.

## Quick Start

### Prerequisites

- Python 3.11+

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mlcosting.git
   cd mlcosting
   ```

2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for package management. While we recommend a standalone installation, you can also use it within a virtual environment:
   ```
   pip install uv
   ```
3. Install the required packages:
   ```
   uv sync
   ```
4. Launch the FastAPI server in dev mode:
   ```
   uv run fastapi dev
   ```
5. Access the API documentation at `http://localhost:8000/docs` to consult and try out available endpoints.

## Usage

### Starting the API server

```python
from app.main import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

Alternatively, you can run directly with:

```
python -m app.main
```

### API Endpoints

#### Transform Request

```
POST /transform_request/{dataset_name}
```

Transforms a request into one-hot encoded features.

Example:
```python
import requests

payload = {
    "product_type": ["reanalysis"],
    "variable": ["temperature", "geopotential"],
    "year": ["2020"],
    "month": ["01"],
    "pressure_level": ["500", "850"]
}

response = requests.post(
    "http://localhost:8000/transform_request/reanalysis_era5_pressure_levels", 
    json=payload
)
```

#### Classify

```
POST /classify/{dataset_name}
```

Classifies a request using the specified model.

Example:
```python
import requests

payload = {
    "product_type": ["reanalysis"],
    "variable": ["temperature", "geopotential"],
    "year": ["2020"],
    "month": ["01"],
    "pressure_level": ["500", "850"]
}

response = requests.post(
    "http://localhost:8000/classify/reanalysis_era5_pressure_levels?model_name=xgboost", 
    json=payload
)
```

## Project Structure

```
mlcosting/
├── app/
│   ├── classifiers/
│   │   ├── preprocess.py    # One-hot encoding for Pydantic models
│   ├── models/
│   │   ├── reanalysis_era5_pressure_levels.py  # ERA5 data model
│   │   ├── reanalysis-era5-pressure-levels.json # Schema definition
│   ├── main.py              # FastAPI application and endpoints
├── pyproject.toml           # Project configuration
├── README.md                # This file
```
`reanalysis-era5-pressure-levels.json` is pulled from [the official API](https://cds.climate.copernicus.eu/api/retrieve/v1/processes/reanalysis-era5-pressure-levels) and adjusted to fit the [JSON schema syntax](https://koxudaxi.github.io/datamodel-code-generator/jsonschema/).

## Development

### Adding New Dataset Models

1. Create a new JSON schema in the `app/models/` directory
2. Generate the Pydantic model using datamodel-code-generator:
   ```
   datamodel-codegen --input app/models/your-schema.json --output app/models/your_schema.py
   ```
3. Update `app/models/__init__.py` to include the new model

### Adding New ML Models

Extend the `ModelName` enum in `app/main.py` and update the classifier endpoint logic.

## Dependencies

- fastapi - Web framework
- numpy, pandas - Data handling
- pydantic - Data validation
- scikit-learn - ML utilities
- xgboost - Classification model
- datamodel-code-generator - JSON schema to Pydantic model generator
