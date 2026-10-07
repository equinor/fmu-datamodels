from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from fmu.datamodels.types import VersionStr


class PvtResultRow(BaseModel):
    """Represents the columns of a row in a pvt export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    PVTNUM: int = Field(ge=0)
    """Index column. The PVT region this row represents. Required."""

    KEYWORD: str
    """Index column. The Eclipse PVT keyword this row is derived from (e.g. PVTO,
    PVDG, PVTW). Required."""

    PRESSURE: float | None = Field(default=None, ge=0.0)
    """The pressure this row represents. Optional."""

    VOLUMEFACTOR: float | None = Field(default=None, ge=0.0)
    """The formation volume factor this row represents. Optional."""

    VISCOSITY: float | None = Field(default=None, ge=0.0)
    """The viscosity this row represents. Optional."""

    RS: float | None = Field(default=None, ge=0.0)
    """The solution gas-oil ratio this row represents. Optional."""

    OGR: float | None = Field(default=None, ge=0.0)
    """The vaporized oil-gas ratio this row represents. Optional."""

    OILDENSITY: float | None = Field(default=None, ge=0.0)
    """The oil density this row represents. Optional."""

    WATERDENSITY: float | None = Field(default=None, ge=0.0)
    """The water density this row represents. Optional."""

    GASDENSITY: float | None = Field(default=None, ge=0.0)
    """The gas density this row represents. Optional."""

    COMPRESSIBILITY: float | None = Field(default=None, ge=0.0)
    """The fluid compressibility this row represents. Optional."""

    VISCOSIBILITY: float | None = Field(default=None, ge=0.0)
    """The viscosibility (viscosity compressibility) this row represents. Optional."""


class PvtResult(RootModel):
    """Represents the resultant pvt parquet file, which is naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[PvtResultRow]


class PvtSchema(SchemaBase):
    """This class represents the schema that is used to validate the pvt table
    being exported. This means that the version, schema filename, and schema
    location corresponds directly with the values and their validation constraints,
    documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "pvt.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return PvtResult.model_json_schema(schema_generator=cls.default_generator())
