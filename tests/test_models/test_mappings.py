"""Tests for validators in the mapping models."""

from uuid import uuid4

import pytest
from pydantic import TypeAdapter, ValidationError

from fmu.datamodels.context.mappings import (
    AnyIdentifierMapping,
    BaseMapping,
    DataSystem,
    IdentifierMapping,
    MappingType,
    RelationType,
    StratigraphyIdentifierMapping,
    StratigraphyMappings,
    WellboreIdentifierMapping,
    WellboreMappings,
)


def create_stratigraphy_mapping(
    *,
    source_system: DataSystem = DataSystem.rms,
    target_system: DataSystem = DataSystem.smda,
    relation_type: RelationType = RelationType.primary,
    source_id: str = "TopVolantis",
    target_id: str | None = "VOLANTIS GP. Top",
) -> StratigraphyIdentifierMapping:
    """Build a stratigraphy mapping with sensible defaults for tests."""
    return StratigraphyIdentifierMapping(
        source_system=source_system,
        target_system=target_system,
        relation_type=relation_type,
        source_id=source_id,
        target_id=target_id,
    )


def create_wellbore_mapping(
    *,
    source_system: DataSystem = DataSystem.rms,
    target_system: DataSystem = DataSystem.smda,
    relation_type: RelationType = RelationType.primary,
    source_id: str = "30_9-B-21_C",
    target_id: str | None = "NO 30/9-B-21 C",
) -> WellboreIdentifierMapping:
    """Build a wellbore mapping with sensible defaults for tests."""
    return WellboreIdentifierMapping(
        source_system=source_system,
        target_system=target_system,
        relation_type=relation_type,
        source_id=source_id,
        target_id=target_id,
    )


@pytest.mark.parametrize("relation_type", [RelationType.primary, RelationType.alias])
def test_base_mapping_allows_same_system_primary_and_alias(
    relation_type: RelationType,
) -> None:
    """Same-system primary and alias relations are allowed."""
    BaseMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        mapping_type=MappingType.stratigraphy,
        relation_type=relation_type,
    )


def test_base_mapping_rejects_same_system_unmappable() -> None:
    """Unmappable is only valid for cross-system mappings."""
    with pytest.raises(
        ValueError,
        match="Same-system mapping cannot use relation_type 'unmappable'",
    ):
        BaseMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.rms,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.unmappable,
        )


def test_base_mapping_rejects_cross_system_alias() -> None:
    """Alias is only valid for same-system mappings."""
    with pytest.raises(
        ValueError,
        match="Cross-system mapping cannot use relation_type 'alias'",
    ):
        BaseMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.smda,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.alias,
        )


def test_identifier_mapping_ids_not_empty_strings() -> None:
    """Ensure that validation fails if a mapping identifier is an empty string."""
    with pytest.raises(ValueError, match="An identifier cannot be an empty string"):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.fmu,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.primary,
            source_id="",
            target_id="foo",
        )


def test_identifier_mapping_strips_surrounding_whitespace_from_ids() -> None:
    """Source and target identifiers are stripped when they contain padding."""
    mapping = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="  TopVolantis  ",
        target_id="  VOLANTIS GP. Top  ",
    )

    assert mapping.source_id == "TopVolantis"
    assert mapping.target_id == "VOLANTIS GP. Top"


def test_identifier_mapping_allows_same_system_primary_mapping_to_itself() -> None:
    """Same-system primary mappings must map an identifier to itself."""
    mapping = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )

    assert mapping.source_id == mapping.target_id


def test_identifier_mapping_rejects_same_system_primary_to_other_identifier() -> None:
    """Same-system primary mappings cannot map an identifier to another one."""
    with pytest.raises(
        ValueError,
        match=(
            "Same-system primary mapping must have matching source_id and "
            "target_id; use relation_type='alias' if they should differ"
        ),
    ):
        create_stratigraphy_mapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.rms,
            relation_type=RelationType.primary,
            source_id="TopVolantis",
            target_id="TopVolon",
        )


def test_identifier_mapping_allows_same_system_alias() -> None:
    """Same-system aliases can point to a primary identifier."""
    mapping = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="TopVolantis",
    )

    assert mapping.source_id == "TOP_VOLANTIS"
    assert mapping.target_id == "TopVolantis"


def test_identifier_mapping_rejects_same_system_alias_mapping_to_itself() -> None:
    """Same-system aliases must point to a different identifier."""
    with pytest.raises(
        ValueError,
        match=(
            "Same-system alias mapping must have different source_id and "
            "target_id; use relation_type='primary' if they should match"
        ),
    ):
        create_stratigraphy_mapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.rms,
            relation_type=RelationType.alias,
            source_id="TopVolantis",
            target_id="TopVolantis",
        )


def test_identifier_mapping_rejects_same_system_unmappable() -> None:
    """Unmappable relations are not valid for same-system mappings."""
    with pytest.raises(
        ValueError,
        match="Same-system mapping cannot use relation_type 'unmappable'",
    ):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.rms,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.unmappable,
            source_id="NoMatch",
        )


def test_identifier_mapping_rejects_cross_system_alias() -> None:
    """Alias relations are not valid for cross-system mappings."""
    with pytest.raises(
        ValueError,
        match="Cross-system mapping cannot use relation_type 'alias'",
    ):
        create_stratigraphy_mapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.smda,
            relation_type=RelationType.alias,
            source_id="TOP_VOLANTIS",
            target_id="VOLANTIS GP. Top",
        )


def test_identifier_mapping_allows_unmappable_without_target() -> None:
    """An unmappable relation can omit target identifier fields."""
    mapping = IdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        mapping_type=MappingType.stratigraphy,
        relation_type=RelationType.unmappable,
        source_id="NoMatch",
    )

    assert mapping.target_id is None
    assert mapping.target_uuid is None


def test_identifier_mapping_allows_explicit_none_target_for_unmappable() -> None:
    """An unmappable relation also accepts an explicit null target identifier."""
    mapping = IdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        mapping_type=MappingType.stratigraphy,
        relation_type=RelationType.unmappable,
        source_id="NoMatch",
        target_id=None,
    )

    assert mapping.target_id is None


def test_identifier_mapping_rejects_blank_target_id() -> None:
    """Target identifiers cannot be blank when provided."""
    with pytest.raises(ValueError, match="An identifier cannot be an empty string"):
        create_stratigraphy_mapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.smda,
            relation_type=RelationType.primary,
            source_id="TopVolantis",
            target_id="   ",
        )


@pytest.mark.parametrize(
    ("target_system", "relation_type"),
    [
        (DataSystem.rms, RelationType.primary),
        (DataSystem.rms, RelationType.alias),
        (DataSystem.smda, RelationType.primary),
    ],
)
def test_identifier_mapping_requires_target_id_for_non_unmappable_relations(
    target_system: DataSystem,
    relation_type: RelationType,
) -> None:
    """All non-unmappable mappings require a target identifier."""
    with pytest.raises(
        ValueError,
        match="target_id is required unless relation_type is 'unmappable'",
    ):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=target_system,
            mapping_type=MappingType.stratigraphy,
            relation_type=relation_type,
            source_id="TopVolantis",
        )


def test_identifier_mapping_rejects_target_for_unmappable_relation() -> None:
    """Unmappable relations must not carry target identifier fields."""
    with pytest.raises(ValueError, match="Unmappable mapping cannot define"):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.smda,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.unmappable,
            source_id="NoMatch",
            target_id="VOLANTIS GP. Top",
        )


def test_identifier_mapping_rejects_target_uuid_for_unmappable_relation() -> None:
    """Unmappable relations must not carry target UUID fields."""
    with pytest.raises(ValueError, match="Unmappable mapping cannot define"):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.smda,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.unmappable,
            source_id="NoMatch",
            target_uuid=uuid4(),
        )


def test_stratigraphy_mappings_allow_empty_collection() -> None:
    """Stratigraphy collections can be empty when no mappings exist yet."""
    mappings = StratigraphyMappings(root=[])

    assert list(mappings) == []
    assert len(mappings) == 0


def test_stratigraphy_mappings_allow_valid_collection() -> None:
    """Stratigraphy collections allow valid mappings."""
    primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )
    alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="TopVolantis",
    )
    mapped = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="VOLANTIS GP. Top",
    )
    mappings = StratigraphyMappings(root=[primary, alias, mapped])
    expected = [primary, alias, mapped]

    assert mappings.root == expected


def test_stratigraphy_mappings_support_dunder_methods() -> None:
    """Stratigraphy collections support the expected dunder methods."""
    primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )
    alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="TopVolantis",
    )
    mapped = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="VOLANTIS GP. Top",
    )
    mappings = StratigraphyMappings(root=[primary, alias, mapped])
    expected = [primary, alias, mapped]

    assert mappings[0] == primary
    assert list(mappings) == expected
    assert len(mappings) == len(expected)


def test_stratigraphy_mappings_reject_alias_without_primary() -> None:
    """Same-system aliases must point to an existing same-system primary."""
    alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="TopVolantis",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Same-system alias mappings must point to an existing "
            "same-system primary source_id"
        ),
    ):
        StratigraphyMappings(root=[alias])


def test_stratigraphy_mappings_reject_cross_system_mappings_for_alias_sources() -> None:
    """Cross-system mappings must use same-system primary source identifiers."""
    primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )
    alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="TopVolantis",
    )
    mapped_alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TOP_VOLANTIS",
        target_id="VOLANTIS GP. Top",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Cross-system mappings must use a source_id that is defined "
            "as a same-system primary"
        ),
    ):
        StratigraphyMappings(root=[primary, alias, mapped_alias])


def test_stratigraphy_mappings_reject_multiple_cross_system_outcomes() -> None:
    """A same-system primary identifier can only have one outcome per target system."""
    primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )
    mapped = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="VOLANTIS GP. Top",
    )
    unmappable = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.unmappable,
        source_id="TopVolantis",
        target_id=None,
    )

    with pytest.raises(
        ValueError,
        match=("A source_id can only have one cross-system mapping per target system"),
    ):
        StratigraphyMappings(root=[primary, mapped, unmappable])


def test_stratigraphy_mappings_reject_reused_same_system_source_identifier() -> None:
    """A source_id cannot be both a primary and an alias in the same collection."""
    primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="TopVolantis",
    )
    other_primary = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="TopVolon",
        target_id="TopVolon",
    )
    conflicting_alias = create_stratigraphy_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.alias,
        source_id="TopVolantis",
        target_id="TopVolon",
    )

    with pytest.raises(
        ValueError,
        match=("Same-system mappings cannot reuse the same source_id"),
    ):
        StratigraphyMappings(root=[primary, other_primary, conflicting_alias])


@pytest.mark.parametrize(
    ("target_system", "target_id"),
    [
        (DataSystem.simulator, "B21C"),
        (DataSystem.smda, "NO 30/9-B-21 C"),
        (DataSystem.pdm, "30/9-B-21 C"),
    ],
)
def test_wellbore_mapping_supports_expected_target_systems(
    target_system: DataSystem, target_id: str
) -> None:
    """Ensure wellbore mappings can target the supported systems."""
    mapping = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=target_system,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id=target_id,
    )

    assert mapping.target_system == target_system
    assert mapping.target_id == target_id


def test_wellbore_mappings_allow_empty_collection() -> None:
    """Wellbore collections can be empty when no mappings exist yet."""
    mappings = WellboreMappings(root=[])

    assert list(mappings) == []
    assert len(mappings) == 0


def test_wellbore_mappings_allow_valid_collection() -> None:
    """Wellbore collections allow valid mappings."""
    primary = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="30_9-B-21_C",
    )
    simulator_target = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.simulator,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="B21C",
    )
    pdm_target = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.pdm,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="30/9-B-21 C",
    )
    mappings = WellboreMappings(root=[primary, simulator_target, pdm_target])
    expected = [primary, simulator_target, pdm_target]

    assert mappings.root == expected


def test_wellbore_mappings_support_dunder_methods() -> None:
    """Wellbore collections support the expected dunder methods."""
    primary = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.rms,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="30_9-B-21_C",
    )
    simulator_target = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.simulator,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="B21C",
    )
    pdm_target = create_wellbore_mapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.pdm,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="30/9-B-21 C",
    )
    mappings = WellboreMappings(root=[primary, simulator_target, pdm_target])
    expected = [primary, simulator_target, pdm_target]

    assert mappings[0] == primary
    assert list(mappings) == expected
    assert len(mappings) == len(expected)


@pytest.mark.parametrize(
    ("payload", "expected_type"),
    [
        (
            {
                "source_system": DataSystem.rms,
                "target_system": DataSystem.smda,
                "mapping_type": MappingType.stratigraphy,
                "relation_type": RelationType.primary,
                "source_id": "TopVolantis",
                "target_id": "VOLANTIS GP. Top",
            },
            StratigraphyIdentifierMapping,
        ),
        (
            {
                "source_system": DataSystem.rms,
                "target_system": DataSystem.smda,
                "mapping_type": MappingType.wellbore,
                "relation_type": RelationType.primary,
                "source_id": "30_9-B-21_C",
                "target_id": "NO 30/9-B-21 C",
            },
            WellboreIdentifierMapping,
        ),
    ],
)
def test_any_identifier_mapping_uses_mapping_type_discriminator(
    payload: dict[str, object], expected_type: type[IdentifierMapping]
) -> None:
    """Ensure the discriminator returns the concrete identifier mapping type."""
    parsed: IdentifierMapping = TypeAdapter(AnyIdentifierMapping).validate_python(
        payload
    )

    assert isinstance(parsed, expected_type)


def test_any_identifier_mapping_rejects_unknown_mapping_type() -> None:
    """Ensure invalid discriminator values fail validation."""
    payload = {
        "source_system": DataSystem.rms,
        "target_system": DataSystem.smda,
        "mapping_type": "unknown",
        "relation_type": RelationType.primary,
        "source_id": "TopVolantis",
        "target_id": "VOLANTIS GP. Top",
    }

    with pytest.raises(ValidationError, match="mapping_type"):
        TypeAdapter(AnyIdentifierMapping).validate_python(payload)
