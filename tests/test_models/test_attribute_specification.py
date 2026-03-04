from typing import Literal, get_args, get_origin

from fmu.datamodels.fmu_results import data, enums
from tests.utils import _get_pydantic_models_from_annotation


def test_all_attribute_enums_in_anyattributespecification() -> None:
    """
    Test that all attribute enums are represented with a model
    in AnyAttributeSpecification.
    """

    models = _get_pydantic_models_from_annotation(
        data.AnyAttributeSpecification.model_fields["root"].annotation
    )

    enums_in_anyattributespecification = []
    for model in models:
        # attribute is used as a discriminator in AnyAttributeSpecification and
        # should be present for all models
        assert "attribute" in model.model_fields
        attribute_annotation = model.model_fields["attribute"].annotation

        # check that the annotation is a Literal
        assert get_origin(attribute_annotation) == Literal

        # get_args will unpack the enum from the Literal
        # into a tuple, should only be one Literal value
        assert len(get_args(attribute_annotation)) == 1

        # the literal value should be an enum
        attribute_enum = get_args(attribute_annotation)[0]
        assert isinstance(attribute_enum, enums.PropertyAttribute)

        enums_in_anyattributespecification.append(attribute_enum)

    # finally check that all attribute enums are represented
    for attribute_enum in enums.PropertyAttribute:
        assert attribute_enum in enums_in_anyattributespecification

    # and that number of models in AnyAttributeSpecification matches
    # number of attribute enums
    assert len(models) == len(enums.PropertyAttribute)
