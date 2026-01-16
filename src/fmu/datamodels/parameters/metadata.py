"""Schemas for Ert parameter metadata.

These schemas are used for Parquet column metadata in Ert parameter tables."""

import json
from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field


class GenKwParameterMetadata(BaseModel):
    """Base class for all parameter metadata.

    These models are attached as column metadata for the exported Ert parameters
    Parquet table."""

    model_config = {"extra": "forbid"}

    group: str
    input_source: Literal["sampled", "design_matrix"]

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

    distribution: Literal["uniform"] = "uniform"
    min: float
    max: float


class LogUnifParameter(GenKwParameterMetadata):
    """Metadata values for a log uniform distribution."""

    distribution: Literal["logunif"] = "logunif"
    min: float
    max: float


class NormalParameter(GenKwParameterMetadata):
    """Metadata values for a normal distribution."""

    distribution: Literal["normal"] = "normal"
    mean: float
    std: float


class LogNormalParameter(GenKwParameterMetadata):
    """Metadata values for a log normal distribution."""

    distribution: Literal["lognormal"] = "lognormal"
    mean: float
    std: float


class TruncatedNormalParameter(GenKwParameterMetadata):
    """Metadata values for a truncated normal distribution."""

    distribution: Literal["truncated_normal"] = "truncated_normal"
    min: float
    max: float
    mean: float
    std: float


class RawParameter(GenKwParameterMetadata):
    """Metadata values for a raw distribution.

    This "distribution" is used for design matrix parameters.
    """

    distribution: Literal["raw"] = "raw"


class ConstParameter(GenKwParameterMetadata):
    """Metadata values for a const distribution."""

    distribution: Literal["const"] = "const"
    value: float


class DUnifParameter(GenKwParameterMetadata):
    """Metadata values for a discrete uniform distribution."""

    distribution: Literal["dunif"] = "dunif"
    min: float
    max: float
    steps: int


class TriangularParameter(GenKwParameterMetadata):
    """Metadata values for a triangular distribution."""

    distribution: Literal["triangular"] = "triangular"
    min: float
    max: float
    mode: float


class ErrfParameter(GenKwParameterMetadata):
    """Metadata values for a Errf (error function) distribution."""

    distribution: Literal["errf"] = "errf"
    min: float
    max: float
    skewness: float
    width: float


class DerrfParameter(GenKwParameterMetadata):
    """Metadata values for a Derrf (discrete error function) distribution."""

    distribution: Literal["derrf"] = "derrf"
    min: float
    max: float
    skewness: float
    width: float
    steps: float


ParameterMetadata = Annotated[
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
