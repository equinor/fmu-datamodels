import pyarrow as pa
import pytest

from fmu.datamodels.parameters import (
    ConstParameter,
    DerrfParameter,
    DUnifParameter,
    ErrfParameter,
    LogNormalParameter,
    LogUnifParameter,
    NormalParameter,
    ParameterMetadata,
    RawParameter,
    TriangularParameter,
    TruncatedNormalParameter,
    UniformParameter,
)


def test_to_pa_metadata_serialization() -> None:
    """Dumping Parquet schemas serializes to dict[bytes, bytes].

    Uses DUnif because it has both float and int."""
    dist = DUnifParameter(
        min=0.0, max=1.0, steps=100, group="GLOBVAR", input_source="sampled"
    )
    assert dist.to_pa_metadata() == {
        b"group": b'"GLOBVAR"',
        b"input_source": b'"sampled"',
        b"distribution": b'"dunif"',
        b"min": b"0.0",
        b"max": b"1.0",
        b"steps": b"100",
    }

    field = pa.field("PARAM1", pa.float64(), metadata=dist.to_pa_metadata())
    assert field.metadata == {
        b"group": b'"GLOBVAR"',
        b"input_source": b'"sampled"',
        b"distribution": b'"dunif"',
        b"min": b"0.0",
        b"max": b"1.0",
        b"steps": b"100",
    }


@pytest.mark.parametrize(
    "parameter_class, value_dict",
    [
        (UniformParameter, {"min": 0.0, "max": 1.0}),
        (LogUnifParameter, {"min": 0.0, "max": 1.0}),
        (NormalParameter, {"mean": 0.2, "std": 0.1}),
        (
            TruncatedNormalParameter,
            {"min": 0.0, "max": 1.0, "mean": 0.2, "std": 0.1},
        ),
        (LogNormalParameter, {"mean": 0.2, "std": 0.1}),
        (RawParameter, {}),
        (ConstParameter, {"value": 2.0}),
        (TriangularParameter, {"min": 0.0, "max": 3.0, "mode": 2.0}),
        (ErrfParameter, {"min": 0.0, "max": 3.0, "skewness": 2.0, "width": 10.0}),
        (
            DerrfParameter,
            {"min": 0.0, "max": 3.0, "skewness": 2.0, "width": 10.0, "steps": 1000.0},
        ),
        (DUnifParameter, {"min": 0.0, "max": 1.0, "steps": 100}),
    ],
)
def test_from_pa_metadata_roundtrip(
    parameter_class: ParameterMetadata, value_dict: dict[str, int | float]
) -> None:
    """Roundtrip serialization-deserialization works for all parameters."""
    input_source = (
        "design_matrix" if type(parameter_class) is RawParameter else "sampled"
    )
    dist = parameter_class.model_validate(
        {"group": "GLOBVAR", "input_source": input_source, **value_dict}
    )
    field = pa.field("PARAM1", pa.float64(), metadata=dist.to_pa_metadata())
    assert field.metadata is not None
    from_dist = parameter_class.from_pa_metadata(field.metadata)
    assert dist == from_dist
