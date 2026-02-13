import pytest
from pydantic import TypeAdapter

from fmu.datamodels.fmu_results.standard_result import AnyStandardResult
from fmu.datamodels.standard_results.enums import StandardResultName

StandardResultAdapter = TypeAdapter(AnyStandardResult)


@pytest.mark.parametrize("name", list(StandardResultName))
def test_all_standard_results_in_anystandardresult(name: StandardResultName) -> None:
    """Every StandardResultName resolves to a valid AnyStandardResult."""
    standard_result = StandardResultAdapter.validate_python({"name": name})
    assert isinstance(standard_result, AnyStandardResult)
