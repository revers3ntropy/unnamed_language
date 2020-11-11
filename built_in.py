"""                                    -{ Unnamed Language }-

Programmers: Joseph Coppin

Holds the functions that should be able to be run just by calling them in the script.
Some of these can be run using operators, like '+' and 'add', but all can be called using
[run:name] like a normal function.

Imports:                                                                                         """
# None


def to_string(message: any):
    """
    Makes some data a string
    """
    return str(message)


def add(values):
    """
    Returns the value of a + b. First checks that they are both numbers.
    """
    a = values[0]
    b = values[1]

    try:
        a = float(a)
    except TypeError:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except TypeError:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    return a + b


def subtract(values):
    """
    Returns the value of a - b. First checks that they are both numbers. Is sensitive to which
    way round the numbers are passed in.
    """
    a = values[0]
    b = values[1]

    try:
        a = float(a)
    except TypeError:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except TypeError:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    return a - b


def multiply(values):
    """
    Returns the value of a * b. First checks that they are both numbers.
    """
    a = values[0]
    b = values[1]

    try:
        a = float(a)
    except TypeError:
        raise ValueError(f"Can only multiply two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except TypeError:
        raise ValueError(f"Can only multiply two numbers, not '{a}' and '{b}'")

    return a * b


def divide(values):
    """
    Returns the value of a / b. First checks that they are both numbers. It sensitive to which
    way round they are passed in
    """
    a = values[0]
    b = values[1]

    try:
        a = float(a)
    except TypeError:
        raise ValueError(f"Can only divide two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except TypeError:
        raise ValueError(f"Can only divide two numbers, not '{a}' and '{b}'")

    return a / b


def check_equal(values):
    if values[0] == values[1]:
        return True
    return False


def check_not_equal(values):
    if values[0] != values[1]:
        return True
    return False


def check_greater_than(values):
    if values[0] > values[1]:
        return True
    return False


def check_less_than(values):
    if values[0] < values[1]:
        return True
    return False


def check_greater_than_or_equal_to(values):
    if values[0] >= values[1]:
        return True
    return False


def check_less_than_or_equal_to(values):
    if values[0] <= values[1]:
        return True
    return False


def get_file(file_name: str):

    file_data = ''
    with open(file_name) as file:
        for line in file:
            file_data += line

    return file_data


def get_file_csv(file_name: str):
    file_data = ''
    with open(file_name) as file:
        for line in file:
            file_data += line.split(',')

    return file_data


def get_range(number: float):

    try:
        float(number)
    except ValueError:
        raise ValueError(f"Cannot range {number}, must be a number")
    
    range_ = []

    for i in range(round(number)):
        range_.append(i)

    return range_


def get_element(args):
    if len(args) != 2:
        raise SyntaxError(f"get_element built-in function takes in 2 arguments, not {args}")

    array = args[0]
    index = round(args[1])
    return array[index]


def set_element(args):
    if len(args) != 3:
        raise SyntaxError(f"set _element built-in function takes in 3 arguments, not {args}")

    array = args[0]
    index = round(args[1])
    new = args[2]

    array[index] = new

    return array


def check_in(values):
    if values[0] in values[1]:
        return True
    return False


class StringManipulation:
    @staticmethod
    def concatenate_strings(values):
        final = ''
        for i in values:
            final += str(i)

        return final

    @staticmethod
    def lower_string(values):
        return str(values).lower()

    @staticmethod
    def upper_string(values):
        return str(values).upper()
