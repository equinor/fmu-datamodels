from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from fmu.datamodels.types import VersionStr


class RelpermResultRow(BaseModel):
    """Represents the columns of a row in a relperm export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    SW: float | None = Field(default=None, ge=0.0, le=1.0)
    """The water saturation this row represents. Optional."""

    KRW: float | None = Field(default=None, ge=0.0)
    """The water relative permeability this row represents. Optional."""

    KROW: float | None = Field(default=None, ge=0.0)
    """The oil-water relative permeability this row represents. Optional."""

    PCOW: float | None = None
    """The oil-water capillary pressure this row represents. Optional."""

    SATNUM: int = Field(ge=0)
    """Index column. The saturation function region this row represents. Required."""

    KEYWORD: str
    """The Eclipse saturation function keyword this row is derived from. Required."""

    SG: float | None = Field(default=None, ge=0.0, le=1.0)
    """The gas saturation this row represents. Optional."""

    KRG: float | None = Field(default=None, ge=0.0)
    """The gas relative permeability this row represents. Optional."""

    KROG: float | None = Field(default=None, ge=0.0)
    """The oil-gas relative permeability this row represents. Optional."""

    PCOG: float | None = None
    """The oil-gas capillary pressure this row represents. Optional."""


class RelpermResult(RootModel):
    """Represents the resultant relperm parquet file as a list of rows."""

    root: list[RelpermResultRow]


class RelpermSchema(SchemaBase):
    """The schema used to validate an exported relperm table."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "relperm.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return RelpermResult.model_json_schema(schema_generator=cls.default_generator())
