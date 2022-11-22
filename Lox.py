import sys
from TokenType import Token, TokenType
from Parser import Parser
from Scanner import Scanner
from Expr import Expr
from AstPrinter import AstPrinter


"""
Lox syntactic grammar:

ambiguous grammar
---------------------------------------------------------------
epxression -> literal | unary | binary | grouping
literal -> NUMBER | STRING | 'true' | 'false' | 'nil'
grouping -> "(" expression ")"
unary -> ("-" | "!") expression
binary -> expression operator expression
operator -> "==" | "!=" | "<" | "<=" | ">" | "+" | "-" | "*" | "/"

unambiguous grammar
---------------------------------------------------------------
primary -> equality
equality -> comparison(("!="|"==") comparison)*
comparison -> term((">"|">="|"<"|"<=")term)*
term -> factor(("-"|"+")factor)*
primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"
unary -> ("!"|"-") unary | primary
factor -> unary(("/"|"*")unary)*
"""

class Lox:
    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        # hadError = True

    @staticmethod
    def error(line: int = 0, message: str = "", token: Token | None = None):
        if not token:
            Lox.report(line, "", message)
        else:
            if token.type == TokenType.EOF:
                Lox.report(token.line, " at end", message)
            else:
                Lox.report(token.line, f" at'{token.lexeme}'", message)

    def run(self, source: str) -> None:
        tokens = Scanner(source).scanTokens()
        parser: Parser = Parser(tokens)
        expression: Expr | None = parser.parse()
        if not expression:
            return
        print(AstPrinter().print(expression))

    def runPrompt(self):
        while True:
            line = input("> ")
            if not line:
                break
            self.run(line)

    def runFile(self, path: str) -> None:
        raise NotImplementedError("Has not been implemented yet!")

    def __init__(self) -> None:
        self.hadError = False

        if len(sys.argv) > 2:
            raise Exception("Usage:plox [script]")
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[0])
        else:
            self.runPrompt();

Lox()
