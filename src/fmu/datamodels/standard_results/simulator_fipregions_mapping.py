from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr

if TYPE_CHECKING:
    from typing import Any


class SimulatorFipregionsMappingResultRow(BaseModel):
    """Represents the columns of a row in a simulator fipregions mapping export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    FIPNUM: int = Field(ge=0)
    """Index column. The id of the fipregion this row represents. Required."""

    ZONE: str
    """Index column. The zone that the fipregion corresponds to. Required."""

    REGION: str
    """Index column. The region that the fipregion corresponds to. Required."""


class SimulatorFipregionsMappingResult(RootModel):
    """Represents the resultant simulator fipregions mapping parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[SimulatorFipregionsMappingResultRow]


class SimulatorFipregionsMappingSchema(SchemaBase):
    """This class represents the schema that is used to validate the mapping
    table being exported. This means that the version, schema filename, and
    schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "simulator_fipregions_mapping.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return SimulatorFipregionsMappingResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
