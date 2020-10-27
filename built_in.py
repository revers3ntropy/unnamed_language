"""                                      -{ Project Name }-

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


def add(a: float, b: float):
    """
    Returns the value of a + b. First checks that they are both numbers.
    """
    try:
        a = float(a)
    except:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    return a + b


def subtract(a: float, b: float):
    """
    Returns the value of a - b. First checks that they are both numbers. Is sensitive to which
    way round the numbers are passed in.
    """
    try:
        a = float(a)
    except:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except:
        raise ValueError(f"Can only take away two numbers, not '{a}' and '{b}'")

    return a - b


def multiply(a: float, b: float):
    """
    Returns the value of a * b. First checks that they are both numbers.
    """
    try:
        a = float(a)
    except:
        raise ValueError(f"Can only multiply two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except:
        raise ValueError(f"Can only multiply two numbers, not '{a}' and '{b}'")

    return a * b


def divide(a: float, b: float):
    """
    Returns the value of a / b. First checks that they are both numbers. It sensitive to which
    way round they are passed in
    """
    try:
        a = float(a)
    except:
        raise ValueError(f"Can only divide two numbers, not '{a}' and '{b}'")

    try:
        b = float(b)
    except:
        raise ValueError(f"Can only divide two numbers, not '{a}' and '{b}'")

    return a / b


def get_file(file_name: str):

    file_data = ''
    with open(file_name) as file:
        for line in file:
            file_data += line

    return file_data
