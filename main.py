"""                                      -{ EntropyTag }-

Programmers: Joseph Coppin

Controls the running and interpretation of the language.

Imports:                                                                                         """
from interpreter import Interpreter


def main():
    with open('main.txt') as program:
        code_ = ''
        for line in program:
            code_ += line
        code(code_)


def code(code_: str):
    """
    Runs the code passed through.
    """
    Interpreter(code_)


if __name__ == '__main__':
    main()
