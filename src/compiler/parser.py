from __future__ import annotations

import compiler.ast as ast
from compiler.domain import SourceLocation, Token


class ParseError(Exception):
    pass

def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0

    def end_location() -> SourceLocation:
        if len(tokens) == 0:
            return SourceLocation(line=1, column=0)
        return tokens[-1].loc

    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        return Token(loc=end_location(), type="end", text="")

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()

        if expected is not None:
            if isinstance(expected, str):
                if token.text != expected:
                    raise ParseError(f'{token.loc}: expected "{expected}"')
            else:
                if token.text not in expected:
                    opts = ", ".join([f'"{x}"' for x in expected])
                    raise ParseError(f"{token.loc}: expected one of: {opts}")

        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        if peek().type != "int_literal":
            raise ParseError(f"{peek().loc}: expected an integer literal")
        token = consume()
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type != "identifier":
            raise ParseError(f"{peek().loc}: expected an identifier")
        token = consume()
        return ast.Identifier(token.text)

    def parse_factor() -> ast.Expression:
        if peek().type == "identifier" and peek().text == "if":
            return parse_if_expression()
        if peek().type == "punctuation" and peek().text == "(":
            consume("(")
            expr = parse_expression()
            consume(")")
            return expr
        if peek().type == "int_literal":
            return parse_int_literal()
        if peek().type == "identifier":
            return parse_identifier()
        raise ParseError(f'{peek().loc}: expected "(", an integer literal or an identifier')

    def parse_term() -> ast.Expression:
        left = parse_factor()
        while peek().type == "operator" and peek().text in ["*", "/", "%"]:
            operator_token = consume()
            right = parse_factor()
            left = ast.BinaryOp(left, operator_token.text, right)
        return left

    def parse_expression() -> ast.Expression:
        left = parse_term()
        while peek().type == "operator" and peek().text in ["+", "-"]:
            operator_token = consume()
            right = parse_term()
            left = ast.BinaryOp(left, operator_token.text, right)
        return left

    def parse_if_expression() -> ast.Expression:
        consume("if")
        cond = parse_expression()
        consume("then")
        then_branch = parse_expression()
        else_branch: ast.Expression | None = None
        if peek().type == "identifier" and peek().text == "else":
            consume("else")
            else_branch = parse_expression()
        return ast.IfExpression(cond, then_branch, else_branch)

    if len(tokens) == 0:
        raise ParseError("empty input")

    result = parse_expression()

    if peek().type != "end":
        t = peek()
        raise ParseError(f"{t.loc}: unexpected token {t.type}({t.text})")

    return result
