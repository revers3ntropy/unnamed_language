"""                                      -{ Project Name }-

Programmers: Joseph Coppin

Holds some utility functions.

Imports:                                                                                         """
from typing import Union


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
    # make sure everything is a list, and that value contains the thing your looking for
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
