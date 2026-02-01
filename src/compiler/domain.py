from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int


class _AnyLocation(SourceLocation):
    def __init__(self) -> None:
        super().__init__(line=-1, column=-1)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SourceLocation)


L = _AnyLocation()


@dataclass(frozen=True)
class Token:
    loc: SourceLocation
    type: str
    text: str
