from __future__ import annotations

from compiler.domain import SourceLocation, Token

def tokenize(source_code: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    line = 1
    column = 0
    
    n = len(source_code)

    two_char = {"==", "!=", "<=", ">="}
    one_char = {"+", "-", "*", "/", "%", "=", "<", ">"}
    punctuation = {"(", ")", "{", "}", ",", ";"}

    while i < n:
        c = source_code[i]
        start_i = i
        start_column = column

        if c.isspace():
            if c == "\n":
                line += 1
                column = 0
            else:
                column += 1
            i += 1
            continue

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

        if c == "#":
            i += 1
            column += 1
            while i < n and source_code[i] != "\n":
                i += 1
                column += 1
            continue

        if c == "/" and i + 1 < n and source_code[i + 1] == "/":
            i += 2
            column += 2
            while i < n and source_code[i] != "\n":
                i += 1
                column += 1
            continue

        if i + 1 < n:
            op2 = source_code[i:i + 2]
            if op2 in two_char:
                i += 2
                column += 2
                tokens.append(Token(SourceLocation(line, start_column), "operator", op2))
                continue

        if c in one_char:
            i += 1
            column += 1
            tokens.append(Token(SourceLocation(line, start_column), "operator", c))
            continue

        if c in punctuation:
            i += 1
            column += 1
            tokens.append(Token(SourceLocation(line, start_column), "punctuation", c))
            continue

        raise ValueError(f"unexpected character {c!r} at line {line} column {column}")

    return tokens
