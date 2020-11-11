"""                                    -{ Unnamed Language }-

Programmers: Joseph Coppin

Holds some utility functions.

Imports:                                                                                         """
from typing import Union

import constants as c


def remove_char_word(word: Union[list, str], index: int):
    """
    Removes a character from a string at position 'index'.

    Parameters:  word - the word
                 index - the place in the word to be removed

    Returns:  the word with the character removed
    """
    word = list(word)
    word.pop(index)
    return ''.join(word)


def get_up_to_in(value: Union[str, list], search_for: str, inclusive: bool = True):
    """
    Returns a string of all the characters that come before the first instance of a set of chars
    in a string. EG. 'hello', 'l' --> 'hel' and 'hello world', 'or' --> 'hello wor'

    Parameters: char - the character to search for
                delete - whether or not the function should delete the characters it returns
                inclusive - whether or not the function should return the character it is
                            looking for or not
    """
    # make sure everything is a string, and that value contains the thing your looking for
    if type(value) == str:

        if search_for not in value:
            return value

    elif type(value) == list:
        value = ''.join(value)
        if search_for not in value:
            return value

    else:
        raise TypeError

    # splits the function at the first instance of the searching for string
    value = value.split(search_for)[0]

    # does the final character the loop misses out
    if inclusive:
        for i in range(len(search_for)):
            value += search_for[i]

    return value


def clear_whitespace(value: Union[str, list]):
    """
    Clears the whitespace at either end of the value
    """
    start_type = type(value)

    # make sure everything is a list, and that value contains the thing your looking for
    if start_type == str:
        value = list(value)

    elif start_type == list:
        pass

    else:
        raise TypeError(f"Can't clear whitespaces from {value}")

    if len(value) > 0:
        start = True
        while start:
            if value[0] in c.ignore:
                value.pop(0)
            else:
                start = False

    if len(value) > 0:
        end = True
        while end:
            if value[-1] in c.ignore:
                value.pop(-1)
            else:
                end = False

    if start_type == str:
        return ''.join(value)

    return value
