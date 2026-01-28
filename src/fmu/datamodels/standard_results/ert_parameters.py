"""Schemas for Ert parameter metadata.

These schemas are used for Parquet column metadata in Ert parameter tables."""

import json
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from pydantic import BaseModel, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr


class ErtDistribution(StrEnum):
    """All currently known Ert distributions."""

    uniform = "uniform"
    logunif = "logunif"
    normal = "normal"
    lognormal = "lognormal"
    truncated_normal = "truncated_normal"
    raw = "raw"
    const = "const"
    dunif = "dunif"
    triangular = "triangular"
    errf = "errf"
    derrf = "derrf"


class GenKwParameterMetadata(BaseModel):
    """Base class for all parameter metadata.

    These models are attached as column metadata for the exported Ert parameters
    Parquet table."""

    model_config = {"extra": "forbid"}

    group: str
    input_source: Literal["sampled", "design_matrix"]
    distribution: Literal[
        ErtDistribution.uniform,
        ErtDistribution.logunif,
        ErtDistribution.normal,
        ErtDistribution.lognormal,
        ErtDistribution.truncated_normal,
        ErtDistribution.raw,
        ErtDistribution.const,
        ErtDistribution.dunif,
        ErtDistribution.triangular,
        ErtDistribution.errf,
        ErtDistribution.derrf,
    ]

    def to_pa_metadata(self) -> dict[bytes, bytes]:
        """Convert the model to a PyArrow-compatible metadata dictionary."""
        return {
            k.encode("utf-8"): json.dumps(v).encode("utf-8")
            for k, v in self.model_dump().items()
        }

    @classmethod
    def from_pa_metadata(cls, metadata: dict[bytes, bytes]) -> Self:
        """Create an instance of the class from PyArrow metadata."""
        str_metadata = {
            k.decode("utf-8"): json.loads(v.decode("utf-8"))
            for k, v in metadata.items()
        }
        return cls.model_validate(str_metadata)


class UniformParameter(GenKwParameterMetadata):
    """Metadata values for a uniform distribution."""

    distribution: Literal[ErtDistribution.uniform]
    min: float
    max: float


class LogUnifParameter(GenKwParameterMetadata):
    """Metadata values for a log uniform distribution."""

    distribution: Literal[ErtDistribution.logunif]
    min: float
    max: float


class NormalParameter(GenKwParameterMetadata):
    """Metadata values for a normal distribution."""

    distribution: Literal[ErtDistribution.normal]
    mean: float
    std: float


class LogNormalParameter(GenKwParameterMetadata):
    """Metadata values for a log normal distribution."""

    distribution: Literal[ErtDistribution.lognormal]
    mean: float
    std: float


class TruncatedNormalParameter(GenKwParameterMetadata):
    """Metadata values for a truncated normal distribution."""

    distribution: Literal[ErtDistribution.truncated_normal]
    min: float
    max: float
    mean: float
    std: float


class RawParameter(GenKwParameterMetadata):
    """Metadata values for a raw distribution.

    This "distribution" is used for design matrix parameters.
    """

    distribution: Literal[ErtDistribution.raw]


class ConstParameter(GenKwParameterMetadata):
    """Metadata values for a const distribution."""

    distribution: Literal[ErtDistribution.const]
    value: float


class DUnifParameter(GenKwParameterMetadata):
    """Metadata values for a discrete uniform distribution."""

    distribution: Literal[ErtDistribution.dunif]
    min: float
    max: float
    steps: int


class TriangularParameter(GenKwParameterMetadata):
    """Metadata values for a triangular distribution."""

    distribution: Literal[ErtDistribution.triangular]
    min: float
    max: float
    mode: float


class ErrfParameter(GenKwParameterMetadata):
    """Metadata values for a Errf (error function) distribution."""

    distribution: Literal[ErtDistribution.errf]
    min: float
    max: float
    skewness: float
    width: float


class DerrfParameter(GenKwParameterMetadata):
    """Metadata values for a Derrf (discrete error function) distribution."""

    distribution: Literal[ErtDistribution.derrf]
    min: float
    max: float
    skewness: float
    width: float
    steps: float


ErtParameterMetadata = Annotated[
    UniformParameter
    | LogUnifParameter
    | LogNormalParameter
    | NormalParameter
    | TruncatedNormalParameter
    | RawParameter
    | ConstParameter
    | DUnifParameter
    | TriangularParameter
    | ErrfParameter
    | DerrfParameter,
    Field(discriminator="distribution"),
]


class ErtParameterColumn(BaseModel):
    """Metadata for a parameter column.

    'string' is a valid dtype when it comes from the design matrix."""

    type: Literal["float64", "int64", "string"]
    metadata: ErtParameterMetadata


class ErtParametersResult(RootModel[dict[str, ErtParameterColumn]]):
    """
    Represents the Ert parameters exported as a Parquet file.

    Every parameter column has associated column metadata.

    The table always has a 'realization' column (int64) as the first column. That column
    is not represented in this schema, but is implied.
    """

    def all_column_names(self) -> list[str]:
        return ["realization", *self.root.keys()]


class ErtParametersSchema(SchemaBase):
    """This class represents the schema that is used to validate the fault lines
    table being exported. This means that the version, schema filename, and schema
    location corresponds directly with the values and their validation constraints,
    documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "ert_parameters.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return ErtParametersResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
