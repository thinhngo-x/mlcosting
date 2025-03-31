from enum import Enum
from typing import Union

from .reanalysis_era5_pressure_levels import ReanalysisEra5PressureLevels

RequestParamModel = Union[ReanalysisEra5PressureLevels]


class DatasetName(str, Enum):
    reanalysis_era5_pressure_levels = "reanalysis_era5_pressure_levels"
    # Add other dataset names as needed


def get_request_model(
    dataset_name: DatasetName,
) -> Union[type[ReanalysisEra5PressureLevels]]:
    if dataset_name == DatasetName.reanalysis_era5_pressure_levels:
        return ReanalysisEra5PressureLevels
    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}")
