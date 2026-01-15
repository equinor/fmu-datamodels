import pyarrow as pa
import pytest

from fmu.datamodels.parameters.distributions import (
    ConstDistribution,
    DerrfDistribution,
    DistributionMetadata,
    DUnifDistribution,
    ErrfDistribution,
    LogNormalDistribution,
    LogUnifDistribution,
    NormalDistribution,
    RawDistribution,
    TriangularDistribution,
    TruncatedNormalDistribution,
    UniformDistribution,
)


def test_to_pa_metadata_serialization() -> None:
    """Dumping Parquet schemas serializes to dict[bytes, bytes].

    Uses DUnif because it has both float and int."""
    dist = DUnifDistribution(
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
    "distribution_class, value_dict",
    [
        (UniformDistribution, {"min": 0.0, "max": 1.0}),
        (LogUnifDistribution, {"min": 0.0, "max": 1.0}),
        (NormalDistribution, {"mean": 0.2, "std": 0.1}),
        (
            TruncatedNormalDistribution,
            {"min": 0.0, "max": 1.0, "mean": 0.2, "std": 0.1},
        ),
        (LogNormalDistribution, {"mean": 0.2, "std": 0.1}),
        (RawDistribution, {}),
        (ConstDistribution, {"value": 2.0}),
        (TriangularDistribution, {"min": 0.0, "max": 3.0, "mode": 2.0}),
        (ErrfDistribution, {"min": 0.0, "max": 3.0, "skewness": 2.0, "width": 10.0}),
        (
            DerrfDistribution,
            {"min": 0.0, "max": 3.0, "skewness": 2.0, "width": 10.0, "steps": 1000.0},
        ),
        (DUnifDistribution, {"min": 0.0, "max": 1.0, "steps": 100}),
    ],
)
def test_from_pa_metadata_roundtrip(
    distribution_class: DistributionMetadata, value_dict: dict[str, int | float]
) -> None:
    """Roundtrip serialization-deserialization works for all distributions."""
    input_source = (
        "design_matrix" if type(distribution_class) is RawDistribution else "sampled"
    )
    dist = distribution_class.model_validate(
        {"group": "GLOBVAR", "input_source": input_source, **value_dict}
    )
    field = pa.field("PARAM1", pa.float64(), metadata=dist.to_pa_metadata())
    assert field.metadata is not None
    from_dist = distribution_class.from_pa_metadata(field.metadata)
    assert dist == from_dist
