"""                                      -{ EntropyTag }-

Programmers: Joseph Coppin

Controls tags.

Imports:                                                                                         """
import constants


class Tag:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

        self.__check()

    def __check(self):
        """
        Checks that a tag is valid, checks the tags name is valid
        """

        if self.type == 'var':
            try:
                float(self.value[0])
                raise SyntaxError(
                    f"Variable cannot be defined as '{self.value}'. Name cannot start with "
                    f"a number.")
            except:
                for char in self.value:
                    if char not in constants.variable_characters:
                        raise SyntaxError(
                            f"Variable cannot be defined as '{self.value}'. Check that all "
                            f"characters are ether a letter, a number or an underscore."
                            )

            if self.value == 'param':
                raise constants.ParamError()
