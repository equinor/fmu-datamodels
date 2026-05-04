"""Data mapping models between systems."""

from collections.abc import Iterator
from enum import StrEnum
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import BaseModel, Field, RootModel, field_validator, model_validator


class MappingType(StrEnum):
    """The discriminator used between mapping types.

    Each of these types should have their own mapping class derived from a base
    mapping type, e.g. IdentifierMapping.
    """

    stratigraphy = "stratigraphy"
    wellbore = "wellbore"


class RelationType(StrEnum):
    """The kind of relation this mapping represents."""

    primary = "primary"
    """The main source identifier to use for this mapping."""

    alias = "alias"
    """Alias of a primary identifier."""


class DataSystem(StrEnum):
    """The system or application data is being mapping to or from."""

    rms = "rms"
    smda = "smda"
    simulator = "simulator"
    pdm = "pdm"


class BaseMapping(BaseModel):
    """The base mapping containing the fields all mappings should contain."""

    source_system: DataSystem
    target_system: DataSystem
    mapping_type: MappingType
    relation_type: RelationType

    @model_validator(mode="after")
    def validate_systems_differ(self) -> "BaseMapping":
        """Ensure source and target systems are different."""

        if self.source_system == self.target_system:
            raise ValueError(
                f"source_system and target_system must differ, "
                f"both are '{self.source_system}'"
            )
        return self


class IdentifierMapping(BaseMapping):
    """Base class for a one-to-one mapping of identifiers.

    This mapping represents an identifier from one source and correlates it to an
    identifier in a target. Most often this target will be some official masterdata
    store like SMDA.
    """

    source_id: str
    source_uuid: UUID | None = None
    target_id: str
    target_uuid: UUID | None = None

    @field_validator("source_id", "target_id")
    def validate_ids_not_empty(cls: Self, v: str) -> str:
        """Ensure IDs are not empty strings."""
        if not v or not v.strip():
            raise ValueError("An identifier cannot be an empty string")
        return v.strip()


class StratigraphyIdentifierMapping(IdentifierMapping):
    """Represents a stratigraphy mapping.

    This is a mapping from stratigraphic identifiers (tops, zones, etc.) to official
    identifiers in SMDA.
    """

    mapping_type: Literal[MappingType.stratigraphy] = MappingType.stratigraphy


class WellboreIdentifierMapping(IdentifierMapping):
    """Represents a wellbore mapping.

    This is a mapping from wellbore identifiers to official identifiers in SMDA/PDM.
    """

    mapping_type: Literal[MappingType.wellbore] = MappingType.wellbore


AnyIdentifierMapping = Annotated[
    StratigraphyIdentifierMapping | WellboreIdentifierMapping,
    Field(discriminator="mapping_type"),
]


class StratigraphyMappings(RootModel[list[StratigraphyIdentifierMapping]]):
    """Collection of all stratigraphy mappings."""

    root: list[StratigraphyIdentifierMapping]

    def __getitem__(self: Self, index: int) -> StratigraphyIdentifierMapping:
        """Retrieves a stratigraphy mapping from the list using the specified index."""
        return self.root[index]

    def __iter__(  # type: ignore[override]
        self: Self,
    ) -> Iterator[StratigraphyIdentifierMapping]:
        """Returns an iterator for the stratigraphy mappings."""
        return iter(self.root)

    def __len__(self: Self) -> int:
        """Returns the number of stratigraphy mappings."""
        return len(self.root)


class WellboreMappings(RootModel[list[WellboreIdentifierMapping]]):
    """Collection of all wellbore mappings."""

    root: list[WellboreIdentifierMapping]

    def __getitem__(self: Self, index: int) -> WellboreIdentifierMapping:
        """Retrieves a wellbore mapping from the list using the specified index."""
        return self.root[index]

    def __iter__(  # type: ignore[override]
        self: Self,
    ) -> Iterator[WellboreIdentifierMapping]:
        """Returns an iterator for the wellbore mappings."""
        return iter(self.root)

    def __len__(self: Self) -> int:
        """Returns the number of wellbore mappings."""
        return len(self.root)
