from __future__ import annotations

from typing import List


def tokenize(source_code: str) -> List[str]:
    tokens: List[str] = []
    i = 0
    n = len(source_code)

    while i < n:
        c = source_code[i]

        if c.isspace():
            i += 1
            continue

        if c.isalpha() or c == "_":
            start = i
            i += 1
            while i < n and (source_code[i].isalnum() or source_code[i] == "_"):
                i += 1
            tokens.append(source_code[start:i])
            continue

        if c.isdigit():
            start = i
            i += 1
            while i < n and source_code[i].isdigit():
                i += 1
            tokens.append(source_code[start:i])
            continue

        raise ValueError(f"unexpected character {c!r} at index {i}")

    return tokens
