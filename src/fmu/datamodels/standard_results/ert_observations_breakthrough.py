from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr


class ErtObservationsBreakthroughResultRow(BaseModel):
    """Represents the columns of a row in a Ert breakthrough observation export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    response_key: str
    """The response key this row represents. Required."""

    time: datetime
    """The datetime in millisecond precision this row represents. Required."""

    observation_value: float
    """The observation value this row represents. Required."""

    observation_error: float
    """The observation error in std this row represents. Required."""

    threshold: float
    """The threshold value this row represents. Required."""

    east: float
    """The east coordinate this row represents. Required."""

    north: float
    """The north coordinate this row represents. Required."""


class ErtObservationsBreakthroughResult(RootModel):
    """Represents the resultant Ert breakthrough observations parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[ErtObservationsBreakthroughResultRow]


class ErtObservationsBreakthroughSchema(SchemaBase):
    """This class represents the schema that is used to validate the Ert breakthrough
    observations table being exported. This means that the version, schema filename,
    and schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "ert_observations_breakthrough.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return ErtObservationsBreakthroughResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
