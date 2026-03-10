from __future__ import annotations

import datetime
import getpass
import os
import platform
from typing import (
    Any,
)

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    RootModel,
)

from . import enums


class User(BaseModel):
    """The ``user`` block holds information about the user."""

    id: str = Field(examples=["peesv", "jriv"])
    """A user identity reference."""


class Version(BaseModel):
    """
    A generic block that contains a string representing the version of
    something.
    """

    version: str
    """A string representing the version."""


class Tracklog(RootModel):
    """The ``tracklog`` block contains a record of events recorded on these data.
    This data object describes the list of tracklog events, in addition to functionality
    for constructing a tracklog and adding new records to it.
    """

    root: list[TracklogEvent]

    def __getitem__(self, item: int) -> TracklogEvent:
        return self.root[item]

    def __iter__(
        self,
    ) -> Any:
        # Using ´Any´ as return type here as mypy is having issues
        # resolving the correct type
        return iter(self.root)

    @classmethod
    def initialize(cls, fmu_dataio_version: str) -> Tracklog:
        """Initialize the tracklog object with a list containing one
        TracklogEvent of type 'created'"""

        return cls(
            root=[
                cls._generate_tracklog_event(
                    enums.TrackLogEventType.created, fmu_dataio_version
                )
            ]
        )

    def append(
        self,
        event: enums.TrackLogEventType,
        fmu_dataio_version: str,
        source_name: str | None = None,
        source_version: str | None = None,
    ) -> None:
        """Append new tracklog record to the tracklog."""
        self.root.append(
            self._generate_tracklog_event(
                event, fmu_dataio_version, source_name, source_version
            )
        )

    @staticmethod
    def _generate_tracklog_event(
        event: enums.TrackLogEventType,
        version: str,
        source_name: str | None = None,
        source_version: str | None = None,
    ) -> TracklogEvent:
        """Generate new tracklog event with the given event type"""
        source: TracklogSource | None = None

        if source_name is not None and source_version is not None:
            source = TracklogSource(
                name=source_name, version=Version(version=source_version)
            )
        elif source_name is not None or source_version is not None:
            raise ValueError(
                "Both the source name and source version must be provided together."
            )

        komodo_release = os.environ.get(
            "KOMODO_RELEASE", os.environ.get("KOMODO_RELEASE_BACKUP", None)
        )
        komodo = Version(version=komodo_release) if komodo_release else None

        sysinfo = SystemInformation.model_construct(
            fmu_dataio=Version(version=version),
            source=source,
            komodo=komodo,
            operating_system=OperatingSystem(
                hostname=platform.node(),
                operating_system=platform.platform(),
                release=platform.release(),
                system=platform.system(),
                version=platform.version(),
            ),
        )

        return TracklogEvent.model_construct(
            datetime=datetime.datetime.now(datetime.UTC),
            event=event,
            user=User(id=getpass.getuser()),
            sysinfo=sysinfo,
        )


class OperatingSystem(BaseModel):
    """
    The ``operating_system`` block contains information about the OS on which the
    ensemble was run.
    """

    hostname: str = Field(examples=["st-123.equinor.com"])
    """A string containing the network name of the machine."""

    operating_system: str = Field(examples=["Darwin-18.7.0-x86_64-i386-64bit"])
    """A string containing the name of the operating system implementation."""

    release: str = Field(examples=["18.7.0"])
    """A string containing the level of the operating system."""

    system: str = Field(examples=["GNU/Linux"])
    """A string containing the name of the operating system kernel."""

    version: str = Field(examples=["#1 SMP Tue Aug 27 21:37:59 PDT 2019"])
    """The specific release version of the system."""


class TracklogSource(BaseModel):
    """The package or service causing an event that's added to the tracklog.

    This is only relevant for a non-fmu-dataio source."""

    name: str
    """The name of the source package or service."""

    version: Version
    """The version of the source package or service."""


# TODO: Make `fmu_dataio` and `operating_system` non-optional
#  when fmu-sumo-aggregation-service uses only fmu-dataio
class SystemInformation(BaseModel):
    """
    The ``tracklog.sysinfo`` block contains information about the system upon which
    these data were exported from.
    """

    fmu_dataio: Version | None = Field(
        alias="fmu-dataio",
        default=None,
        examples=["1.2.3"],
    )
    """The version of fmu-dataio used to export the data. See :class:`Version`."""

    source: TracklogSource | None = None
    """The package or service that is the source of the tracklog entry.

    This field should not be used when fmu-dataio is the source itself."""

    komodo: Version | None = Field(
        default=None,
        examples=["2023.12.05-py38"],
    )
    """The version of Komodo in which the the ensemble was run from."""

    operating_system: OperatingSystem | None = Field(default=None)
    """The operating system from which the ensemble was started from.
    See :class:`OperatingSystem`."""


class TracklogEvent(BaseModel):
    """The ``tracklog`` block contains a record of events recorded on these data.
    This data object describes a tracklog event.
    """

    datetime: AwareDatetime = Field(examples=["2020-10-28T14:28:024286Z"])
    """A datetime representation recording when the event occurred."""

    event: enums.TrackLogEventType
    """The type of event being logged.
    See :class:`datamodels.common.enums.TrackLogEventType`.
    """

    user: User
    """The user who caused the event to happen. See :class:`User`."""

    # TODO: Make non-optional when fmu-sumo-aggregation-service uses only fmu-dataio
    sysinfo: SystemInformation | None = Field(
        default_factory=SystemInformation,
    )
    """Information about the system on which the event occurred.
    See :class:`SystemInformation`."""
