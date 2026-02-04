from __future__ import annotations

from enum import StrEnum


class StandardResultName(StrEnum):
    """The standard result name of a given data object."""

    parameters = "parameters"
    field_outline = "field_outline"
    inplace_volumes = "inplace_volumes"
    structure_depth_surface = "structure_depth_surface"
    structure_time_surface = "structure_time_surface"
    structure_depth_isochore = "structure_depth_isochore"
    structure_depth_fault_lines = "structure_depth_fault_lines"
    structure_depth_fault_surface = "structure_depth_fault_surface"
    fluid_contact_surface = "fluid_contact_surface"
    fluid_contact_outline = "fluid_contact_outline"


class InplaceVolumes:
    """Enumerations relevant to inplace volumes tables."""

    class Fluid(StrEnum):
        """Fluid types used as values in the FLUID column."""

        oil = "oil"
        gas = "gas"
        water = "water"

    class TableIndexColumns(StrEnum):
        """The index columns for an inplace volumes table."""

        FLUID = "FLUID"
        ZONE = "ZONE"
        REGION = "REGION"
        FACIES = "FACIES"
        LICENSE = "LICENSE"

    class VolumetricColumns(StrEnum):
        """The value columns for an inplace volumes table."""

        BULK = "BULK"
        NET = "NET"
        PORV = "PORV"
        HCPV = "HCPV"
        STOIIP = "STOIIP"
        GIIP = "GIIP"
        ASSOCIATEDGAS = "ASSOCIATEDGAS"
        ASSOCIATEDOIL = "ASSOCIATEDOIL"

    @staticmethod
    def index_columns() -> list[str]:
        """Returns a list of the index columns."""
        return [k.value for k in InplaceVolumes.TableIndexColumns]

    @staticmethod
    def required_index_columns() -> list[str]:
        return [
            InplaceVolumes.TableIndexColumns.FLUID.value,
            InplaceVolumes.TableIndexColumns.ZONE.value,
            InplaceVolumes.TableIndexColumns.REGION.value,
        ]

    @staticmethod
    def value_columns() -> list[str]:
        """Returns a list of the value columns."""
        return [k.value for k in InplaceVolumes.VolumetricColumns]

    @staticmethod
    def required_value_columns() -> list[str]:
        """Returns a list of the value columns."""
        return [
            InplaceVolumes.VolumetricColumns.BULK.value,
            InplaceVolumes.VolumetricColumns.NET.value,
            InplaceVolumes.VolumetricColumns.PORV.value,
            InplaceVolumes.VolumetricColumns.HCPV.value,
        ]

    @staticmethod
    def required_columns() -> list[str]:
        """Returns a list of the columns required at export."""
        return (
            InplaceVolumes.required_index_columns()
            + InplaceVolumes.required_value_columns()
        )

    @staticmethod
    def table_columns() -> list[str]:
        """Returns a list of all table columns."""
        return InplaceVolumes.index_columns() + InplaceVolumes.value_columns()


class FaultLines:
    """Enumerations relevant to fault lines tables."""

    class TableIndexColumns(StrEnum):
        """The index columns for a fault lines table."""

        POLY_ID = "POLY_ID"
        NAME = "NAME"

    @staticmethod
    def index_columns() -> list[str]:
        """Returns a list of the index columns."""
        return [k.value for k in FaultLines.TableIndexColumns]
