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

        if self.source_system == self.target_system:
            # Allow FMU to map to FMU.
            if self.source_system == DataSystem.fmu:
                return self

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

    @model_validator(mode="after")
    def validate_equivalent_relation(self) -> Self:
        """Ensure relation_type=equivalent is only used when source and target match."""
        if (
            self.relation_type == RelationType.equivalent
            and self.source_id != self.target_id
        ):
            raise ValueError(
                "Equivalent mapping requires matching source_id/target_id; "
                f"got source_id='{self.source_id}', target_id='{self.target_id}'"
            )
        return self


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
