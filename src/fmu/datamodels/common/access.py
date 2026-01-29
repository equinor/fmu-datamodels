from __future__ import annotations

from pydantic import (
    BaseModel,
    Field,
)

from . import enums


class Access(BaseModel):
    """
    The ``access`` block contains information related to access control for
    this data object.
    """

    asset: Asset
    """A block containing information about the owner asset of these data.
    See :class:`Asset`."""

    classification: enums.Classification | None = Field(default=None)
    """The access classification level. See :class:`enums.Classification`."""


class SsdlAccess(Access):
    """
    The ``access`` block contains information related to access control for
    this data object, with legacy SSDL settings.
    """

    ssdl: Ssdl
    """A block containing information related to SSDL. See :class:`Ssdl`."""


class Asset(BaseModel):
    """The ``access.asset`` block contains information about the owner asset of
    these data."""

    name: str = Field(examples=["Drogon"])
    """A string referring to a known asset name."""


class Ssdl(BaseModel):
    """
    The ``access.ssdl`` block contains information related to SSDL.
    Note that this is kept due to legacy.
    """

    access_level: enums.Classification
    """The SSDL access level. See :class:`Classification`."""

    rep_include: bool
    """Flag if this data is to be shown in REP or not."""
