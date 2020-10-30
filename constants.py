"""                                      -{ Project Name }-

Programmers: Joseph Coppin

Holds constant values that need to be accessed by various things.

Imports:                                                                                         """
import built_in
import math

debug_level = 0


# the operators that can be used, and their associated built-in functions
operators = {
    '+': built_in.add,
    '-': built_in.subtract,
    '*': built_in.multiply,
    '/': built_in.divide,

    '=': built_in.check_equal,
    '!=': built_in.check_not_equal,
    'gt': built_in.check_greater_than,
    'lt': built_in.check_less_than,
    'gt=': built_in.check_greater_than_or_equal_to,
    'lt=': built_in.check_less_than_or_equal_to
}

built_in_functions = {
    # general
    'echo': print,
    'listen': input,
    'open': built_in.get_file,
    'range': built_in.get_range,

    # types
    'str': str,
    'num': float,
    'array': list,

    # maths
    'add': built_in.add,
    'subtract': built_in.subtract,
    'multiply': built_in.multiply,
    'divide': built_in.divide,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
}

# all character that can be in a variable name. Note that it can't start with a number,
# because it would get picked up by number detection first.
variable_characters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
    'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_'
]

built_in_variables = {
    'true': True,
    'false': False
}

'''                 code definitions                '''
# tags
open_tag = '<'
tag_divider = '|'
close_tag = '>'
closing_tag_sign = '/'

ignore = [' ', '\n']

# data types
open_string = "'"
close_string = "'"

negative_sign = '-'
decimal_point = '.'

open_array = "["
array_separator = ','
close_array = "]"

open_bracket = '('
close_bracket = ')'

# types of tags
function_declaration = 'func'
variable_declaration = 'var'
run_function = 'run'
import_declaration = 'import'
for_loop = 'for'
if_statement = 'if'
elif_statement = 'else'
else_statement = '________'
return_statement = 'return'

open_comment = '#'
close_comment = '/#'

parameter_variable, reversed_parameter_name = 'arg', 'gra'


# exceptions
class ParamError(NameError):
    """
    For if something is called 'param'. This can only be used in functions to represent the
    parameter the function takes in.
    """
    def __init__(self):
        super().__init__("Keyword 'param' must be used for function parameters only.")
