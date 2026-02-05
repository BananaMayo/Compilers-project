import pytest

import compiler.ast as ast
from compiler.parser import ParseError, parse
from compiler.tokenizer import tokenize

def test_literal() -> None:
    assert parse(tokenize("123")) == ast.Literal(123)

def test_identifier() -> None:
    assert parse(tokenize("x")) == ast.Identifier("x")

def test_left_associative_add_sub() -> None:
    assert parse(tokenize("1-2+3")) == ast.BinaryOp(
        ast.BinaryOp(ast.Literal(1), "-", ast.Literal(2)),
        "+",
        ast.Literal(3),
    )

def test_precedence() -> None:
    assert parse(tokenize("1+2*3")) == ast.BinaryOp(
        ast.Literal(1),
        "+",
        ast.BinaryOp(ast.Literal(2), "*", ast.Literal(3)),
    )

def test_parentheses() -> None:
    assert parse(tokenize("(1+2)*3")) == ast.BinaryOp(
        ast.BinaryOp(ast.Literal(1), "+", ast.Literal(2)),
        "*",
        ast.Literal(3),
    )

def test_empty_input_error() -> None:
    with pytest.raises(ParseError):
        parse([])

def test_garbage_at_end_error() -> None:
    with pytest.raises(ParseError):
        parse(tokenize("a + b c"))

def test_missing_closing_paren_error() -> None:
    with pytest.raises(ParseError):
        parse(tokenize("(1+2"))

def test_if_then_else() -> None:
    assert parse(tokenize("if a then b else c")) == ast.IfExpression(
        ast.Identifier("a"),
        ast.Identifier("b"),
        ast.Identifier("c"),
    )

def test_if_then_without_else() -> None:
    assert parse(tokenize("if a then b")) == ast.IfExpression(
        ast.Identifier("a"),
        ast.Identifier("b"),
        None,
    )

def test_if_inside_expression() -> None:
    assert parse(tokenize("1 + if true then 2 else 3")) == ast.BinaryOp(
        ast.Literal(1),
        "+",
        ast.IfExpression(
            ast.Identifier("true"),
            ast.Literal(2),
            ast.Literal(3),
        ),
    )

def test_nested_if() -> None:
    assert parse(tokenize("if a then if b then c else d else e")) == ast.IfExpression(
        ast.Identifier("a"),
        ast.IfExpression(
            ast.Identifier("b"),
            ast.Identifier("c"),
            ast.Identifier("d"),
        ),
        ast.Identifier("e"),
    )
