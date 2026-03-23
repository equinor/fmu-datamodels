from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, RootModel

from . import enums


class AttributeSpecification(BaseModel):
    """Specifies a property attribute and its characteristics."""

    attribute: enums.PropertyAttribute
    """The name of the property attribute."""
    is_discrete: bool
    """Whether the property is discrete (categorical) or continuous."""
    min_value: float | None = None
    """Minimum value for the property, if applicable."""
    max_value: float | None = None
    """Maximum value for the property, if applicable."""


class BulkVolumeGasAttributeSpecification(AttributeSpecification):
    """Specifications related to the bulk volume gas attribute."""

    attribute: Literal[enums.PropertyAttribute.bulk_volume_gas]
    is_discrete: bool = False
    min_value: float = 0


class BulkVolumeOilAttributeSpecification(AttributeSpecification):
    """Specifications related to the bulk volume oil attribute."""

    attribute: Literal[enums.PropertyAttribute.bulk_volume_oil]
    is_discrete: bool = False
    min_value: float = 0


class FaciesAttributeSpecification(AttributeSpecification):
    """Specifications related to the facies attribute."""

    attribute: Literal[enums.PropertyAttribute.facies]
    is_discrete: bool = True
    min_value: float = 0


class FluidIndicatorAttributeSpecification(AttributeSpecification):
    """Specifications related to the fluid indicator attribute."""

    attribute: Literal[enums.PropertyAttribute.fluid_indicator]
    is_discrete: bool = True
    min_value: float = 0


class NetToGrossAttributeSpecification(AttributeSpecification):
    """Specifications related to the net-to-gross attribute."""

    attribute: Literal[enums.PropertyAttribute.net_to_gross]
    is_discrete: bool = True
    min_value: float = 0
    max_value: float = 1


class PermeabilityAttributeSpecification(AttributeSpecification):
    """Specifications related to the permeability attribute."""

    attribute: Literal[enums.PropertyAttribute.permeability]
    is_discrete: bool = False
    min_value: float = 0


class PermeabilityVerticalAttributeSpecification(AttributeSpecification):
    """Specifications related to the vertical permeability attribute."""

    attribute: Literal[enums.PropertyAttribute.permeability_vertical]
    is_discrete: bool = False
    min_value: float = 0


class PorosityAttributeSpecification(AttributeSpecification):
    """Specifications related to the porosity attribute."""

    attribute: Literal[enums.PropertyAttribute.porosity]
    is_discrete: bool = False
    min_value: float = 0
    max_value: float = 1


class RegionsAttributeSpecification(AttributeSpecification):
    """Specifications related to the regions attribute."""

    attribute: Literal[enums.PropertyAttribute.regions]
    is_discrete: bool = True
    min_value: float = 0


class SaturationGasAttributeSpecification(AttributeSpecification):
    """Specifications related to the gas saturation attribute."""

    attribute: Literal[enums.PropertyAttribute.saturation_gas]
    is_discrete: bool = False
    min_value: float = 0
    max_value: float = 1


class SaturationOilAttributeSpecification(AttributeSpecification):
    """Specifications related to the oil saturation attribute."""

    attribute: Literal[enums.PropertyAttribute.saturation_oil]
    is_discrete: bool = False
    min_value: float = 0
    max_value: float = 1


class SaturationWaterAttributeSpecification(AttributeSpecification):
    """Specifications related to the water saturation attribute."""

    attribute: Literal[enums.PropertyAttribute.saturation_water]
    is_discrete: bool = False
    min_value: float = 0
    max_value: float = 1


class VolumeShaleAttributeSpecification(AttributeSpecification):
    """Specifications related to the volume shale attribute."""

    attribute: Literal[enums.PropertyAttribute.volume_shale]
    is_discrete: bool = False
    min_value: float = 0
    max_value: float = 1


class ZonationAttributeSpecification(AttributeSpecification):
    """Specifications related to the zonation attribute."""

    attribute: Literal[enums.PropertyAttribute.zonation]
    is_discrete: bool = True
    min_value: float = 0


class AnyAttributeSpecification(RootModel):
    """
    Root model that allows for property attribute specifications with different
    attribute types to be placed within it. The discriminator field is ``attribute``,
    which indicates the specific property attribute being described.
    """

    root: Annotated[
        BulkVolumeGasAttributeSpecification
        | BulkVolumeOilAttributeSpecification
        | FaciesAttributeSpecification
        | FluidIndicatorAttributeSpecification
        | NetToGrossAttributeSpecification
        | PermeabilityAttributeSpecification
        | PermeabilityVerticalAttributeSpecification
        | PorosityAttributeSpecification
        | RegionsAttributeSpecification
        | SaturationGasAttributeSpecification
        | SaturationOilAttributeSpecification
        | SaturationWaterAttributeSpecification
        | VolumeShaleAttributeSpecification
        | ZonationAttributeSpecification,
        Field(discriminator="attribute"),
    ]
