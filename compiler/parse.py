from dataclasses import dataclass
from enum import Enum, auto

from lex import Token
from shared import Stream

class ExternDeclarationKind(Enum):
    FuncDecl = auto()
    ConstDecl = auto()
    VarDecl = auto()


@dataclass
class ExternDeclaration:
    kind: ExternDeclarationKind


class TopLevelStatementKind(Enum):
    ConstDef = auto()
    VarDecl = auto()
    VarDef = auto()
    FuncDecl = auto()
    FuncDef = auto()
    StructDecl = auto()
    StructDef = auto()
    UnionDecl = auto()
    UnionDef = auto()
    ExternDecl = auto()


class TopLevelStatement:
    pass


@dataclass
class Program:
    stmts = list[TopLevelStatement]


class BinOpNode:
    def __init__(self, oper: BinOpKind, left)

class Node:
    pass


class Parser:
    def __init__(self, tokens: list[Token], stop_at: Token):
        self.toks = Stream(tokens)
        self.stop_at = stop_at

    def parse(self) -> Node:
        return Node()