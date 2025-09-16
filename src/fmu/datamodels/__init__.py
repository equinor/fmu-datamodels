"""Top-level package for fmu-datamodels."""

from fmu.datamodels._schema_base import SchemaBase

from .fmu_results import FmuResults, FmuResultsSchema
from .standard_results import (
    FieldOutlineResult,
    FieldOutlineSchema,
    InplaceVolumesResult,
    InplaceVolumesSchema,
    StructureDepthFaultLinesResult,
    StructureDepthFaultLinesSchema,
)

try:
    from .version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"

__all__ = [
    "FmuResults",
    "FmuResultsSchema",
    "FieldOutlineResult",
    "FieldOutlineSchema",
    "InplaceVolumesResult",
    "InplaceVolumesSchema",
    "StructureDepthFaultLinesResult",
    "StructureDepthFaultLinesSchema",
]

schemas: list[type[SchemaBase]] = [
    FmuResultsSchema,
    FieldOutlineSchema,
    InplaceVolumesSchema,
    StructureDepthFaultLinesSchema,
]
