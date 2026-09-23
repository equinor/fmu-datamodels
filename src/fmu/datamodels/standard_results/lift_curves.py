from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr


class LiftCurvesResultRow(BaseModel):
    """Represents the columns of a row in a lift curves export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    RATE: float
    """Flow rate. Required."""

    PRESSURE: float
    """Pressure value. Required."""

    WFR: float | None = Field(default=None)
    """Water fraction axis value. Optional."""

    GFR: float | None = Field(default=None)
    """Gas fraction axis value. Optional."""

    ALQ: float | None = Field(default=None)
    """Artificial lift quantity axis value. Optional."""

    TAB: float | None = Field(default=None)
    """Tabulated pressure axis value. Optional."""

    VFP_TYPE: str
    """Index column. The VFP table type. Required."""

    TABLE_NUMBER: int
    """Index column. The VFP table number. Required."""

    DATUM: float
    """The table reference depth. Required."""

    RATE_TYPE: str
    """Index column. The flow-rate type. Required."""

    WFR_TYPE: str | None = Field(default=None)
    """Index column. The water-fraction type. Optional."""

    GFR_TYPE: str | None = Field(default=None)
    """Index column. The gas-fraction type. Optional."""

    ALQ_TYPE: str | None = Field(default=None)
    """Index column. The artificial-lift quantity type. Optional."""

    PRESSURE_TYPE: str
    """Index column. The pressure type. Required."""

    TAB_TYPE: str | None = Field(default=None)
    """Index column. The tabulated pressure type. Optional."""

    UNIT_TYPE: str
    """Index column. The unit system. Required."""


class LiftCurvesResult(RootModel):
    """Represents the resultant lift curves parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[LiftCurvesResultRow]


class LiftCurvesSchema(SchemaBase):
    """This class represents the schema that is used to validate the lift curves
    table being exported. This means that the version, schema filename,
    and schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "lift_curves.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return LiftCurvesResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
