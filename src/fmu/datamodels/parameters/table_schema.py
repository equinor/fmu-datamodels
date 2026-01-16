from typing import Literal

from pydantic import BaseModel

from .metadata import ParameterMetadata


class ParameterColumn(BaseModel):
    """Metadata for a parameter column."""

    type: Literal["float64", "int64"]
    metadata: ParameterMetadata


class ParameterTableSchema(BaseModel):
    """
    Schema for PyArrow parameters exported with Ert parameters.

    The table always has a 'realization' column (int64) as the first column.
    """

    parameters: dict[str, ParameterColumn]
