from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from fmu.datamodels.types import VersionStr


class ModelStratigraphyHorizonsResultRow(BaseModel):
    """Represents a horizon in an RMS model stratigraphy."""

    model_config = ConfigDict(use_attribute_docstrings=True)

    name: str
    """Index column. Name of the horizon. Required."""

    type: Literal[
        "calculated",
        "calculated_unconformity",
        "interpreted",
        "interpreted_unconformity",
        "interpreted_intrusion",
    ]
    """Index column. Type of the horizon. Required."""

    stratigraphic_order: int = Field(ge=0)
    """The zero-based order of the horizon in the stratigraphic column. Required."""


class ModelStratigraphyHorizonsResult(RootModel):
    """Represents the model stratigraphy horizons table as a list of rows."""

    root: list[ModelStratigraphyHorizonsResultRow]


class ModelStratigraphyHorizonsSchema(SchemaBase):
    """The schema used to validate a model stratigraphy horizons table."""

    VERSION: VersionStr = "0.1.0"

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "model_stratigraphy_horizons.json"
    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return ModelStratigraphyHorizonsResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
