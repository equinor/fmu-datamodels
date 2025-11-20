"""Tests for validators in the mapping models."""

import pytest

from fmu.datamodels.context.mappings import (
    BaseMapping,
    DataSystem,
    IdentifierMapping,
    MappingType,
    RelationType,
    StratigraphyIdentifierMapping,
    StratigraphyMappings,
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
