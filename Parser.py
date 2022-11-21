from typing import List
from TokenType import Token, TokenType
from Expr import Expr, Binary, Unary, Literal, Grouping

"""
unambiguous grammar
---------------------------------------------------------------
expression -> equality
equality -> comparison(("!="|"==") comparison)*
comparison -> term((">"|">="|"<"|"<=")term)*
term -> factor(("-"|"+")factor)*
factor -> unary(("/"|"*")unary)*
unary -> ("!"|"-") unary | primary
primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"
"""

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current: int = 0

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise Exception(f"{self.peek()}{message}")

    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]):
            return Literal(TokenType.FALSE)
        if self.match([TokenType.TRUE]):
            return Literal(TokenType.TRUE)
        if self.match([TokenType.NIL]):
            return Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        if self.match([TokenType.LEFT_PAREN]):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        return Literal(None)

    def unary(self) -> Expr:
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.primary()

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def match(self, types: List[TokenType]) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def expression(self) -> Expr:
        return self.equality()
Parser([])