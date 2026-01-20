from typing import Literal

from pydantic import BaseModel

from .metadata import ParameterMetadata


class ParameterColumn(BaseModel):
    """Metadata for a parameter column.

    'string' is a valid dtype when it comes from the design matrix."""

    type: Literal["float64", "int64", "string"]
    metadata: ParameterMetadata


class ParameterTableSchema(BaseModel):
    """
    Schema for PyArrow parameters exported with Ert parameters.

    The table always has a 'realization' column (int64) as the first column.
    """

    parameters: dict[str, ParameterColumn]
