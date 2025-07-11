from copy import deepcopy
from typing import Literal, get_args, get_origin

import pytest
from pydantic import ValidationError

from fmu.datamodels.fmu_results import data, enums
from fmu.datamodels.fmu_results.fmu_results import (
    FmuResults,
    FmuResultsSchema,
    ObjectMetadata,
)
from tests.utils import _get_pydantic_models_from_annotation


def test_all_content_enums_in_anydata() -> None:
    """Test that all content enums are represented with a model in AnyData."""

    anydata_models = _get_pydantic_models_from_annotation(
        data.AnyData.model_fields["root"].annotation
    )

    content_enums_in_anydata = []
    for model in anydata_models:
        # content is used as a discriminator in AnyData and
        # should be present for all models
        assert "content" in model.model_fields
        content_annotation = model.model_fields["content"].annotation

        # check that the annotation is a Literal
        assert get_origin(content_annotation) == Literal

        # get_args will unpack the enum from the Literal
        # into a tuple, should only be one Literal value
        assert len(get_args(content_annotation)) == 1

        # the literal value should be an enum
        content_enum = get_args(content_annotation)[0]
        assert isinstance(content_enum, enums.Content)

        content_enums_in_anydata.append(content_enum)

    # finally check that all content enums are represented
    for content_enum in enums.Content:
        assert content_enum in content_enums_in_anydata

    # and that number of models in AnyData matches number of content enums
    assert len(anydata_models) == len(enums.Content)


def test_content_whitelist(fluid_contact_metadata: dict) -> None:
    """Test that validation fails when value of data.content is not in
    the whitelist."""

    # assert validation as-is
    FmuResults.model_validate(fluid_contact_metadata)

    # shall fail when content is not in whitelist
    fluid_contact_metadata["data"]["content"] = "not_valid_content"
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)


def test_content_fluid_contact(fluid_contact_metadata: dict) -> None:
    """Test content-specific rule.

    When content == fluid_contact, require the fluid_contact field
    """

    # assert validation as-is
    FmuResults.model_validate(fluid_contact_metadata)

    # check that assumptions for the test is true
    assert fluid_contact_metadata["data"]["content"] == "fluid_contact"
    assert "fluid_contact" in fluid_contact_metadata["data"]
    assert "contact" in fluid_contact_metadata["data"]["fluid_contact"]

    # assert that data.fluid_contact is required
    _metadata = deepcopy(fluid_contact_metadata)
    del _metadata["data"]["fluid_contact"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    # assert that data.fluid_contact.contact is required
    _metadata = deepcopy(fluid_contact_metadata)
    del _metadata["data"]["fluid_contact"]["contact"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)


def test_content_field_outline(field_outline_metadata: dict) -> None:
    """Test content-specific rule.

    When content == field_outline, require the field_outline field.
    """

    # assert validation as-is
    FmuResults.model_validate(field_outline_metadata)

    # check that assumptions for the test is true
    assert field_outline_metadata["data"]["content"] == "field_outline"
    assert "field_outline" in field_outline_metadata["data"]
    assert "contact" in field_outline_metadata["data"]["field_outline"]

    # assert that data.field_outline is required
    _metadata = deepcopy(field_outline_metadata)
    del _metadata["data"]["field_outline"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    # assert that data.field_region.contact is required
    _metadata = deepcopy(field_outline_metadata)
    del _metadata["data"]["field_outline"]["contact"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)


def test_content_field_region(field_region_metadata: dict) -> None:
    """Test content-specific rule: field_region.

    When content == field_region, require the data.field_region field.
    """

    # check assumptions
    assert field_region_metadata["data"]["content"] == "field_region"
    assert "field_region" in field_region_metadata["data"]
    assert "id" in field_region_metadata["data"]["field_region"]

    # assert validation as-is
    FmuResults.model_validate(field_region_metadata)

    # assert that data.field_region is required
    _metadata = deepcopy(field_region_metadata)
    del _metadata["data"]["field_region"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    # assert that data.field_region.id is required and a number
    _metadata = deepcopy(field_region_metadata)
    del _metadata["data"]["field_region"]["id"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    field_region_metadata["data"]["field_region"]["id"] = "NotANumber"
    with pytest.raises(ValidationError):
        FmuResults.model_validate(field_region_metadata)


def test_content_seismic(seismic_metadata: dict) -> None:
    """Test content-specific rule: seismic.

    When content == seismic, require the data.seismic field.
    """

    # check assumptions
    assert seismic_metadata["data"]["content"] == "seismic"
    assert "seismic" in seismic_metadata["data"]

    # assert validation as-is
    FmuResults.model_validate(seismic_metadata)

    # assert that data.seismic is required
    _metadata = deepcopy(seismic_metadata)
    del _metadata["data"]["seismic"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)


def test_data_top_and_base(seismic_metadata: dict) -> None:
    """Test require data.top and data.base.

    * Require both data.top and data.base, or none.
    """

    # assert validation as-is
    FmuResults.model_validate(seismic_metadata)

    # check that assumptions for the test is true
    assert "top" in seismic_metadata["data"]
    assert "base" in seismic_metadata["data"]

    # remove "top" - shall fail
    _metadata = deepcopy(seismic_metadata)
    del _metadata["data"]["top"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    # remove "base" - shall fail
    _metadata = deepcopy(seismic_metadata)
    del _metadata["data"]["base"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_metadata)

    # remove both - shall pass
    del seismic_metadata["data"]["top"]
    del seismic_metadata["data"]["base"]
    assert "top" not in seismic_metadata["data"]  # test assumption
    assert "base" not in seismic_metadata["data"]  # test assumption
    FmuResults.model_validate(seismic_metadata)


def test_data_time(seismic_metadata: dict) -> None:
    """Test schema logic for data.time."""

    # assert validation as-is
    FmuResults.model_validate(seismic_metadata)

    # check that assumptions for the test is true
    assert "time" in seismic_metadata["data"]

    # valid when data.time is missing
    _example = deepcopy(seismic_metadata)
    del _example["data"]["time"]
    FmuResults.model_validate(_example)

    # valid when only t0
    _example = deepcopy(seismic_metadata)
    del _example["data"]["time"]["t1"]
    assert "t0" in _example["data"]["time"]  # test assumption
    FmuResults.model_validate(_example)

    # valid without labels
    _example = deepcopy(seismic_metadata)
    del _example["data"]["time"]["t0"]["label"]
    FmuResults.model_validate(_example)

    # NOT valid when other types
    for testvalue in [
        [{"t0": "2020-10-28T14:28:02", "label": "mylabel"}],
        "2020-10-28T14:28:02",
        123,
        123.4,
    ]:
        _example = deepcopy(seismic_metadata)
        _example["data"]["time"] = testvalue
        with pytest.raises(ValidationError):
            FmuResults.model_validate(_example)


def test_data_spec(
    fluid_contact_metadata: dict,
    volumes_metadata: dict,
    field_region_metadata: dict,
) -> None:
    """Test schema logic for data.spec."""

    # assert data.spec required when class == surface
    FmuResults.model_validate(fluid_contact_metadata)
    assert fluid_contact_metadata["class"] == "surface"
    assert "spec" in fluid_contact_metadata["data"]

    del fluid_contact_metadata["data"]["spec"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)

    # assert data.spec required when class == table
    FmuResults.model_validate(volumes_metadata)
    assert volumes_metadata["class"] == "table"
    assert "spec" in volumes_metadata["data"]

    del volumes_metadata["data"]["spec"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(volumes_metadata)

    # assert data.spec not required when class == polygons
    FmuResults.model_validate(field_region_metadata)
    assert field_region_metadata["class"] == "polygons"
    assert "spec" in field_region_metadata["data"]

    del field_region_metadata["data"]["spec"]
    FmuResults.model_validate(field_region_metadata)


def test_zmin_zmax_not_present_for_surfaces(fluid_contact_metadata: dict) -> None:
    """
    Test that the validation works for surface metadata without
    zmin/zmax info or with zmin/zmax = None.
    """

    # assert validation as-is
    model = FmuResults.model_validate(fluid_contact_metadata)

    # assert that bbox is 3D
    assert isinstance(model.root, ObjectMetadata)
    assert isinstance(model.root.data.root.bbox, data.BoundingBox3D)

    # assert validation works with zmin/zmax = None, bbox should be 2D
    fluid_contact_metadata["data"]["bbox"]["zmin"] = None
    fluid_contact_metadata["data"]["bbox"]["zmax"] = None
    model = FmuResults.model_validate(fluid_contact_metadata)
    assert isinstance(model.root, ObjectMetadata)
    assert isinstance(model.root.data.root.bbox, data.BoundingBox2D)

    # assert validation works without zmin/zmax, bbox should be 2D
    del fluid_contact_metadata["data"]["bbox"]["zmin"]
    del fluid_contact_metadata["data"]["bbox"]["zmax"]
    model = FmuResults.model_validate(fluid_contact_metadata)
    assert isinstance(model.root, ObjectMetadata)
    assert isinstance(model.root.data.root.bbox, data.BoundingBox2D)


def test_isodatetime_format_for_time() -> None:
    """Test that the format for timestamps is set to iso-date-time
    instead of datetime that pydantic resolves it to."""

    schema = FmuResultsSchema.dump()
    timestamp_value = schema["$defs"]["Timestamp"]["properties"]["value"]

    assert timestamp_value["format"] == "iso-date-time"
