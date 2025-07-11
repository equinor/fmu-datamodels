from typing import Any, get_args

from pydantic import BaseModel


def _get_pydantic_models_from_annotation(annotation: Any) -> list[Any]:
    """
    Get a list of all pydantic models defined inside an annotation.
    Example: Union[Model1, list[dict[str, Model2]]] returns [Model1, Model2]
    """
    if isinstance(annotation, type(BaseModel)):
        return [annotation]

    annotations = []
    for ann in get_args(annotation):
        annotations += _get_pydantic_models_from_annotation(ann)
    return annotations


def _get_nested_pydantic_models(model: type[BaseModel]) -> set[type[BaseModel]]:
    """Get a set of all nested pydantic models from a pydantic model"""
    models = {model}

    for field_info in model.model_fields.values():
        for pydantic_model in _get_pydantic_models_from_annotation(
            field_info.annotation
        ):
            if pydantic_model not in models:
                models.update(_get_nested_pydantic_models(pydantic_model))
    return models
