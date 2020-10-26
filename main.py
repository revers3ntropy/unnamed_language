"""                                      -{ EntropyTag }-

Programmers: Joseph Coppin

Controls the running and interpretation of the language.

Imports:                                                                                         """
from interpreter import Interpreter


def code(code_: str, debug_lvl: int = 0):
    """
    Runs the code passed through.
    """
    if debug_lvl > 1:
        print(f"debug level '{debug_lvl}'")

    Interpreter(code_, debug_lvl=debug_lvl)
