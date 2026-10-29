from typing import Annotated, TypeAlias

from pydantic import Field

VersionStr: TypeAlias = Annotated[
    str, Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
]

# Support both hex and base64 MD5 checksums.
MD5HashStr: TypeAlias = Annotated[
    str,
    Field(pattern=r"^([a-fA-F0-9]{32}|[A-Za-z0-9+/]{21}[AQgw]==)$"),
]
