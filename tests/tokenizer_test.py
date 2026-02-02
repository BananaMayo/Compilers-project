import pytest

from compiler.tokenizer import tokenize
from compiler.domain import L, Token

def test_tokenizer_basics() -> None:
    assert tokenize("if 3\nwhile") == [
        Token(loc=L, type="identifier", text="if"),
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="identifier", text="while"),
    ]

def test_integers() -> None:
    assert tokenize("0") == [Token(L, "int_literal", "0")]
    assert tokenize("007") == [Token(L, "int_literal", "007")]
    assert tokenize("123 456") == [
        Token(L, "int_literal", "123"),
        Token(L, "int_literal", "456"),
    ]


def test_operators() -> None:
    assert tokenize("a==b!=c<=d>=e<f>g") == [
        Token(L, "identifier", "a"),
        Token(L, "operator", "=="),
        Token(L, "identifier", "b"),
        Token(L, "operator", "!="),
        Token(L, "identifier", "c"),
        Token(L, "operator", "<="),
        Token(L, "identifier", "d"),
        Token(L, "operator", ">="),
        Token(L, "identifier", "e"),
        Token(L, "operator", "<"),
        Token(L, "identifier", "f"),
        Token(L, "operator", ">"),
        Token(L, "identifier", "g"),
    ]

def test_single_char_operators() -> None:
    assert tokenize("x=1+2*3/4%5-6") == [
        Token(L, "identifier", "x"),
        Token(L, "operator", "="),
        Token(L, "int_literal", "1"),
        Token(L, "operator", "+"),
        Token(L, "int_literal", "2"),
        Token(L, "operator", "*"),
        Token(L, "int_literal", "3"),
        Token(L, "operator", "/"),
        Token(L, "int_literal", "4"),
        Token(L, "operator", "%"),
        Token(L, "int_literal", "5"),
        Token(L, "operator", "-"),
        Token(L, "int_literal", "6"),
    ]


def test_punctuation() -> None:
    assert tokenize("f(a,b);{x}") == [
        Token(L, "identifier", "f"),
        Token(L, "punctuation", "("),
        Token(L, "identifier", "a"),
        Token(L, "punctuation", ","),
        Token(L, "identifier", "b"),
        Token(L, "punctuation", ")"),
        Token(L, "punctuation", ";"),
        Token(L, "punctuation", "{"),
        Token(L, "identifier", "x"),
        Token(L, "punctuation", "}"),
    ]


def test_skips_comments() -> None:
    assert tokenize("a # hi\nb") == [
        Token(L, "identifier", "a"),
        Token(L, "identifier", "b"),
    ]
    assert tokenize("a // hi\nb") == [
        Token(L, "identifier", "a"),
        Token(L, "identifier", "b"),
    ]

def test_locations() -> None:
    tokens = tokenize("a 1\nb")
    assert tokens[0].loc.line == 1
    assert tokens[0].loc.column == 0
    assert tokens[1].loc.line == 1
    assert tokens[1].loc.column == 2
    assert tokens[2].loc.line == 2
    assert tokens[2].loc.column == 0

def test_rejects_unknown_characters() -> None:
    with pytest.raises(ValueError):
        tokenize("@")
