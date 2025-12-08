from __future__ import annotations

from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Literal,
)
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    GetJsonSchemaHandler,
    model_validator,
)

from fmu.datamodels.common.tracklog import User
from fmu.datamodels.types import MD5HashStr

from . import enums

if TYPE_CHECKING:
    from pydantic_core import CoreSchema


class File(BaseModel):
    """
    The ``file`` block contains references to this data object as a file on a disk.
    A filename in this context can be actual, or abstract. Particularly the
    ``relative_path`` is, and will most likely remain, an important identifier for
    individual file objects within an FMU case - irrespective of the existance of an
    actual file system. For this reason, the ``relative_path`` - as well as the
    ``checksum_md5`` will be generated even if a file is not saved to disk. The
    ``absolute_path`` will only be generated in the case of actually creating a file on
    disk and is not required under this schema.
    """

    absolute_path: Path | None = Field(
        default=None,
        examples=["/abs/path/share/results/maps/volantis_gp_base--depth.gri"],
    )
    """The absolute path of a file, e.g. /scratch/field/user/case/etc."""

    relative_path: Path = Field(
        examples=[
            "realization-0/iter-0/share/results/maps/volantis_gp_base--depth.gri"
        ],
    )
    """The path of a file relative to the case root."""

    runpath_relative_path: Path | None = Field(
        default=None,
        examples=["share/results/maps/volantis_gp_base--depth.gri"],
    )
    """
    The path of a file relative to the runpath root of the realization.
    For files exported with the fmu.context ``case`` the field will be None.
    """

    checksum_md5: MD5HashStr = Field(examples=["fa4d055b113ae5282796e328cde0ffa4"])
    """A valid MD5 checksum of the file."""

    size_bytes: int | None = Field(default=None)
    """Size of file object in bytes"""

    @model_validator(mode="before")
    @classmethod
    def _check_for_non_ascii_in_path(cls, values: dict) -> dict:
        if (path := values.get("absolute_path")) and not str(path).isascii():
            raise ValueError(
                f"Path has non-ascii elements which is not supported: {path}"
            )
        return values


class Aggregation(BaseModel):
    """
    The ``fmu.aggregation`` block contains information about an aggregation
    performed over an ensemble.
    """

    id: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """The unique identifier of an aggregation."""

    operation: str
    """A string representing the type of aggregation performed."""

    realization_ids: list[int]
    """An array of realization ids included in this aggregation."""


class Workflow(BaseModel):
    """
    The ``fmu.workflow`` block refers to specific subworkflows within the large
    FMU workflow being ran. This has not been standardized, mainly due to the lack of
    programmatic access to the workflows being run in important software within FMU.

    .. note:: A key usage of ``fmu.workflow.reference`` is related to ensuring
       uniqueness of data objects.
    """

    reference: str
    """A string referring to which workflow this data object was exported by."""


class Case(BaseModel):
    """
    The ``fmu.case`` block contains information about the case from which this data
    object was exported.

    A case represent a set of ensembles that belong together, either by being part of
    the same run (i.e. history matching) or by being placed together by the user,
    corresponding to /scratch/<asset>/<user>/<my case name>/.

    .. note:: If an FMU data object is exported outside the case context, this block
       will not be present.
    """

    name: str = Field(examples=["MyCaseName"])
    """The name of the case."""

    user: User
    """A block holding information about the user.
    See :class:`User`."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """The unique identifier of this case. Currently made by fmu.dataio."""

    description: list[str] | None = Field(default=None)
    """A free-text description of this case."""


class Ert(BaseModel):
    """The ``fmu.ert`` block contains information about the current ert run."""

    experiment: Experiment
    """Reference to the ert experiment.
    See :class:`Experiment`."""

    simulation_mode: enums.ErtSimulationMode
    """Reference to the ert simulation mode.
    See :class:`SimulationMode`."""


class Experiment(BaseModel):
    """The ``fmu.ert.experiment`` block contains information about
    the current ert experiment run."""

    id: UUID
    """The unique identifier of this ert experiment run."""


class Ensemble(BaseModel):
    """
    The ``fmu.ensemble`` block contains information about the ensemble this data
    object belongs to.
    """

    id: int = Field(ge=0)
    """The internal identification of this ensemble, represented by an integer."""

    name: str = Field(examples=["iter-0"])
    """The name of the ensemble. This is typically reflecting the folder name on
    scratch. In ERT, custom names for ensembles are supported, e.g. "pred"."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """The unique identifier of this case. Currently made by fmu.dataio."""

    restart_from: UUID | None = Field(
        default=None,
        examples=["15ce3b84-766f-4c93-9050-b154861f9100"],
    )
    """A uuid reference to another ensemble that this ensemble was restarted
    from"""


class Model(BaseModel):
    """The ``fmu.model`` block contains information about the model used.

    .. note::
       Synonyms for "model" in this context are "template", "setup", etc. The term
       "model" is ultra-generic but was chosen before e.g. "template" as the latter
       deviates from daily communications and is, if possible, even more generic
       than "model".
    """

    description: list[str] | None = Field(default=None)
    """This is a free text description of the model setup"""

    name: str = Field(examples=["Drogon"])
    """The name of the model."""

    revision: str = Field(examples=["21.0.0.dev"])
    """The revision of the model."""


class Realization(BaseModel):
    """
    The ``fmu.realization`` block contains information about the realization this
    data object belongs to.
    """

    id: int = Field(ge=0)
    """The internal ID of the realization, represented by an integer."""

    name: str = Field(examples=["realization-0"])
    """The name of the realization. This is typically reflecting the folder name on
    scratch. We recommend to use ``fmu.realization.id`` for all usage except purely
    visual appearance."""

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """The universally unique identifier for this realization. It is a hash of
    ``fmu.case.uuid`` and ``fmu.ensemble.uuid`` and ``fmu.realization.id``."""

    is_reference: bool | None = Field(default=None)
    """
    Flag used to determine if this realization is tagged as a reference.

    Typically, a reference realization is one that includes prediction surfaces and
    maintains all other input parameters at their default settings. However, caution
    must be exercised when putting logic upon this field, as this is simply a selected
    realization by the user and no guarantees of what the realization represents
    can be made.

    .. note::
        Please note that users shall not set this flag in the metadata upon export;
        it is intended to be configured through interactions with the Sumo GUI.
    """


class Display(BaseModel):
    """
    The ``display`` block contains information related to how this data object
    should/could be displayed. As a general rule, the consumer of data is responsible
    for figuring out how a specific data object shall be displayed. However, we use
    this block to communicate preferences from the data producers perspective.

    We also maintain this block due to legacy reasons. No data filtering logic should
    be placed on the ``display`` block.
    """

    name: str | None = Field(default=None)
    """A display-friendly version of ``data.name``."""


class Context(BaseModel):
    """
    The ``fmu.context`` block contains the FMU context in which this data object
    was produced.
    """

    stage: enums.FMUContext
    """The stage of an FMU experiment in which this data was produced.
    See :class:`enums.FMUContext`."""


class IterationContext(Context):
    """
    The ``fmu.context`` block contains the FMU context in which this data object
    was produced. Here ``stage`` is required to be ``iteration``.
    """

    stage: Literal[enums.FMUContext.iteration] = Field(
        default=enums.FMUContext.iteration
    )


class EnsembleContext(Context):
    """
    The ``fmu.context`` block contains the FMU context in which this data object
    was produced. Here ``stage`` is required to be ``ensemble``.
    """

    stage: Literal[enums.FMUContext.ensemble] = Field(default=enums.FMUContext.ensemble)


class RealizationContext(Context):
    """
    The ``fmu.context`` block contains the FMU context in which this data object
    was produced. Here ``stage`` is required to be ``realization``.
    """

    stage: Literal[enums.FMUContext.realization] = Field(
        default=enums.FMUContext.realization
    )


class FMUBase(BaseModel):
    """
    The ``fmu`` block contains all attributes specific to FMU. The idea is that the FMU
    results data model can be applied to data from *other* sources - in which the
    fmu-specific stuff may not make sense or be applicable.
    """

    case: Case
    """The ``fmu.case`` block contains information about the case from which this data
    object was exported. See :class:`Case`."""

    model: Model
    """The ``fmu.model`` block contains information about the model used.
    See :class:`Model`."""


class FMUIteration(FMUBase):
    """Deprecated and replaced by :class:`FMUEnsemble`."""

    context: IterationContext
    """The ``fmu.context`` block contains the FMU context in which this data object
    was produced. See :class:`Context`. For ``iteration`` the context is ``iteration``.
    """

    iteration: Ensemble
    """The ``fmu.iteration`` block contains information about the iteration this data
    object belongs to. See :class:`Iteration`. """


class FMUEnsemble(FMUBase):
    """
    The ``fmu`` block contains all attributes specific to FMU. The idea is that the FMU
    results data model can be applied to data from *other* sources - in which the
    fmu-specific stuff may not make sense or be applicable.
    This is a specialization of the FMU block for ``ensemble`` objects.
    """

    context: EnsembleContext
    """The ``fmu.context`` block contains the FMU context in which this data object
    was produced. See :class:`Context`. For ``ensemble`` the context is ``ensemble``.
    """

    ensemble: Ensemble
    """The ``fmu.ensemble`` block contains information about the ensemble this data
    object belongs to. See :class:`ensemble`. """


class FMURealization(FMUBase):
    """
    The ``fmu`` block contains all attributes specific to FMU. The idea is that the FMU
    results data model can be applied to data from *other* sources - in which the
    fmu-specific stuff may not make sense or be applicable.
    This is a specialization of the FMU block for ``realization`` objects.
    """

    context: RealizationContext
    """The ``fmu.context`` block contains the FMU context in which this data object
    was produced. See :class:`Context`. For ``realization`` the context is always
    ``realization``.
    """

    ensemble: Ensemble
    """The ``fmu.ensemble`` block contains information about the ensemble this data
    object belongs to. See :class:`ensemble`. """

    iteration: Ensemble | None = Field(default=None)
    """Deprecated and replaced by ``fmu.ensemble``"""

    realization: Realization
    """The ``fmu.realization`` block contains information about the realization this
    data object belongs to. See :class:`Realization`."""


class Entity(BaseModel):
    """
    The ``fmu.entity`` block identifies data objects representing the same entity
    within a case, i.e. both realizations and aggregations of a particular entity
    will share the same unique identifier.
    """

    uuid: UUID = Field(examples=["15ce3b84-766f-4c93-9050-b154861f9100"])
    """The unique identifier of an object entity within a case."""


class FMU(FMUBase):
    """
    The ``fmu`` block contains all attributes specific to FMU. The idea is that the FMU
    results data model can be applied to data from *other* sources - in which the
    fmu-specific stuff may not make sense or be applicable.
    """

    context: Context
    """The ``fmu.context`` block contains the FMU context in which this data object
    was produced. See :class:`Context`.  """

    ensemble: Ensemble | None = Field(default=None)
    """The ``fmu.ensemble`` block contains information about the ensemble this data
    object belongs to. See :class:`Ensemble`. """

    iteration: Ensemble | None = Field(default=None)
    """Deprecated and replaced by ``fmu.ensemble``"""

    workflow: Workflow | None = Field(default=None)
    """The ``fmu.workflow`` block refers to specific subworkflows within the large
    FMU workflow being ran. See :class:`Workflow`."""

    aggregation: Aggregation | None = Field(default=None)
    """The ``fmu.aggregation`` block contains information about an aggregation
    performed over an ensemble. See :class:`Aggregation`."""

    realization: Realization | None = Field(default=None)
    """The ``fmu.realization`` block contains information about the realization this
    data object belongs to. See :class:`Realization`."""

    entity: Entity | None = Field(default=None)
    """The ``fmu.entity`` block identifies data objects representing the same entity
    within a case. Note, for objects exported in context ``case`` this field will
    be empty. See :class:`Ensemble`."""

    ert: Ert | None = Field(default=None)
    """The ``fmu.ert`` block contains information about the current ert run
    See :class:`Ert`."""

    @model_validator(mode="after")
    def _set_iteration_equal_ensemble(self) -> FMU:
        """
        The 'fmu.ensemble' field has replaced the 'fmu.iteration' field. However in a
        transition period we keep both, hence we set the 'fmu.iteration' here.
        """
        self.iteration = self.ensemble
        return self

    @model_validator(mode="before")
    @classmethod
    def _dependencies_aggregation_realization(cls, values: dict) -> dict:
        aggregation, realization = values.get("aggregation"), values.get("realization")
        if aggregation and realization:
            raise ValueError(
                "Both 'aggregation' and 'realization' cannot be set "
                "at the same time. Please set only one."
            )
        return values

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> dict[str, object]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(
            {
                "dependencies": {
                    "aggregation": {"not": {"required": ["realization"]}},
                    "realization": {"not": {"required": ["aggregation"]}},
                }
            }
        )
        return json_schema
