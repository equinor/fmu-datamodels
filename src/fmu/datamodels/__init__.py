"""Top-level package for fmu-datamodels."""

from fmu.datamodels._schema_base import SchemaBase

from .fmu_results import FmuResults, FmuResultsSchema
from .standard_results import (
    ErtDistribution,
    ErtParameterMetadata,
    ErtParametersResult,
    ErtParametersSchema,
    FieldOutlineResult,
    FieldOutlineSchema,
    FluidContactOutlineResult,
    FluidContactOutlineSchema,
    InplaceVolumesResult,
    InplaceVolumesSchema,
    SimulatorFipregionsMappingResult,
    SimulatorFipregionsMappingSchema,
    StructureDepthFaultLinesResult,
    StructureDepthFaultLinesSchema,
)

try:
    from .version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"

__all__ = [
    "ErtDistribution",
    "ErtParameterMetadata",
    "ErtParametersResult",
    "ErtParametersSchema",
    "FmuResults",
    "FmuResultsSchema",
    "FieldOutlineResult",
    "FieldOutlineSchema",
    "FluidContactOutlineResult",
    "FluidContactOutlineSchema",
    "InplaceVolumesResult",
    "InplaceVolumesSchema",
    "SimulatorFipregionsMappingResult",
    "SimulatorFipregionsMappingSchema",
    "StructureDepthFaultLinesResult",
    "StructureDepthFaultLinesSchema",
]

schemas: list[type[SchemaBase]] = [
    FmuResultsSchema,
    ErtParametersSchema,
    FieldOutlineSchema,
    FluidContactOutlineSchema,
    InplaceVolumesSchema,
    SimulatorFipregionsMappingSchema,
    StructureDepthFaultLinesSchema,
]
