from typing import Any

import pytest
from pydantic import BaseModel

from fmu.datamodels.standard_results.ert_observations_breakthrough import (
    ErtObservationsBreakthroughResultRow,
)
from fmu.datamodels.standard_results.ert_observations_rft import (
    ErtObservationsRftResultRow,
)
from fmu.datamodels.standard_results.ert_observations_seismic import (
    ErtObservationsSeismicResultRow,
)
from fmu.datamodels.standard_results.ert_observations_summary import (
    ErtObservationsSummaryResultRow,
)
from fmu.datamodels.standard_results.ert_responses_rft import ErtResponsesRftResultRow
from fmu.datamodels.standard_results.ert_responses_summary import (
    ErtResponsesSummaryResultRow,
)


@pytest.mark.parametrize(
    ("row_model", "row"),
    [
        (
            ErtObservationsBreakthroughResultRow,
            {
                "response_key": "WOPR:OP_1",
                "time": "2026-01-01T00:00:00",
                "observation_value": 1.0,
                "observation_error": 0.1,
                "threshold": 0.5,
            },
        ),
        (
            ErtObservationsRftResultRow,
            {
                "response_key": "PRESSURE:OP_1",
                "property": "PRESSURE",
                "well": "OP_1",
                "date": "2026-01-01",
                "observation_value": 1.0,
                "observation_error": 0.1,
                "east": 10.0,
                "north": 20.0,
                "tvd": 30.0,
            },
        ),
        (
            ErtObservationsSeismicResultRow,
            {
                "response_key": "SEISMIC:1",
                "observation_value": 1.0,
                "observation_error": 0.1,
                "east": 10.0,
                "north": 20.0,
            },
        ),
        (
            ErtObservationsSummaryResultRow,
            {
                "response_key": "WOPR:OP_1",
                "time": "2026-01-01T00:00:00",
                "observation_value": 1.0,
                "observation_error": 0.1,
            },
        ),
        (
            ErtResponsesRftResultRow,
            {
                "realization": 1,
                "response_key": "PRESSURE:OP_1",
                "well": "OP_1",
                "date": "2026-01-01",
                "property": "PRESSURE",
                "response_value": 1.0,
                "well_connection_cell": [1, 2, 3],
            },
        ),
        (
            ErtResponsesSummaryResultRow,
            {
                "realization": 1,
                "response_key": "WOPR:OP_1",
                "time": "2026-01-01T00:00:00",
                "response_value": 1.0,
            },
        ),
    ],
)
def test_optional_id_on_observation_and_response_rows(
    row_model: type[BaseModel], row: dict[str, Any]
) -> None:
    assert row_model.model_validate(row).model_dump()["observation_id"] is None
    result = row_model.model_validate({**row, "observation_id": 42}).model_dump()
    assert result["observation_id"] == 42
    assert "id" not in result
