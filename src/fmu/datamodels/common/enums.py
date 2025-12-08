from __future__ import annotations

from enum import StrEnum


class Classification(StrEnum):
    """The security classification for a given data object."""

    asset = "asset"
    # Deprecated. This value should be undocumented and eventually removed.

    internal = "internal"
    """Grants access to all users with ``READ`` access to the asset.

    The ``READ`` role is an access role defined by the asset's Unix and Sumo groups.
    This is the default for most data.
    """

    restricted = "restricted"
    """Grants access to all users with ``WRITE`` access to the asset.

    The ``WRITE`` role is an access role defined by the asset's Unix and Sumo groups.
    This is the default for some sensitive data, like volumes, but in general must be
    explicitly set when restricted access is desired.
    """


class TrackLogEventType(StrEnum):
    """The type of event being logged"""

    created = "created"
    """The initial data was created."""

    updated = "updated"
    """Data was updated."""

    merged = "merged"
    """Data was merged."""
