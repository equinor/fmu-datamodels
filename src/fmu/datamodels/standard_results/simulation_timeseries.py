from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr


class SimulationTimeseriesResultRow(BaseModel):
    """Represents the columns of a row in a simulation timeseries export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    DATE: datetime
    """The simulation report datetime represented by this row. Required."""

    FGPT: float | None = Field(default=None)
    """The field gas production total at ``DATE``. Optional."""

    FOPT: float | None = Field(default=None)
    """The field oil production total at ``DATE``. Optional."""

    FVPT: float | None = Field(default=None)
    """The field voidage production total at ``DATE``. Optional."""

    FWPT: float | None = Field(default=None)
    """The field water production total at ``DATE``. Optional."""


class SimulationTimeseriesResult(RootModel):
    """Represents the resultant Ert breakthrough observations parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[SimulationTimeseriesResultRow]


class SimulationTimeseriesSchema(SchemaBase):
    """This class represents the schema used to validate the simulation timeseries table
    being exported. This means that the version, schema filename,
    and schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "simulation_timeseries.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return SimulationTimeseriesResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
