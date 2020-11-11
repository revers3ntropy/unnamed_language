"""                                    -{ Unnamed Language }-

Programmers: Joseph Coppin

Holds a function object.

Imports:                                                                                         """
# None


class Function:
    """
    Is a function. Contains the name of the function and the script the function should run when
    called.
      
    Constructor:
        name - the name of the function, what is referenced to call it
        contents - the raw contents of the function, in a string

    Functions:
        None
    """
    def __init__(self, name: str, contents: str, functions: dict = None):
        if functions is None:
            self.functions = {}
        else:
            self.functions = functions

        self.name = name
        self.contents = contents

        self.__check()

    def get_contents(self):
        """
        returns the contents of the function ready for adding to the main code. First lists the
        contents, as it comes in raw as a string, and then reverses it, because the individual parts
        of the code are added backwards, leading to a normal facing code at the front of the script.

        Called by the interpreter when interpreting a function call.
        """
        code_as_list = list(self.contents)
        code_as_list.reverse()
        return code_as_list

    def __check(self):
        """
        Checks that the function name is valid, for example that it is unique and the naming follows
        the rules.
        """
        try:
            # test if the function name is contained in the list of functions
            test = self.functions[self.name]
            raise SyntaxError(f"Cannot create two functions of the same name: '{self.name}'")
        except:
            pass
