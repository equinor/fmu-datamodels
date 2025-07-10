import pytest
from pydantic import ValidationError

from fmu.datamodels.fmu_results.fmu_results import FmuResults, FmuResultsSchema


def test_version_string_type(fluid_contact_metadata: dict) -> None:
    """Tests fmu.datamodels.types.VerionStr."""

    # assert validation as-is
    FmuResults.model_validate(fluid_contact_metadata)

    # assert validation fails when version pattern is invalid
    fluid_contact_metadata["version"] = "1.2.a"
    with pytest.raises(ValidationError, match="String should match pattern"):
        FmuResults.model_validate(fluid_contact_metadata)

    fluid_contact_metadata["version"] = "1.2"
    with pytest.raises(ValidationError, match="String should match pattern"):
        FmuResults.model_validate(fluid_contact_metadata)

    # assert version default if version not set
    del fluid_contact_metadata["version"]
    assert "version" not in fluid_contact_metadata
    model = FmuResults.model_validate(fluid_contact_metadata)
    assert model.root.version == FmuResultsSchema.VERSION
