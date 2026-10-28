import pytest
from pydantic import TypeAdapter, ValidationError

from fmu.datamodels.fmu_results.fmu_results import FmuResults, FmuResultsSchema
from fmu.datamodels.types import MD5HashStr


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


@pytest.mark.parametrize(
    "checksum",
    [
        "5d41402AbC4b2a76b9719d911017c592",  # mixed-case hex
        "XUFAKrxLKna5cZ2REBfFkg==",  # base64
    ],
)
def test_md5_hash_encodings(checksum: str, fluid_contact_metadata: dict) -> None:
    """Accept both MD5 encodings and preserve them in metadata JSON."""
    assert TypeAdapter(MD5HashStr).validate_python(checksum) == checksum
    fluid_contact_metadata["file"]["checksum_md5"] = checksum
    model = FmuResults.model_validate(fluid_contact_metadata)
    assert model.model_dump(mode="json")["file"]["checksum_md5"] == checksum
    restored = FmuResults.model_validate_json(model.model_dump_json(by_alias=True))
    assert restored.model_dump(mode="json")["file"]["checksum_md5"] == checksum


@pytest.mark.parametrize(
    "checksum",
    [
        "zd41402abc4b2a76b9719d911017c592",  # invalid hex character
        "XUFAKrxLKna5cZ2REBfFkg",  # missing base64 padding
        "XUFAKrxLKna5cZ2REBfFkh==",  # nonzero padding bits
        "AAAAAAAAAAAAAAAAAAAAAAA=",  # base64 for 17 bytes instead of 16
    ],
)
def test_md5_hash_invalid_encodings(checksum: str) -> None:
    """Reject values that cannot represent an MD5 digest in an accepted format."""
    with pytest.raises(ValidationError, match="String should match pattern"):
        TypeAdapter(MD5HashStr).validate_python(checksum)
