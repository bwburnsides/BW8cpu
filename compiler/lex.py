from dataclasses import dataclass
from enum import Enum
from typing import Optional
import string

from shared import Stream


class UnexpectedTokenError(Exception):
    pass


Keywords = {
    "word",
    "uword",
    "int",
    "uint",
    "long",
    "ulong",
    "char",
    "sizeof",
    "offsetof",
    "const",
    "if",
    "while",
    "break",
    "continue",
    "return",
    "fn",
    "struct",
    "union",
    "extern",
}


class TokenKind(Enum):
    Keyword = "Keyword"
    Identifier = "Ident"
    DecIntegerLiteral = "DecInteger"
    HexIntegerLiteral = "HexInteger"
    BinIntegerLiteral = "BinInteger"
    StringLiteral = "String"
    CharLiteral = "Char"

    # Structural
    Colon = ":"
    Semicolon = ";"
    LeftParen = "("
    RightParen = ")"
    LeftBrace = "{"
    RightBrace = "}"
    EOF = "EOF"

    # Arithmetic and Logical Operators
    PlusSign = "+"
    MinusSign = "-"
    TimesSign = "*"
    DivisionSign = "/"
    ModuloSign = "%"
    LeftShift = "<<"
    RightShift = ">>"
    BitwiseAnd = "&"
    BitwiseOr = "|"
    BitwiseXor = "^"
    BitwiseNot = "!"

    # Assignment Operators
    EqualSign = "="
    PlusEqual = "+="
    MinusEqual = "-="
    TimesEqual = "*="
    DivideEqual = "/="
    ModuloEqual = "%="
    LeftShiftEqual = "<<="
    RightShiftEqual = ">>="
    BitwiseAndEqual = "&="
    BitwiseOrEqual = "|="
    BitwiseXorEqual = "^="

    # Relational Operators
    ShortCircuitAnd = "&&"
    ShortCircuitOr = "||"
    DoubleEqualSign = "=="
    NotEqual = "!="
    GreaterThan = ">"
    LessThan = "<"
    GreaterEqual = ">="
    LessEqual = "<="

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class Token:
    kind: TokenKind
    value: str

    def __repr__(self) -> str:
        return f'Token({self.kind}, "{self.value}")'


class Lexer:
    WORD_INIT_CHARS = set(string.ascii_letters) | set("_")
    WORD_CHARS = WORD_INIT_CHARS | set(string.digits)

    INT_INIT_CHARS = set("123456789")
    INT_CHARS = INT_INIT_CHARS | set("_0")
    HEX_CHARS = INT_CHARS | set("abcdefABCDEF")
    BIN_CHARS = set("_01")

    def __init__(self, source: str):
        self.src = Stream(source)

    def lex(self) -> list[Token]:
        tokens = []
        in_comment = False
        while self.src.current is not None:
            char = self.src.current

            if in_comment:
                if char == "\n":
                    in_comment = False
                self.src.advance()
                continue

            if char == "#":
                in_comment = True
            elif char == ":":
                tokens.append(Token(kind=TokenKind.Colon, value=char))
            elif char == ";":
                tokens.append(Token(kind=TokenKind.Semicolon, value=char))
            elif char == "(":
                tokens.append(Token(kind=TokenKind.LeftParen, value=char))
            elif char == ")":
                tokens.append(Token(kind=TokenKind.RightParen, value=char))
            elif char == "{":
                tokens.append(Token(kind=TokenKind.LeftBrace, value=char))
            elif char == "}":
                tokens.append(Token(kind=TokenKind.RightBrace, value=char))
            elif char == "+":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.PlusEqual, TokenKind.PlusSign
                    )
                )
            elif char == "-":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.MinusEqual, TokenKind.MinusSign
                    )
                )
            elif char == "*":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.TimesEqual, TokenKind.TimesSign
                    )
                )
            elif char == "/":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.DivideEqual, TokenKind.DivisionSign
                    )
                )
            elif char == "%":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.ModuloEqual, TokenKind.ModuloSign
                    )
                )
            elif char == "=":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.DoubleEqualSign, TokenKind.EqualSign
                    )
                )
            elif char == "^":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.BitwiseXorEqual, TokenKind.BitwiseXor
                    )
                )
            elif char == "!":
                tokens.append(
                    self.make_multichar_operator(
                        char, "=", TokenKind.NotEqual, TokenKind.BitwiseNot
                    )
                )

            elif char == "&":
                if self.src.next == "=":
                    token = Token(kind=TokenKind.BitwiseAndEqual, value="&=")
                    self.src.advance()
                elif self.src.next == "&":
                    token = Token(kind=TokenKind.ShortCircuitAnd, value="&&")
                    self.src.advance()
                else:
                    token = Token(kind=TokenKind.BitwiseAnd, value="&")
                tokens.append(token)

            elif char == "|":
                if self.src.next == "=":
                    token = Token(kind=TokenKind.BitwiseOrEqual, value="|=")
                    self.src.advance()
                elif self.src.next == "|":
                    token = Token(kind=TokenKind.ShortCircuitOr, value="||")
                    self.src.advance()
                else:
                    token = Token(kind=TokenKind.BitwiseOr, value="|")
                tokens.append(token)

            elif char == ">":
                if self.src.next == "=":
                    token = Token(kind=TokenKind.GreaterEqual, value=">=")
                    self.src.advance()
                elif self.src.next == ">":
                    self.src.advance()
                    if self.src.next == "=":
                        token = Token(kind=TokenKind.RightShiftEqual, value=">>=")
                        self.src.advance()
                    else:
                        token = Token(kind=TokenKind.RightShift, value=">>")
                else:
                    token = Token(kind=TokenKind.GreaterThan, value=">")
                tokens.append(token)

            elif char == "<":
                if self.src.next == "=":
                    token = Token(kind=TokenKind.LessEqual, value="<=")
                    self.src.advance()
                elif self.src.next == "<":
                    self.src.advance()
                    if self.src.next == "=":
                        token = Token(kind=TokenKind.LeftShiftEqual, value="<<=")
                        self.src.advance()
                    else:
                        token = Token(kind=TokenKind.LeftShift, value="<<")
                else:
                    token = Token(kind=TokenKind.LessThan, value="<")
                tokens.append(token)

            elif char == '"':
                tokens.append(
                    Token(kind=TokenKind.StringLiteral, value=self.make_string())
                )
            elif char == "'":
                tokens.append(Token(kind=TokenKind.CharLiteral, value=self.make_char()))

            elif char in self.INT_INIT_CHARS:
                tokens.append(
                    Token(
                        kind=TokenKind.DecIntegerLiteral, value=self.make_dec_int(char)
                    )
                )
            elif char == "0":
                result = self.make_hex_int(char)
                if result is not None:
                    tokens.append(Token(kind=TokenKind.HexIntegerLiteral, value=result))
                else:
                    result = self.make_bin_int(char)
                    if result is not None:
                        tokens.append(
                            Token(kind=TokenKind.BinIntegerLiteral, value=result)
                        )
                    else:
                        raise UnexpectedTokenError(
                            f"Unexpected token while scanning Hex/Bin literal: '{self.src.next}'"
                        )

            elif char in self.WORD_INIT_CHARS:
                result = self.make_word(char)
                if result in Keywords:
                    tokens.append(Token(kind=TokenKind.Keyword, value=result))
                else:
                    tokens.append(Token(kind=TokenKind.Identifier, value=result))

            self.src.advance()

        tokens.append(Token(kind=TokenKind.EOF, value="EOF"))
        return tokens

    def make_multichar_operator(
        self,
        first_char: str,
        second_char: str,
        match_kind: TokenKind,
        not_match_kind: TokenKind,
    ):
        if self.src.next == second_char:
            self.src.advance()
            return Token(kind=match_kind, value=f"{first_char}{second_char}")
        return Token(kind=not_match_kind, value=first_char)

    def make_word(self, init_char: str) -> str:
        chars = [init_char]
        while self.src.next in self.WORD_CHARS:
            char = self.src.next
            self.src.advance()
            chars.append(char)

        return "".join(chars)

    def make_dec_int(self, init_char: str) -> str:
        chars = [init_char]
        while self.src.next in self.INT_CHARS:
            char = self.src.next
            self.src.advance()
            chars.append(char)

        return "".join(chars)

    def make_hex_int(self, init_char: str) -> Optional[str]:
        if self.src.next != "x":
            return None

        self.src.advance()
        chars = [init_char, self.src.current]
        while self.src.next is not None and self.src.next in self.HEX_CHARS:
            char = self.src.next
            self.src.advance()
            chars.append(char)

        return "".join(chars)

    def make_bin_int(self, init_char: str) -> Optional[str]:
        if self.src.next != "b":
            return None

        self.src.advance()
        chars = [init_char, self.src.current]
        while self.src.next is not None and self.src.next in self.BIN_CHARS:
            char = self.src.next
            self.src.advance()
            chars.append(char)

        return "".join(chars)

    def make_string(self) -> str:
        chars = []
        while self.src.next is not None and self.src.next != '"':
            if self.src.next == "\\":
                self.src.advance()
                if self.src.next == "n":
                    char = "\n"
                elif self.src.next == "r":
                    char = "\r"
                elif self.src.next == "t":
                    char = "\t"
                elif self.src.next == '"':
                    char = '"'
                elif self.src.next == "\\":
                    char = "\\"
                else:
                    char = f"\\{self.src.next}"
            else:
                char = self.src.next

            chars.append(char)
            self.src.advance()

        self.src.advance()
        return "".join(chars)

    def make_char(self) -> str:
        if self.src.next == "\\":
            self.src.advance()
            if self.src.next == "n":
                char = "\n"
            elif self.src.next == "r":
                char = "\r"
            elif self.src.next == "t":
                char = "\t"
            elif self.src.next == "'":
                char = "'"
            elif self.src.next == "\\":
                char = "\\"
            else:
                raise UnexpectedTokenError(
                    f"Unexpected token while scanning char literal: '{self.src.next}'"
                )
        else:
            char = self.src.next

        self.src.advance()
        if self.src.next == "'":
            self.src.advance()
            return char

        raise UnexpectedTokenError(
            f"Unexpected token while scanning char literal: '{self.src.next}'"
        )
