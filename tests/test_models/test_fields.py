"""Test the pydantic schema"""

from copy import deepcopy
from typing import get_args
from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError

from fmu.datamodels import FmuResults
from fmu.datamodels.common.enums import Classification
from fmu.datamodels.fmu_results.fields import Aggregation, Realization


def test_for_optional_fields_without_default(
    pydantic_models_from_root: set[type[BaseModel]],
) -> None:
    """Test that all optional fields have a default value."""

    optionals_without_default = []
    for model in pydantic_models_from_root:
        for field_name, field_info in model.model_fields.items():
            if (
                type(None) in get_args(field_info.annotation)
                and field_info.is_required()
            ):
                optionals_without_default.append(
                    f"{model.__module__}.{model.__name__}.{field_name}"
                )

    assert not optionals_without_default


def test_fmu_field(case_metadata: dict, field_region_metadata: dict) -> None:
    """Asserting validation failure when illegal contents in fmu block."""

    # assert validation as-is
    FmuResults.model_validate(case_metadata)
    FmuResults.model_validate(field_region_metadata)

    # assert validation error when "fmu" is missing
    _example = deepcopy(case_metadata)
    del _example["fmu"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_example)

    _example = deepcopy(field_region_metadata)
    del _example["fmu"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_example)

    # assert validation error when "fmu.model" is missing
    _example = deepcopy(case_metadata)
    del _example["fmu"]["model"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_example)

    _example = deepcopy(field_region_metadata)
    del _example["fmu"]["model"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(_example)


def test_masterdata_smda_field(
    case_metadata: dict, field_outline_metadata: dict
) -> None:
    """Test schema logic for masterdata.smda."""

    for metadata in [case_metadata, field_outline_metadata]:
        # assert validation as-is
        FmuResults.model_validate(metadata)

        # assert validation error when masterdata block is missing
        _example = deepcopy(metadata)
        del _example["masterdata"]
        with pytest.raises(ValidationError):
            FmuResults.model_validate(_example)

        # assert validation error when masterdata.smda is missing
        _example = deepcopy(metadata)
        del _example["masterdata"]["smda"]
        with pytest.raises(ValidationError):
            FmuResults.model_validate(_example)

        # assert validation error when missing attribute
        for block in [
            "country",
            "discovery",
            "field",
            "coordinate_system",
            "stratigraphic_column",
        ]:
            _example = deepcopy(metadata)
            del _example["masterdata"]["smda"][block]
            with pytest.raises(ValidationError):
                FmuResults.model_validate(_example)

        # assert validation error if not correct type
        for block, type_ in [
            ("country", list),
            ("discovery", list),
            ("coordinate_system", dict),
            ("stratigraphic_column", dict),
        ]:
            _example = deepcopy(metadata)
            assert isinstance(_example["masterdata"]["smda"][block], type_)

            _example["masterdata"]["smda"][block] = "somestring"

            with pytest.raises(ValidationError):
                FmuResults.model_validate(_example)


def test_file_field(fluid_contact_metadata: dict) -> None:
    """Test variations on the file block."""

    # assert validation as-is
    FmuResults.model_validate(fluid_contact_metadata)

    # shall validate without absolute_path
    del fluid_contact_metadata["file"]["absolute_path"]
    FmuResults.model_validate(fluid_contact_metadata)

    # shall not validate when md5 checksum is not a string
    valid_checksum = fluid_contact_metadata["file"]["checksum_md5"]
    fluid_contact_metadata["file"]["checksum_md5"] = 123.4
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)

    # shall not validate without checksum_md5
    del fluid_contact_metadata["file"]["checksum_md5"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)

    # shall validate when checksum is put back in
    fluid_contact_metadata["file"]["checksum_md5"] = valid_checksum
    FmuResults.model_validate(fluid_contact_metadata)

    # shall not validate without relative_path
    del fluid_contact_metadata["file"]["relative_path"]
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)


def test_aggregation_and_realalization_field(fluid_contact_metadata: dict) -> None:
    """Test that fmu.realization and fmu.aggregation
    are not allowed at the same time."""

    # assert validation as-is
    FmuResults.model_validate(fluid_contact_metadata)

    # add realization block to test data
    fluid_contact_metadata["fmu"]["realization"] = Realization(
        id=0,
        name="realization-0",
        uuid=UUID("00000000-0000-0000-0000-000000000000"),
        is_reference=None,
    ).model_dump(mode="json", exclude_none=True, by_alias=True)

    # check that assumptions for the test is true
    assert "realization" in fluid_contact_metadata["fmu"]
    assert "aggregation" not in fluid_contact_metadata["fmu"]

    # assert validation with realization set
    FmuResults.model_validate(fluid_contact_metadata)

    # add aggregation block to test data
    fluid_contact_metadata["fmu"]["realization"] = Aggregation(
        id=UUID("15ce3b84-766f-4c93-9050-b154861f9100"),
        operation="std",
        realization_ids=[0, 1, 9],
    ).model_dump(mode="json", exclude_none=True, by_alias=True)

    # assert validation fail when both realization and aggregation are set
    with pytest.raises(ValidationError):
        FmuResults.model_validate(fluid_contact_metadata)


@pytest.mark.parametrize("classification", Classification)
def test_access_field(
    case_metadata: dict, seismic_metadata: dict, classification: dict
) -> None:
    """Test the classification of individual files."""

    # assert valid classification validates
    case_metadata["access"]["classification"] = classification
    FmuResults.model_validate(case_metadata)

    seismic_metadata["access"]["ssdl"]["access_level"] = classification
    FmuResults.model_validate(seismic_metadata)

    # assert erroneous value does not validate
    case_metadata["access"]["classification"] = "open"
    with pytest.raises(ValidationError):
        FmuResults.model_validate(case_metadata)

    seismic_metadata["access"]["ssdl"]["access_level"] = "open"
    with pytest.raises(ValidationError):
        FmuResults.model_validate(seismic_metadata)
