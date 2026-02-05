from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    pass

@dataclass(frozen=True)
class Literal(Expression):
    value: int

@dataclass(frozen=True)
class Identifier(Expression):
    name: str

@dataclass(frozen=True)
class BinaryOp(Expression):
    left: Expression
    op: str
    right: Expression

@dataclass(frozen=True)
class IfExpression(Expression):
    condition_branch: Expression
    then_branch: Expression
    else_branch: Expression | None
