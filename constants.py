"""                                      -{ Project Name }-

Programmers: Joseph Coppin

Holds constant values that need to be accessed by various things.

Imports:                                                                                         """
import built_in


# the operators that can be used, and their associated built-in functions
operators = {
    '+': built_in.add,
    '-': built_in.subtract,
    '*': built_in.multiply,
    '/': built_in.divide,
}

built_in_functions = {
    'print': print,
    'add': built_in.add,
    'subtract': built_in.subtract,
    'multiply': built_in.multiply,
    'divide': built_in.divide,

}

# all character that can be in a variable name. Note that it can't start with a number,
# because it would get picked up by number detection first.
variable_characters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
    'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_'
]

'''                 code definitions                '''
# tags
open_tag = '['
tag_divider = ':'
close_tag = ']'
closing_tag_sign = '-'

ignore = [' ', '\n']

# data types
open_string = "'"
close_string = "'"

negative_sign = '-'
decimal_point = '.'

open_array = "("
close_array = ")"

# types of tags
function_declaration = 'func'
variable_declaration = 'var'
run_function = 'run'

open_comment = '[#]'
close_comment = '[-#]'

parameter_variable, reversed_parameter_name = 'param', 'marap'


# exceptions
class ParamError(NameError):
    """
    For if something is called 'param'. This can only be used in functions to represent the
    parameter the function takes in.
    """
    def __init__(self):
        super().__init__("Keyword 'param' must be used for function parameters only.")
