"""Schemas for Ert parameter distributions.

These schemas are used for Parquet column metadata in Ert parameter tables."""

import json
from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field


class BaseDistribution(BaseModel):
    """Base class for all distribution metadata.

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


class UniformDistribution(BaseDistribution):
    """Metadata values for a uniform distribution."""

    distribution: Literal["uniform"] = "uniform"
    min: float
    max: float


class LogUnifDistribution(BaseDistribution):
    """Metadata values for a log uniform distribution."""

    distribution: Literal["logunif"] = "logunif"
    min: float
    max: float


class NormalDistribution(BaseDistribution):
    """Metadata values for a normal distribution."""

    distribution: Literal["normal"] = "normal"
    mean: float
    std: float


class LogNormalDistribution(BaseDistribution):
    """Metadata values for a log normal distribution."""

    distribution: Literal["lognormal"] = "lognormal"
    mean: float
    std: float


class TruncatedNormalDistribution(BaseDistribution):
    """Metadata values for a truncated normal distribution."""

    distribution: Literal["truncated_normal"] = "truncated_normal"
    min: float
    max: float
    mean: float
    std: float


class RawDistribution(BaseDistribution):
    """Metadata values for a raw distribution.

    This "distribution" is used for design matrix parameters.
    """

    distribution: Literal["raw"] = "raw"


class ConstDistribution(BaseDistribution):
    """Metadata values for a const distribution."""

    distribution: Literal["const"] = "const"
    value: float


class DUnifDistribution(BaseDistribution):
    """Metadata values for a discrete uniform distribution."""

    distribution: Literal["dunif"] = "dunif"
    min: float
    max: float
    steps: int


class TriangularDistribution(BaseDistribution):
    """Metadata values for a triangular distribution."""

    distribution: Literal["triangular"] = "triangular"
    min: float
    max: float
    mode: float


class ErrfDistribution(BaseDistribution):
    """Metadata values for a Errf (error function) distribution."""

    distribution: Literal["errf"] = "errf"
    min: float
    max: float
    skewness: float
    width: float


class DerrfDistribution(BaseDistribution):
    """Metadata values for a Derrf (discrete error function) distribution."""

    distribution: Literal["derrf"] = "derrf"
    min: float
    max: float
    skewness: float
    width: float
    steps: float


DistributionMetadata = Annotated[
    UniformDistribution
    | LogUnifDistribution
    | LogNormalDistribution
    | NormalDistribution
    | TruncatedNormalDistribution
    | RawDistribution
    | ConstDistribution
    | DUnifDistribution
    | TriangularDistribution
    | ErrfDistribution
    | DerrfDistribution,
    Field(discriminator="distribution"),
]
