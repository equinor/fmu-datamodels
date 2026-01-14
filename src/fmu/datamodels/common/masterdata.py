from __future__ import annotations

from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)


class Masterdata(BaseModel):
    """The ``masterdata`` block contains information related to masterdata.
    Currently, SMDA holds the masterdata.
    """

    smda: Smda
    """Block containing SMDA-related attributes. See :class:`Smda`."""


class Smda(BaseModel):
    """The ``masterdata.smda`` block contains SMDA-related attributes."""

    coordinate_system: CoordinateSystem
    """Reference to coordinate system known to SMDA.
    See :class:`CoordinateSystem`."""

    country: list[CountryItem]
    """A list referring to countries known to SMDA. First item is primary.
    See :class:`CountryItem`."""

    discovery: list[DiscoveryItem]
    """A list referring to discoveries known to SMDA. First item is primary.
    See :class:`DiscoveryItem`."""

    field: list[FieldItem]
    """A list referring to fields known to SMDA. First item is primary.
    See :class:`FieldItem`."""

    stratigraphic_column: StratigraphicColumn
    """Reference to stratigraphic column known to SMDA.
    See :class:`StratigraphicColumn`."""


class CountryItem(BaseModel):
    """A single country in the ``smda.masterdata.country`` list of countries
    known to SMDA."""

    identifier: str = Field(examples=["Norway"])
    """Identifier known to SMDA."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """Identifier known to SMDA."""


class DiscoveryItem(BaseModel):
    """A single discovery in the ``masterdata.smda.discovery`` list of discoveries
    known to SMDA."""

    short_identifier: str = Field(examples=["SomeDiscovery"])
    """Identifier known to SMDA."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """Identifier known to SMDA."""


class FieldItem(BaseModel):
    """A single field in the ``masterdata.smda.field`` list of fields
    known to SMDA."""

    identifier: str = Field(examples=["OseFax"])
    """Identifier known to SMDA."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """Identifier known to SMDA."""


class CoordinateSystem(BaseModel):
    """The ``masterdata.smda.coordinate_system`` block contains the coordinate
    system known to SMDA."""

    identifier: str = Field(examples=["ST_WGS84_UTM37N_P32637"])
    """Identifier known to SMDA."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """Identifier known to SMDA."""


class StratigraphicColumn(BaseModel):
    """The ``masterdata.smda.stratigraphic_column`` block contains the
    stratigraphic column known to SMDA."""

    identifier: str = Field(examples=["DROGON_2020"])
    """Identifier known to SMDA."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """Identifier known to SMDA."""
