from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field, RootModel

from fmu.datamodels._schema_base import FMU_SCHEMAS_PATH, SchemaBase
from fmu.datamodels.standard_results.enums import InplaceVolumes
from fmu.datamodels.types import VersionStr

if TYPE_CHECKING:
    from typing import Any


class SimulatorInplaceVolumesResultRow(BaseModel):
    """Represents the columns of a row in a simulator inplace volumes export.

    These fields are the current agreed upon standard result. Changes to the fields or
    their validation should cause the version defined in the standard result schema to
    increase the version number in a way that corresponds to the schema versioning
    specification (i.e. they are a patch, minor, or major change)."""

    FLUID: Literal[InplaceVolumes.Fluid.gas, InplaceVolumes.Fluid.oil]
    """Index column. The kind of fluid this row represents. Required."""

    DATE: datetime
    """Index column. The datetime this row represents. Required."""

    FIPNUM: int = Field(ge=0.0)
    """Index column. The fipnum region which this volume is coming from. Required."""

    STOIIP: float | None = Field(default=None, ge=0.0)
    """The STOIIP volume of the fluid-type given in ``FLUID``. Optional."""

    GIIP: float | None = Field(default=None, ge=0.0)
    """The GIIP volume of the fluid-type given in ``FLUID``. Optional."""

    ASSOCIATEDGAS: float | None = Field(default=None, ge=0.0)
    """The associated gas volume of the fluid-type given in ``FLUID``. Optional."""

    ASSOCIATEDOIL: float | None = Field(default=None, ge=0.0)
    """The associated oil volume of the fluid-type given in ``FLUID``. Optional."""

    PORV: float | None = Field(default=None, ge=0.0)
    """The pore volume of the fluid-type given in ``FLUID``. Optional."""

    HCPV: float | None = Field(default=None, ge=0.0)
    """The hydrocarbon pore volume of the fluid-type given in ``FLUID``. Optional."""


class SimulatorInplaceVolumesResult(RootModel):
    """Represents the resultant simulator inplace volumes parquet file, which is
    naturally a list of rows.

    Consumers who retrieve this parquet file must read it into a json-dictionary
    equivalent format to validate it against the schema."""

    root: list[SimulatorInplaceVolumesResultRow]


class SimulatorInplaceVolumesSchema(SchemaBase):
    """This class represents the schema that is used to validate the inplace volumes
    table being exported. This means that the version, schema filename, and schema
    location corresponds directly with the values and their validation constraints,
    documented above."""

    VERSION: VersionStr = "0.1.0"

    VERSION_CHANGELOG: str = """
    #### 0.1.0

    This is the initial schema version.
    """

    FILENAME: str = "simulator_inplace_volumes.json"
    """The filename this schema is written to."""

    PATH: Path = FMU_SCHEMAS_PATH / "file_formats" / VERSION / FILENAME
    """The local and URL path of this schema."""

    @classmethod
    def dump(cls) -> dict[str, Any]:
        return SimulatorInplaceVolumesResult.model_json_schema(
            schema_generator=cls.default_generator()
        )
