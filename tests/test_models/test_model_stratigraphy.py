from fmu.settings.models.project_config import RmsHorizon, RmsStratigraphicZone

from fmu.datamodels.standard_results.model_stratigraphy_horizons import (
    ModelStratigraphyHorizonsResultRow,
)
from fmu.datamodels.standard_results.model_stratigraphy_zones import (
    ModelStratigraphyZonesResultRow,
)


def test_horizon_attributes_match_fmu_settings() -> None:
    settings_fields = {*RmsHorizon.model_fields, "stratigraphic_order"}

    assert ModelStratigraphyHorizonsResultRow.model_fields.keys() == settings_fields


def test_zone_attributes_match_fmu_settings() -> None:
    settings_fields = {
        "stratigraphic_column_names" if name == "stratigraphic_column_name" else name
        for name in RmsStratigraphicZone.model_fields
    }

    assert ModelStratigraphyZonesResultRow.model_fields.keys() == settings_fields
