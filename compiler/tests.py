import pytest
from lex import Lexer, Token, TokenKind


def test_lex_ints():
    tokens = Lexer("44").lex()
    assert tokens[0] == Token(TokenKind.DecIntegerLiteral, "44")

    tokens = Lexer("0x44").lex()
    assert tokens[0] == Token(TokenKind.HexIntegerLiteral, "0x44")

    tokens = Lexer("0b10_10").lex()
    assert tokens[0] == Token(TokenKind.BinIntegerLiteral, "0b10_10")


def test_lex_strs():
    tokens = Lexer('"Hello, World!"').lex()
    assert tokens[0] == Token(TokenKind.StringLiteral, "Hello, World!")

    # tokens = Lexer('"\"Foo\""').lex()
    # assert tokens[0] == Token(TokenKind.StringLiteral, '\"Foo\"')


def test_lex_var_def():
    tokens = Lexer("a: int = 44;").lex()
    assert tokens == [
        Token(TokenKind.Identifier, "a"),
        Token(TokenKind.Colon, ":"),
        Token(TokenKind.Keyword, "int"),
        Token(TokenKind.EqualSign, "="),
        Token(TokenKind.DecIntegerLiteral, "44"),
        Token(TokenKind.Semicolon, ";"),
    ]
