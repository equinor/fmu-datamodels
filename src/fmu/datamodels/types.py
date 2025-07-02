from typing import Annotated, TypeAlias

from pydantic import Field

VersionStr: TypeAlias = Annotated[
    str, Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
]

MD5HashStr: TypeAlias = Annotated[str, Field(pattern=r"^([a-f\d]{32}|[A-F\d]{32})$")]
