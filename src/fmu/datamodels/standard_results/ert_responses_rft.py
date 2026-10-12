from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.types import VersionStr


class ErtResponsesRftResultRow(BaseModel):
    """Represents the columns of a row in a Ert rft responses export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    realization: int
    """Index column. The realization this row represents. Required."""

    response_key: str
    """Index column. The response key this row represents. Required."""

    well: str
    """Index column. The well this row represents. Required."""

    date: str
    """Index column. The date in ISO 8601 format this row represents. Required."""

    property: str
    """Index column. The property this row represents, e.g. 'PRESSURE' or 'SWAT'. 
    Required."""

    response_value: float
    """The simulated response value this row represents. Required."""

    well_connection_cell: list[int]
    """The well connection cell this row represents. Required."""


class ErtResponsesRftResult(RootModel):
    """Represents the resultant Ert rft responses parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    clearly equivalent format to validate it against the schema."""

    root: list[ErtResponsesRftResultRow]


class ErtResponsesRftSchema(SchemaBase):
    """This class represents the schema that is used to validate the Ert rft
    responses table being exported. This means that the version, schema filename,
    and schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"
    """The version of this schema."""

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "ert_responses_rft.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return ErtResponsesRftResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
