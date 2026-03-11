"""Top-level package for fmu-datamodels."""

from fmu.datamodels._schema_base import SchemaBase

from .common import (
    Access,
    Asset,
    CoordinateSystem,
    CountryItem,
    DiscoveryItem,
    FieldItem,
    Masterdata,
    OperatingSystem,
    Smda,
    Ssdl,
    SsdlAccess,
    StratigraphicColumn,
    SystemInformation,
    Tracklog,
    TracklogEvent,
    TracklogSource,
    User,
    Version,
)
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
    "Access",
    "SsdlAccess",
    "Asset",
    "Ssdl",
    "Masterdata",
    "Smda",
    "StratigraphicColumn",
    "CoordinateSystem",
    "CountryItem",
    "FieldItem",
    "DiscoveryItem",
    "Tracklog",
    "OperatingSystem",
    "SystemInformation",
    "TracklogEvent",
    "TracklogSource",
    "User",
    "Version",
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
