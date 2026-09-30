from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from fmu.datamodels.types import VersionStr


class ModelStratigraphyZonesResultRow(BaseModel):
    """Represents a zone in an RMS model stratigraphy."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    name: str
    """Index column. Name of the zone. Required."""

    top_horizon_name: str
    """Index column. Name of the horizon at the top of the zone. Required."""

    base_horizon_name: str
    """Index column. Name of the horizon at the base of the zone. Required."""

    stratigraphic_column_names: list[str] | None
    """Names of the stratigraphic columns the zone belongs to. Required.

    None indicates that stratigraphic column information is unavailable.
    """


class ModelStratigraphyZonesResult(RootModel):
    """Represents the model stratigraphy zones table as a list of rows."""

    root: list[ModelStratigraphyZonesResultRow]


class ModelStratigraphyZonesSchema(SchemaBase):
    """The schema used to validate a model stratigraphy zones table."""

    VERSION: VersionStr = "0.1.0"

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "model_stratigraphy_zones.json"
    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return ModelStratigraphyZonesResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
