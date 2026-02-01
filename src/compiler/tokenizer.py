from __future__ import annotations

from compiler.domain import SourceLocation, Token

def tokenize(source_code: str) -> List[str]:
    tokens: list[Token] = []
    i = 0
    line = 1
    column = 0
    n = len(source_code)

    while i < n:
        c = source_code[i]

        if c.isspace():
            if c == "\n":
                line += 1
                column = 0
            else:
                column += 1
            i += 1
            continue

        start_i = i
        start_column = column

        if c.isalpha() or c == "_":
            i += 1
            column += 1
            while i < n and (source_code[i].isalnum() or source_code[i] == "_"):
                i += 1
                column += 1
            text = source_code[start_i:i]
            tokens.append(Token(SourceLocation(line, start_column), "identifier", text))
            continue

        if c.isdigit():
            i += 1
            column += 1
            while i < n and source_code[i].isdigit():
                i += 1
                column += 1
            text = source_code[start_i:i]
            tokens.append(Token(SourceLocation(line, start_column), "int_literal", text))
            continue

        raise ValueError(f"unexpected character {c!r} at line {line}, column {column}")

    return tokens
