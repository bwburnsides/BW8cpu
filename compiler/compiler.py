from pprint import pprint
from lex import Lexer
from parse import Parser


def main():
    with open("example.bw8") as f:
        contents = f.read()
    tokens = Lexer(contents).lex()
    ast = Parser(tokens).parse()
    pprint(ast)


if __name__ == "__main__":
    main()
