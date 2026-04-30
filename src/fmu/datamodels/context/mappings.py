"""Data mapping models between systems."""

from collections.abc import Iterator, Sequence
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

    unmappable = "unmappable"
    """A source identifier that has been reviewed and cannot be mapped.

    This means the identifier has been checked, but no matching identifier exists
    in the target system.
    """


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
    def validate_relation_system_constraints(self) -> "BaseMapping":
        """Validate which relation types are allowed for same vs cross-system mappings.

        Same-system mappings can only be ``primary`` or ``alias``.
        Cross-system mappings can only be ``primary`` or ``unmappable``.
        """

        if self.source_system == self.target_system:
            if self.relation_type == RelationType.unmappable:
                raise ValueError(
                    "Same-system mapping cannot use relation_type 'unmappable'"
                )
            return self

        if self.relation_type == RelationType.alias:
            raise ValueError("Cross-system mapping cannot use relation_type 'alias'")

        return self


class IdentifierMapping(BaseMapping):
    """Base class for a one-to-one mapping of identifiers.

    This mapping represents an identifier from one source and correlates it to an
    identifier in a target. Most often this target will be some official masterdata
    store like SMDA.
    """

    source_id: str
    source_uuid: UUID | None = None
    target_id: str | None = None
    target_uuid: UUID | None = None

    @field_validator("source_id")
    def validate_source_id_not_empty(cls: Self, v: str) -> str:
        """Ensure source IDs are not empty strings."""
        if not v or not v.strip():
            raise ValueError("An identifier cannot be an empty string")
        return v.strip()

    @field_validator("target_id")
    def validate_target_id_not_empty(cls: Self, v: str | None) -> str | None:
        """Ensure target IDs are not empty strings when provided."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("An identifier cannot be an empty string")
        return v.strip()

    @model_validator(mode="after")
    def validate_relation_target_constraints(self) -> Self:
        """Validate how ``source_id`` and ``target_id`` are allowed to relate.

        This means:
        - ``unmappable`` mappings must leave the target empty
        - all other mappings must provide a target
        - same-system ``primary`` mappings must use the same ``source_id`` and
          ``target_id``
        - same-system ``alias`` mappings must point to a different same-system
          ``target_id``
        """
        if self.relation_type == RelationType.unmappable:
            if self.target_id is not None or self.target_uuid is not None:
                raise ValueError(
                    "Unmappable mapping cannot define target_id or target_uuid"
                )
            return self

        if self.target_id is None:
            raise ValueError(
                "target_id is required unless relation_type is 'unmappable'"
            )

        if self.source_system == self.target_system:
            if self.relation_type == RelationType.primary:
                if self.source_id != self.target_id:
                    raise ValueError(
                        "Same-system primary mapping must have matching "
                        "source_id and target_id; use relation_type='alias' "
                        "if they should differ"
                    )
                return self

            if self.relation_type == RelationType.alias:
                if self.source_id == self.target_id:
                    raise ValueError(
                        "Same-system alias mapping must have different "
                        "source_id and target_id; use relation_type='primary' "
                        "if they should match"
                    )
                return self

        return self


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


def _validate_identifier_mappings_collection(
    mappings: Sequence[IdentifierMapping],
) -> None:
    """Validate how mappings are allowed to fit together.

    The collection must satisfy three invariants:

    - A same-system ``source_id`` can appear only once per mapping type.
      Example valid mappings::

          rms -> rms, primary, source_id="TopVolantis", target_id="TopVolantis"
          rms -> rms, alias, source_id="TOP_VOLANTIS", target_id="TopVolantis"

      Example invalid mappings::

          rms -> rms, primary, source_id="TopVolantis", target_id="TopVolantis"
          rms -> rms, alias, source_id="TopVolantis", target_id="TopVolon"

      The second mapping is invalid because ``TopVolantis`` is reused as a
      same-system ``source_id``.

    - Same-system alias mappings must point to an existing same-system primary
      mapping.
      Example valid mappings::

          rms -> rms, primary, source_id="TopVolantis", target_id="TopVolantis"
          rms -> rms, alias, source_id="TOP_VOLANTIS", target_id="TopVolantis"

      Example invalid mapping::

          rms -> rms, alias, source_id="TOP_VOLANTIS", target_id="TopVolantis"

      The alias is invalid on its own because there is no same-system primary
      mapping for ``TopVolantis``.

    - Cross-system mappings must originate from a same-system primary mapping and
      can appear only once per target system.
      Example valid mappings::

          rms -> rms, primary, source_id="TopVolantis", target_id="TopVolantis"
          rms -> smda, primary, source_id="TopVolantis", target_id="VOLANTIS GP. Top"

      Example invalid mappings::

          rms -> rms, alias, source_id="TOP_VOLANTIS", target_id="TopVolantis"
          rms -> smda, primary, source_id="TOP_VOLANTIS", target_id="VOLANTIS GP. Top"

      The cross-system mapping is invalid because it starts from an alias instead
      of a same-system primary. It is also invalid to add two ``rms -> smda``
      mappings for the same ``source_id``.
    """
    same_system_source_keys: set[tuple[DataSystem, MappingType, str]] = set()
    same_system_primary_source_keys: set[tuple[DataSystem, MappingType, str]] = set()
    same_system_aliases: list[IdentifierMapping] = []
    cross_system_source_keys: set[tuple[MappingType, DataSystem, DataSystem, str]] = (
        set()
    )
    cross_system_mappings: list[IdentifierMapping] = []

    for mapping in mappings:
        source_key = (
            mapping.source_system,
            mapping.mapping_type,
            mapping.source_id,
        )

        # Same-system mappings tell us which source_id is the primary and which
        # source_ids are aliases of that primary.
        if mapping.source_system == mapping.target_system:
            if source_key in same_system_source_keys:
                raise ValueError("Same-system mappings cannot reuse the same source_id")
            same_system_source_keys.add(source_key)

            if mapping.relation_type == RelationType.primary:
                same_system_primary_source_keys.add(source_key)
            else:
                same_system_aliases.append(mapping)
            continue

        # A source_id can map to each target system only once.
        cross_system_key = (
            mapping.mapping_type,
            mapping.source_system,
            mapping.target_system,
            mapping.source_id,
        )
        if cross_system_key in cross_system_source_keys:
            raise ValueError(
                "A source_id can only have one cross-system mapping per target system"
            )
        cross_system_source_keys.add(cross_system_key)
        cross_system_mappings.append(mapping)

    # Every alias must point to a same-system primary source_id that already
    # exists in the collection.
    for mapping in same_system_aliases:
        primary_target_id = mapping.target_id
        assert primary_target_id is not None
        primary_target_key = (
            mapping.source_system,
            mapping.mapping_type,
            primary_target_id,
        )
        if primary_target_key not in same_system_primary_source_keys:
            raise ValueError(
                "Same-system alias mappings must point to an existing "
                "same-system primary source_id"
            )

    # Cross-system mappings are only allowed when they start from a same-system
    # primary source_id.
    for mapping in cross_system_mappings:
        primary_source_key = (
            mapping.source_system,
            mapping.mapping_type,
            mapping.source_id,
        )
        if primary_source_key not in same_system_primary_source_keys:
            raise ValueError(
                "Cross-system mappings must use a source_id that is defined "
                "as a same-system primary"
            )


class StratigraphyMappings(RootModel[list[StratigraphyIdentifierMapping]]):
    """Collection of all stratigraphy mappings."""

    root: list[StratigraphyIdentifierMapping]

    @model_validator(mode="after")
    def validate_collection(self) -> Self:
        """Ensure the mapping collection follows the allowed mapping rules."""
        _validate_identifier_mappings_collection(self.root)
        return self

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

    @model_validator(mode="after")
    def validate_collection(self) -> Self:
        """Ensure the mapping collection follows the allowed mapping rules."""
        # Wellbore mappings are not expected to use aliases today, but reusing the
        # shared identifier-mapping rules keeps the validation consistent if that
        # changes later.
        _validate_identifier_mappings_collection(self.root)
        return self

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
