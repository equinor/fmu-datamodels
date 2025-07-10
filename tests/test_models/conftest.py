import datetime
from uuid import UUID

import pytest
from pydantic import BaseModel

from fmu.datamodels.fmu_results import enums
from fmu.datamodels.fmu_results.data import (
    AnyData,
    BoundingBox2D,
    BoundingBox3D,
    FieldOutline,
    FieldRegion,
    FluidContact,
    Layer,
    Seismic,
    Time,
    Timestamp,
)
from fmu.datamodels.fmu_results.fields import (
    FMU,
    Access,
    Asset,
    Case,
    Context,
    CoordinateSystem,
    CountryItem,
    DiscoveryItem,
    Display,
    FieldItem,
    File,
    FMUBase,
    Masterdata,
    Model,
    OperatingSystem,
    Smda,
    Ssdl,
    SsdlAccess,
    StratigraphicColumn,
    SystemInformation,
    Tracklog,
    TracklogEvent,
    User,
    Version,
)
from fmu.datamodels.fmu_results.fmu_results import (
    CaseMetadata,
    FmuResults,
    FmuResultsSchema,
    ObjectMetadata,
)
from fmu.datamodels.fmu_results.global_configuration import (
    Stratigraphy,
    StratigraphyElement,
)
from fmu.datamodels.fmu_results.specification import (
    PolygonsSpecification,
    SurfaceSpecification,
    TableSpecification,
)
from fmu.datamodels.types import MD5HashStr
from tests.test_utils import _get_nested_pydantic_models


@pytest.fixture(scope="session")
def pydantic_models_from_root() -> set[type[BaseModel]]:
    """Return all nested pydantic models from FmuResults and downwards"""
    return _get_nested_pydantic_models(FmuResults)


@pytest.fixture(name="testdata_stratigraphy", scope="function")
def fixture_testdata_stratigraphy() -> Stratigraphy:
    """
    Return a dict of StratigraphyElement instances.
    """
    return Stratigraphy(
        root={
            "TopStratUnit1": StratigraphyElement(
                name="Stratigraphic Unit 1",
                stratigraphic=True,
                alias=["TopSU1", "TopLayer1"],
            ),
            "TopStratUnit2": StratigraphyElement(
                name="Stratigraphic Unit 2",
                stratigraphic=True,
                alias=["TopSU2", "TopLayer2"],
            ),
            "TopStratUnit3": StratigraphyElement(
                name="Stratigraphic Unit 3",
                stratigraphic=True,
                alias=["TopSU3", "TopLayer3"],
            ),
        }
    )


def _generate_metadata_base() -> dict:
    """Generates an example of the metadata base in FMU results"""

    masterdata = Masterdata.model_construct(
        smda=Smda.model_construct(
            coordinate_system=CoordinateSystem.model_construct(
                identifier="ST_WGS84_UTM37N_P32637",
                uuid=UUID("00000000-0000-0000-0000-000000000000"),
            ),
            country=[
                CountryItem.model_construct(
                    identifier="SomeDiscovery",
                    uuid=UUID("00000000-0000-0000-0000-000000000000"),
                )
            ],
            discovery=[
                DiscoveryItem.model_construct(
                    short_identifier="Norway",
                    uuid=UUID("00000000-0000-0000-0000-000000000000"),
                )
            ],
            field=[
                FieldItem.model_construct(
                    identifier="OseFax",
                    uuid=UUID("00000000-0000-0000-0000-000000000000"),
                )
            ],
            stratigraphic_column=StratigraphicColumn.model_construct(
                identifier="DROGON_2020",
                uuid=UUID("00000000-0000-0000-0000-000000000000"),
            ),
        )
    )

    tracklog = Tracklog.model_construct(
        [
            TracklogEvent.model_construct(
                datetime=datetime.datetime.now(datetime.UTC),
                event=enums.TrackLogEventType.created,
                user=User(id="user"),
                sysinfo=SystemInformation.model_construct(
                    fmu_dataio=Version.model_construct(version="dummy_version"),
                    komodo=Version.model_construct(version="dummy_version"),
                    operating_system=OperatingSystem(
                        hostname="dummy_hostname",
                        operating_system="dummy_os",
                        release="dummy_release",
                        system="dummy_system",
                        version="dummy_version",
                    ),
                ),
            )
        ]
    )

    return {
        "masterdata": masterdata,
        "tracklog": tracklog,
        "source": "fmu",
        "version": FmuResultsSchema.VERSION,
        "schema": "https://schema_url.com",
    }


def _generate_fmu_base() -> FMUBase:
    """Generates an example of the FMU base in FMU results"""

    return FMUBase.model_construct(
        case=Case.model_construct(
            name="MyCaseName",
            user=User(id="user"),
            uuid=UUID("00000000-0000-0000-0000-000000000000"),
            description=None,
        ),
        model=Model.model_construct(
            description=None, name="Drogon", revision="21.0.0.dev"
        ),
    )


def _generate_object_metadata_base() -> dict:
    """Generate a base for the ObjectMetadata object, without the 'data' field set"""

    metadata_base = _generate_metadata_base()
    fmu_base = _generate_fmu_base()

    fmu = FMU.model_construct(
        case=fmu_base.case,
        model=fmu_base.model,
        fmu_base=fmu_base,
        context=Context(stage=enums.FMUContext.realization),
        ensemble=None,
        iteration=None,
        workflow=None,
        aggregation=None,
        realization=None,
        entity=None,
        ert=None,
    )

    access = SsdlAccess.model_construct(
        asset=Asset(name="test"),
        ssdl=Ssdl.model_construct(
            access_level=enums.Classification.internal, rep_include=False
        ),
    )

    file = File.model_construct(
        absolute_path="/some/absolute/path/",
        relative_path="realization-0/iter-0/share/results/maps/some_file_name",
        runpath_relative_path=None,
        checksum_md5=MD5HashStr("ab0fb42049138871749c6c367d2d094f"),
        size_bytes=None,
    )

    object_metadata_dict = {
        "fmu": fmu,
        "access": access,
        "file": file,
        "display": Display(name="VIKING GP. Top"),
    }

    object_metadata_dict.update(metadata_base)
    return object_metadata_dict


@pytest.fixture(scope="function")
def case_metadata() -> dict:
    """Generate an example of valid case metadata"""

    metadata_base = _generate_metadata_base()
    fmu_base = _generate_fmu_base()

    access = Access.model_construct(
        asset=Asset(name="test"), classification=enums.Classification.internal
    )

    case_metadata_dict = {
        "class": enums.FMUResultsMetadataClass.case,
        "fmu": fmu_base,
        "access": access,
    }

    case_metadata_dict.update(metadata_base)
    return CaseMetadata.model_validate(case_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )


@pytest.fixture(scope="function")
def fluid_contact_metadata() -> dict:
    """Generate an example of valid fluid contact metadata"""

    object_metadata_dict = _generate_object_metadata_base()

    data = AnyData.model_validate(
        {
            "content": enums.Content.fluid_contact,
            "standard_result": None,
            "name": "VIKING GP. Top",
            "alias": None,
            "tagname": None,
            "stratigraphic": False,
            "description": None,
            "geometry": None,
            "bbox": BoundingBox3D(
                xmin=456063.6875,
                xmax=467483.6875,
                ymin=5926551.0,
                ymax=5939431.0,
                zmax=1933.5001220703125,
                zmin=1554.5228271484375,
            ),
            "format": enums.FileFormat.irap_binary,
            "grid_model": None,
            "is_observation": False,
            "is_prediction": False,
            "layout": None,
            "offset": 0.6,
            "spec": SurfaceSpecification(
                nrow=5,
                ncol=5,
                rotation=0.1,
                undef=0.0,
                xinc=0.1,
                yinc=0.1,
                xori=0.1,
                yflip=enums.AxisOrientation.normal,
                yori=0.1,
            ),
            "time": None,
            "undef_is_zero": None,
            "unit": "m",
            "vertical_domain": "depth",
            "domain_reference": None,
            "table_index": None,
            "base": None,
            "top": None,
            "fluid_contact": FluidContact(
                contact=enums.FluidContactType.goc,
                truncated=False,
            ),
        }
    )

    object_metadata_dict["class"] = enums.ObjectMetadataClass.surface
    object_metadata_dict["data"] = data

    return ObjectMetadata.model_validate(object_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )


@pytest.fixture(scope="function")
def field_outline_metadata() -> dict:
    """Generate an example of valid field outline metadata"""

    object_metadata_dict = _generate_object_metadata_base()

    data = AnyData.model_validate(
        {
            "content": enums.Content.field_outline,
            "standard_result": None,
            "name": "VOLANTIS GP. Base",
            "alias": None,
            "tagname": None,
            "stratigraphic": False,
            "description": None,
            "geometry": None,
            "bbox": None,
            "format": enums.FileFormat.csv_xtgeo,
            "grid_model": None,
            "is_observation": False,
            "is_prediction": False,
            "layout": None,
            "offset": 0.6,
            "spec": PolygonsSpecification(
                npolys=2,
                columns=["X_UTME", "Y_UTMN", "Z_TVDSS", "POLY_ID"],
                num_columns=4,
                num_rows=200,
                size=800,
            ),
            "time": None,
            "undef_is_zero": None,
            "unit": "m",
            "vertical_domain": "depth",
            "domain_reference": None,
            "table_index": None,
            "base": None,
            "top": None,
            "field_outline": FieldOutline(
                contact="goc",
            ),
        }
    )

    object_metadata_dict["class"] = enums.ObjectMetadataClass.polygons
    object_metadata_dict["data"] = data

    return ObjectMetadata.model_validate(object_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )


@pytest.fixture(scope="function")
def field_region_metadata() -> dict:
    """Generate valid field region metadata"""

    object_metadata_dict = _generate_object_metadata_base()

    data = AnyData.model_validate(
        {
            "content": enums.Content.field_region,
            "standard_result": None,
            "name": "VOLANTIS GP. Base",
            "alias": None,
            "tagname": None,
            "stratigraphic": False,
            "description": None,
            "geometry": None,
            "bbox": None,
            "format": enums.FileFormat.csv_xtgeo,
            "grid_model": None,
            "is_observation": False,
            "is_prediction": False,
            "layout": None,
            "offset": 0.6,
            "spec": PolygonsSpecification(
                npolys=2,
                columns=["X_UTME", "Y_UTMN", "Z_TVDSS", "POLY_ID"],
                num_columns=4,
                num_rows=200,
                size=800,
            ),
            "time": None,
            "undef_is_zero": None,
            "unit": "m",
            "vertical_domain": None,
            "domain_reference": None,
            "table_index": None,
            "base": None,
            "top": None,
            "field_region": FieldRegion(
                id=99,
            ),
        }
    )

    object_metadata_dict["class"] = enums.ObjectMetadataClass.polygons
    object_metadata_dict["data"] = data

    return ObjectMetadata.model_validate(object_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )


@pytest.fixture(scope="function")
def seismic_metadata() -> dict:
    """Generate valid seismic metadata"""

    object_metadata_dict = _generate_object_metadata_base()

    data = AnyData.model_validate(
        {
            "content": enums.Content.seismic,
            "standard_result": None,
            "name": "VIKING GP. Top",
            "alias": None,
            "tagname": None,
            "stratigraphic": True,
            "description": None,
            "geometry": None,
            "bbox": BoundingBox2D(
                xmin=456063.6875, xmax=467483.6875, ymin=5926551.0, ymax=5939431.0
            ),
            "format": enums.FileFormat.irap_binary,
            "grid_model": None,
            "is_observation": False,
            "is_prediction": True,
            "layout": enums.Layout.regular,
            "offset": 0.0,
            "spec": SurfaceSpecification(
                ncol=20,
                nrow=100,
                rotation=0.0,
                undef=0.0,
                xinc=0.1,
                yinc=0.1,
                xori=456063.6875,
                yori=5926551.0,
                yflip=enums.AxisOrientation.normal,
            ),
            "time": Time(
                t0=Timestamp(label="base", value=datetime.datetime.now(datetime.UTC)),
                t1=Timestamp(
                    label="monitor", value=datetime.datetime.now(datetime.UTC)
                ),
            ),
            "undef_is_zero": False,
            "unit": "m",
            "vertical_domain": "depth",
            "domain_reference": "msl",
            "table_index": None,
            "base": Layer(name="volantis_gp_base", offset=1.0, stratigraphic=True),
            "top": Layer(name="volantis_gp_top", offset=2.0, stratigraphic=True),
            "seismic": Seismic(attribute="amplitude", calculation="mean"),
        }
    )

    object_metadata_dict["class"] = enums.ObjectMetadataClass.surface
    object_metadata_dict["data"] = data

    return ObjectMetadata.model_validate(object_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )


@pytest.fixture(scope="function")
def volumes_metadata() -> dict:
    """Generate valid volumes metadata"""

    object_metadata_dict = _generate_object_metadata_base()

    data = AnyData.model_validate(
        {
            "content": enums.Content.volumes,
            "standard_result": None,
            "name": "geogrid",
            "alias": None,
            "tagname": None,
            "stratigraphic": False,
            "description": None,
            "geometry": None,
            "bbox": None,
            "format": enums.FileFormat.csv,
            "grid_model": None,
            "is_observation": False,
            "is_prediction": True,
            "layout": enums.Layout.table,
            "offset": 0.0,
            "spec": TableSpecification(
                columns=["ZONE", "REGION", "FLUID", "BULK_OIL"],
                num_columns=4,
                num_rows=10,
                size=40,
            ),
            "undef_is_zero": False,
            "unit": "m",
            "vertical_domain": "depth",
            "domain_reference": "msl",
            "table_index": ["FLUID", "ZONE", "REGION"],
            "base": None,
            "top": None,
        }
    )

    object_metadata_dict["class"] = enums.ObjectMetadataClass.table
    object_metadata_dict["data"] = data

    return ObjectMetadata.model_validate(object_metadata_dict).model_dump(
        mode="json", exclude_none=True, by_alias=True
    )
