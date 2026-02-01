import pytest

from compiler.tokenizer import tokenize


def test_tokenizer_basics() -> None:
    assert tokenize("if 3\nwhile") == ["if", "3", "while"]


def test_identifiers() -> None:
    assert tokenize("_") == ["_"]
    assert tokenize("_abc") == ["_abc"]
    assert tokenize("A_b9") == ["A_b9"]
    assert tokenize("hello_world123") == ["hello_world123"]


def test_integers() -> None:
    assert tokenize("0") == ["0"]
    assert tokenize("007") == ["007"]
    assert tokenize("123 456") == ["123", "456"]


def test_skips_whitespace() -> None:
    assert tokenize(" \t\n  foo \n  42 \tbar  ") == ["foo", "42", "bar"]


def test_rejects_unknown_characters() -> None:
    with pytest.raises(ValueError):
        tokenize("3-2")
