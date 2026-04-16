"""Tests for validators in the mapping models."""

import pytest
from pydantic import TypeAdapter

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


def test_base_mapping_validates_systems_differ() -> None:
    """Ensure that validation fails if a mapping maps to the same system."""
    with pytest.raises(ValueError, match="source_system and target_system must differ"):
        BaseMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.rms,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.primary,
        )


def test_base_mapping_allows_fmu_to_fmu_mappings() -> None:
    """Ensure that validation does not fail if FMU maps to FMU."""
    # Does not raise
    BaseMapping(
        source_system=DataSystem.fmu,
        target_system=DataSystem.fmu,
        mapping_type=MappingType.stratigraphy,
        relation_type=RelationType.primary,
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


def test_identifiers_equivalent_if_relation_equivalent() -> None:
    """Validation fails if the relation type is equivalent but identifiers are not."""
    with pytest.raises(ValueError, match="Equivalent mapping requires"):
        IdentifierMapping(
            source_system=DataSystem.rms,
            target_system=DataSystem.fmu,
            mapping_type=MappingType.stratigraphy,
            relation_type=RelationType.equivalent,
            source_id="bar",
            target_id="foo",
        )


def test_stratigraping_mappings_accessors() -> None:
    """Ensure all stratigraphy mapping methods work as expected."""
    primary = StratigraphyIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="VOLANTIS GP. Top",
    )
    alias1 = StratigraphyIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.alias,
        source_id="TopVOLANTIS",
        target_id="VOLANTIS GP. Top",
    )
    alias2 = StratigraphyIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="VOLANTIS GP. Top",
    )
    mappings = StratigraphyMappings(root=[primary, alias1, alias2])

    assert mappings.get_by_source(source_id="TopVOLANTIS") == [alias1]
    assert mappings.get_by_target(target_id="VOLANTIS GP. Top") == [
        primary,
        alias1,
        alias2,
    ]
    assert mappings.get_official_name(rms_name="TOP_VOLANTIS") == "VOLANTIS GP. Top"
    assert mappings.get_official_name(rms_name="TOPVOLANTIS") is None


def test_stratigrapy_mappings_dunder_methods() -> None:
    """Ensure stratigraphy mappings support indexing, iteration, and len()."""
    primary = StratigraphyIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.primary,
        source_id="TopVolantis",
        target_id="VOLANTIS GP. Top",
    )
    alias = StratigraphyIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.smda,
        relation_type=RelationType.alias,
        source_id="TOP_VOLANTIS",
        target_id="VOLANTIS GP. Top",
    )
    mappings = StratigraphyMappings(root=[primary, alias])
    expected = [primary, alias]

    assert mappings[0] == primary
    assert list(mappings) == expected
    assert len(mappings) == len(expected)


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
    mapping = WellboreIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=target_system,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id=target_id,
    )

    assert mapping.target_system == target_system
    assert mapping.target_id == target_id


def test_wellbore_mappings_dunder_methods() -> None:
    """Ensure wellbore mappings support indexing, iteration, and len()."""
    first = WellboreIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.simulator,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="B21C",
    )
    second = WellboreIdentifierMapping(
        source_system=DataSystem.rms,
        target_system=DataSystem.pdm,
        relation_type=RelationType.primary,
        source_id="30_9-B-21_C",
        target_id="30/9-B-21 C",
    )
    mappings = WellboreMappings(root=[first, second])
    expected = [first, second]

    assert mappings[0] == first
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
