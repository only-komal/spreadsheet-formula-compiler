# src/parser/parser.py
# Parser for spreadsheet formulas
# Converts tokens into an Abstract Syntax Tree (AST)
# Depends on the lexer to provide tokens
# Uses AST node classes to build the tree structure
# Supports numbers, cell references, ranges, binary operations, and function calls
# Raises syntax errors for invalid token sequences

from src.lexer.lexer import TokenType
from src.ast.nodes import (
    NumberNode,
    CellNode,
    RangeNode,
    BinaryOpNode,
    FunctionCallNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ------------------------------------------------------------------
    # Token stream access
    # ------------------------------------------------------------------
    def current_token(self):
        return self.tokens[self.pos]

    # ------------------------------------------------------------------
    # Controlled token consumption with basic error checking
    # ------------------------------------------------------------------
    def eat(self, token_type=None):
        token = self.current_token()

        if token_type and token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")

        self.pos += 1
        return token

    # ------------------------------------------------------------------
    # Entry point for parsing
    # ------------------------------------------------------------------
    def parse(self):
        node = self.expression()
        return node

    # ------------------------------------------------------------------
    # Expression level (+ -)
    # ------------------------------------------------------------------
    def expression(self):
        node = self.term()

        while (
            self.current_token().type == TokenType.OPERATOR
            and self.current_token().value in ("+", "-")
        ):
            op = self.eat(TokenType.OPERATOR).value
            right = self.term()
            node = BinaryOpNode(node, op, right)

        return node

    # ------------------------------------------------------------------
    # Term level (* /)
    # ------------------------------------------------------------------
    def term(self):
        node = self.factor()

        while (
            self.current_token().type == TokenType.OPERATOR
            and self.current_token().value in ("*", "/")
        ):
            op = self.eat(TokenType.OPERATOR).value
            right = self.factor()
            node = BinaryOpNode(node, op, right)

        return node

    # ------------------------------------------------------------------
    # Factor level (^)
    # ------------------------------------------------------------------
    def factor(self):
        node = self.primary()

        while (
            self.current_token().type == TokenType.OPERATOR
            and self.current_token().value == "^"
        ):
            op = self.eat(TokenType.OPERATOR).value
            right = self.primary()
            node = BinaryOpNode(node, op, right)

        return node

    # ------------------------------------------------------------------
    # Primary expressions (the atoms)
    # ------------------------------------------------------------------
    def primary(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token.value)

        if token.type == TokenType.CELL:
            self.eat(TokenType.CELL)
            return CellNode(token.value)

        if token.type == TokenType.RANGE:
            self.eat(TokenType.RANGE)
            return RangeNode(token.value)

        if token.type == TokenType.FUNCTION:
            return self.function_call()

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        raise SyntaxError(f"Unexpected token: {token}")

    # ------------------------------------------------------------------
    # Function call parsing
    # ------------------------------------------------------------------
    def function_call(self):
        name = self.eat(TokenType.FUNCTION).value
        self.eat(TokenType.LPAREN)

        args = []

        if self.current_token().type != TokenType.RPAREN:
            args.append(self.expression())

            while self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.expression())

        self.eat(TokenType.RPAREN)
        return FunctionCallNode(name, args)
