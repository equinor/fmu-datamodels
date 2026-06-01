from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.context.mappings import (
    StratigraphyIdentifierMapping,
)
from fmu.datamodels.types import VersionStr

if TYPE_CHECKING:
    from typing import Any


class StratigraphyMappingResultRow(StratigraphyIdentifierMapping):
    """Represents the columns of a row in a stratigraphy mapping export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""


class StratigraphyMappingResult(RootModel):
    """Represents the resultant stratigraphy mapping parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[StratigraphyMappingResultRow]


class StratigraphyMappingSchema(SchemaBase):
    """This class represents the schema that is used to validate the mapping
    table being exported. This means that the version, schema filename, and
    schema location corresponds directly with the values and their validation
    constraints, documented above."""

    VERSION: VersionStr = "0.1.0"

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "stratigraphy_mapping.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return StratigraphyMappingResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
