from __future__ import annotations

from enum import IntEnum, StrEnum


class AxisOrientation(IntEnum):
    """The axis orientation for a given data object."""

    normal = 1
    """A coordinate system with Z-axis positive downwards."""

    flipped = -1
    """A coordinate system with Z-axis positive upwards."""


class Content(StrEnum):
    """The content type of a given data object."""

    depth = "depth"
    """A data object representing depth values.

    Typically provided as an ``xtgeo.RegularSurface`` or ``xtgeo.Grid`` for export.
    """

    facies_thickness = "facies_thickness"
    """Thickness map representing facies thickness, derived from a 3D grid.

    Typically provided as an ``xtgeo.RegularSurface`` for export.
    """

    fault_lines = "fault_lines"
    """Intersections between fault planes and horizons.

    Typically provided as an ``xtgeo.Polygons`` for export.
    """

    fault_surface = "fault_surface"
    """A surface representing a fault plane.

    Typically provided either as an RMS FaultRoom GeoJSON surface or an fmu-dataio
    ``TSurfData`` for export.
    """

    fault_properties = "fault_properties"
    """Properties, such as permeability and porosity, on a fault.

    Typically provided as a GeoJSON file derived from RMS FaultRoom for export.
    """

    field_outline = "field_outline"
    """Polygons representing the outline of a field, initial (static) conditions.

    Typically provided as an ``xtgeo.Polygons`` for export.
    """

    field_region = "field_region"
    """Delineated or named region within a field.

    Typically provided as an ``xtgeo.Polygons`` for export.
    """

    fluid_contact = "fluid_contact"
    """Depth surface representing a fluid contact used per realization.

    Typically provided as an ``xtgeo.RegularSurface`` for export.
    """

    khproduct = "khproduct"
    """The product of permeability (k) and reservoir thickness (h).

    Typically provided as an ``xtgeo.RegularSurface`` for export.
    """

    lift_curves = "lift_curves"
    """Table representing the relationship between production rates and pressures.

    Typically provided as a Pandas ``Dataframe`` for export.
    """
    mapping = "mapping"
    """Tabular cross-references used to translate between different naming conventions
    or identifiers.

    Acts as a bridge to align data across different domains, such as:
    * Official stratigraphy to model zonation.
    * Static reservoir regions/zones to simulator-specific identifiers (e.g., FIPGRP).
    * Unique Well Identifiers (UWI) to simulation well names.

    Typically provided as a Pandas ``Dataframe`` for export.
    """

    named_area = "named_area"
    """A named area within a field that is _not_ a region.

    Typically provided as an ``xtgeo.Polygons`` for export.
    """

    parameters = "parameters"
    """The ERT parameters generated for the realization.

    Typically provided as a Pandas ``Dataframe`` for export.

    .. tip::

       You should not export this manually. This is done automatically by `SUMO_UPLOADER
       <https://fmu-sumo-uploader.readthedocs.io/en/latest/>`_ when uploading files.

    """

    production_network = "production_network"
    """Tabular data representing the production group structure.

    Typically provided as a Pandas ``Dataframe``.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.
    """

    pinchout = "pinchout"
    """Polygons designating a pinchout.

    Typically provided as an ``xtgeo.Polygons`` for export.
    """

    property = "property"
    """A property, like permeability or porosity, belonging to a 3D grid.

    Typically provided as an ``xtgeo.GridProperty``.

    .. tip::

       This content type requires additional input in the ``content_metadata`` field.

       Grid property data handling is still immature. More comprehensive data
       categorization will come in the future.

    """

    pvt = "pvt"
    """Tabular pressure-volume-temperature data.

    Typically provided as a Pandas ``Dataframe`` for export.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    regions = "regions"
    """Distinct areas within the field that have different characteristics.

    Examples may be volume regions or contact regions.

    Typically provided as an ``xtgeo.Polygons`` or ``xtgeo.GridProperty``.
    """

    relperm = "relperm"
    """Tabular relative permeability data.

    Typically provided as a Pandas ``Dataframe`` for export.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    rft = "rft"
    """Tabular reservoir formation tests data.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    seismic = "seismic"
    """Data that is seismic in nature, including seismic cubes and surface data derived
    from seismic cubes.

    Typically provided as an ``xtgeo.Cube``, ``xtgeo.RegularSurface``, or other.

    .. tip::

       This content type requires additional input in the ``content_metadata`` field.

       Seismic data handling is still immature. More comprehensive data categorization
       will come in the future.

    """

    simulationtimeseries = "simulationtimeseries"
    """Time-series data generated by a reservoir simulator like OPM Flow or Eclipse.

    For example, a summary file parsed into a Pandas ``Dataframe`` by
    `res2df <https://equinor.github.io/res2df>`_.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    subcrop = "subcrop"
    """Surface or polygon representing a subcrop area.

    Typically provided as an ``xtgeo.RegularSurface`` or ``xtgeo.Polygons`` for export.
    """

    thickness = "thickness"
    """A thickness map.

    Typically provided as an ``xtgeo.RegularSurface`` for export.
    """

    time = "time"
    """A seismic time surface or seismic cube in time domain.

    Typically provided as an ``xtgeo.RegularSurface`` or ``xtgeo.Cube``.
    """

    timeseries = "timeseries"
    # Deprecated. Use "simlationtimeseries" ?

    transmissibilities = "transmissibilities"
    """Tabular data containing transmissibilities (neighbour and
    non-neigbor-connections).

    Typically provided as a Pandas ``Dataframe``.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    velocity = "velocity"
    """A seismic velocity map represented as a regular surface or a cube.

    Typically provided as an ``xtgeo.RegularSurface`` or ``xtgeo.Cube`` for export.
    """

    volumes = "volumes"
    """Tabulated inplace volumes per grid, initial (static) conditions.

    Typically provided as a Pandas ``Dataframe``.
    """

    well_completions = "well_completions"
    """Tabular data representing well completions.

    Typically provided as a Pandas ``Dataframe``.

    .. tip::

       You should not export this manually. Use `SIM2SUMO
       <https://fmu-sumo-sim2sumo.readthedocs.io/en/latest/>`_.

    """

    wellpicks = "wellpicks"
    """Tabular data representing wellpicks.

    Typically provided as a Pandas ``Dataframe``.
    """

    @classmethod
    def _missing_(cls: type[Content], value: object) -> None:
        raise ValueError(
            f"Invalid 'content' {value=}. Valid entries are {[m.value for m in cls]}"
        )


class ErtSimulationMode(StrEnum):
    """The simulation mode ert was run in. These definitions come from
    `ert.mode_definitions`."""

    ensemble_experiment = "ensemble_experiment"
    ensemble_information_filter = "ensemble_information_filter"
    ensemble_smoother = "ensemble_smoother"
    es_mda = "es_mda"
    evaluate_ensemble = "evaluate_ensemble"
    manual_enif_update = "manual_enif_update"
    manual_update = "manual_update"
    test_run = "test_run"
    workflow = "workflow"


class MetadataClass(StrEnum):
    """Base class for objects by FMU convention or standards."""


class ObjectMetadataClass(MetadataClass):
    """The class of a data object (typically originating from an RMS model)."""

    surface = "surface"
    table = "table"
    cpgrid = "cpgrid"
    cpgrid_property = "cpgrid_property"
    polygons = "polygons"
    cube = "cube"
    well = "well"
    points = "points"
    dictionary = "dictionary"


class FMUResultsMetadataClass(MetadataClass):
    """The class of an FMU results object."""

    case = "case"
    realization = "realization"
    iteration = "iteration"
    ensemble = "ensemble"


class Layout(StrEnum):
    """The layout of a given data object."""

    regular = "regular"
    unset = "unset"
    cornerpoint = "cornerpoint"
    table = "table"
    dictionary = "dictionary"
    triangulated = "triangulated"


class FMUContext(StrEnum):
    """The context in which FMU was being run when data were generated."""

    case = "case"
    iteration = "iteration"
    ensemble = "ensemble"
    realization = "realization"


class VerticalDomain(StrEnum):
    depth = "depth"
    """In the domain of depth."""

    time = "time"
    """In the domain of time."""


class DomainReference(StrEnum):
    msl = "msl"
    """In reference to Mean Sea Level."""

    sb = "sb"
    """In reference to Sea Bottom."""

    rkb = "rkb"
    """In reference to Rotary Kelly Bushing (RKB)."""


class FluidContactType(StrEnum):
    """The type of fluid contact."""

    fgl = "fgl"
    """Free gas level."""

    fwl = "fwl"
    """Free water level."""

    goc = "goc"
    """Gas-oil contact."""

    gwc = "gwc"
    """Gas-water contact."""

    owc = "owc"
    """Oil-water contact."""


class FileFormat(StrEnum):
    """The format of a given data object."""

    parquet = "parquet"
    json = "json"
    csv = "csv"
    csv_xtgeo = "csv|xtgeo"
    irap_ascii = "irap_ascii"
    irap_binary = "irap_binary"
    roff = "roff"
    segy = "segy"
    openvds = "openvds"
    tsurf = "tsurf"
