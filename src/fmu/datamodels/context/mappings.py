"""Data mapping models between systems."""

from enum import StrEnum
from typing import Annotated, Any, Literal, Self
from uuid import UUID

from pydantic import BaseModel, Field, RootModel, field_validator, model_validator


class MappingType(StrEnum):
    """The discriminator used between mapping types.

    Each of these types should have their own mapping class derived from a base
    mapping type, e.g. IdentifierMapping.
    """

    stratigraphy = "stratigraphy"


class RelationType(StrEnum):
    """The kind of relation this mapping represents."""

    primary = "primary"
    """The primary unofficial identifier."""

    alias = "alias"
    """Alias of a primary unofficial identifier."""

    equivalent = "equivalent"
    """A name used in the source system that is the same as the official name.

    For example, if an RMS stratigraphic name is the same as the SMDA name."""


class DataSystem(StrEnum):
    """The system or application data is being mapping to or from."""

    rms = "rms"
    smda = "smda"
    fmu = "fmu"


class BaseMapping(BaseModel):
    """The base mapping containing the fields all mappings should contain."""

    source_system: DataSystem
    target_system: DataSystem
    mapping_type: MappingType
    relation_type: RelationType

    @model_validator(mode="after")
    def validate_systems_differ(self) -> "BaseMapping":
        """Ensure source and target systems are different.

        Mappings between FMU sources are allowed.
        """
        if self.source_system == self.target_system == DataSystem.fmu:
            return self

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
            raise ValueError("ID cannot be empty.")
        return v.strip()


class StratigraphyIdentifierMapping(IdentifierMapping):
    """Represents a stratigraphy mapping.

    This is a mapping from stratigraphic identifiers (tops, zones, etc.) to official
    identifiers in SMDA.
    """

    mapping_type: Literal[MappingType.stratigraphy] = MappingType.stratigraphy


AnyIdentifierMapping = Annotated[
    StratigraphyIdentifierMapping, Field(discriminator="mapping_type")
]


class StratigraphyMappings(RootModel[list[StratigraphyIdentifierMapping]]):
    """Collection of all stratigraphy mappings."""

    root: list[StratigraphyIdentifierMapping]

    def get_by_source(
        self, source_id: str, source_system: DataSystem = DataSystem.rms
    ) -> list[StratigraphyIdentifierMapping]:
        """Get all stratigraphy mappings from a source identifier."""
        return [
            m
            for m in self.root
            if m.source_id == source_id and m.source_system == source_system
        ]

    def get_by_target(
        self,
        target_id: str,
        target_system: DataSystem = DataSystem.smda,
    ) -> list[StratigraphyIdentifierMapping]:
        """Get all stratigraphy mappings to a target identifier."""
        return [
            m
            for m in self.root
            if m.target_id == target_id and m.target_system == target_system
        ]

    def get_official_name(
        self,
        rms_name: str,
    ) -> str | None:
        """Get the official SMDA name for an RMS stratigraphy identifier.

        Args:
            rms_name: The RMS name

        Returns:
            The official SMDA name, or None if not found
        """
        mappings = [
            m
            for m in self.root
            if m.source_id == rms_name
            and m.source_system == DataSystem.rms
            and m.target_system == DataSystem.smda
        ]
        return mappings[0].target_id if mappings else None


class MappingGroup(BaseModel):
    """A mapping group containing a primary mapping and its related mappings.

    This is a _view_ of the data for GUI display purposes, not how it's stored.
    Groups all mappings (primary, aliases, equivalents) that share the same target.

    Expects that mappings have already been filtered down to include only mappings that
    map to 'target_id' in the target system.
    """

    target_id: str
    target_system: DataSystem
    mappings: list[AnyIdentifierMapping]

    @property
    def primary(self) -> AnyIdentifierMapping | None:
        """Get the primary mapping.

        Takes the first primary, which should be the only one."""
        primaries = [
            m for m in self.mappings if m.relation_type == RelationType.primary
        ]
        return primaries[0] if primaries else None

    @property
    def aliases(self) -> list[AnyIdentifierMapping]:
        """Get all alias mappings."""
        return [m for m in self.mappings if m.relation_type == RelationType.alias]

    @property
    def equivalents(self) -> list[AnyIdentifierMapping]:
        """Get all equivalent mappings."""
        return [m for m in self.mappings if m.relation_type == RelationType.equivalent]

    def to_display_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for display."""
        return {
            "official_name": self.target_id,
            "primary_source": self.primary.source_id if self.primary else None,
            "aliases": [m.source_id for m in self.aliases],
            "equivalents": [m.source_id for m in self.equivalents],
        }
