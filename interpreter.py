"""                                      -{ EntropyTag }-

Programmers: Joseph Coppin

Holds the interpreter, which runs the code.

Imports:                                                                                         """
import util
from tag import Tag
from function import Function
import constants as c


class Interpreter:
    """
    Interprets the code and runs it in python.
    TODO: write tests for this

    Constructor:
        code_ - a long string of all the code to be run
        debug_lvl - how much debugging should take place:
                    0: normal
                    1: print values once per step
                    2: print multiple values per step, plus extra prints
                    3: don't call step function automatically + prints

    Functions:
        __get_up_to
        __interpret
        __step
        __set_value
        __run
        __tag
        __new_tag
        __remove_tag
        __remove_comment
        __assign
    """

    def __init__(self, code_: str, debug_lvl: int = 0):
        self.__debug = debug_lvl
        self.__code = list(code_)
        self.__tag_hierarchy = []
        self.__variables = {}
        self.__functions = {}

        self.__current_value = None

        if self.__debug < 3:
            self.__interpret()

    # -------------------------------------- util functions ---------------------------------------#

    def __get_up_to(self, search_for: str, delete: bool = True, inclusive: bool = True):
        """
        Returns a string of all the characters that come before the first instance of a character
        in the code. For example:

            self.__code = ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
            self.__get_up_to('o') == 'hello'

        Parameters: char - the character to search for
                    delete - whether or not the function should delete the characters it returns
                    inclusive - whether or not the function should return the character it is
                                looking for or not
        """
        value = util.get_up_to_in(self.__code, search_for, inclusive=inclusive)

        # puts back the characters if you don't want them to be deleted from self.__code
        if delete:
            for i in range(len(value)):
                self.__code.pop(0)

        return value

    # ---------------------------------------------------------------------------------------------#

    def __interpret(self):
        """
        Runs the interpreter on the code until the code has finished
        """

        while self.__code:
            self.__step()

    def __step(self):
        """
        Looks at the queue self.__code, and controls what happens given the current character.
        This character or more will then be deleted from the queue, leaving a new character.
        """
        char = self.__code[0]

        if self.__debug > 0:
            print(f"start: code: '{self.__code}'")
            print(f"start: functions: '{self.__functions}'")
            print(f"start: tags: '{self.__tag_hierarchy}'")

        if char == c.open_tag:
            self.__tag()

        elif char in c.ignore:
            self.__code.pop(0)

        else:
            self.__set_value()

        if self.__debug > 1:
            print(f"end: code: '{self.__code}'")
            print(f"end: functions: '{self.__functions}'")
            print(f"end: tags: '{self.__tag_hierarchy}'")

    def __set_value(self):
        """
        Goes through until it sees the start of a new tag, setting what it finds to
        self.__current_value. Generally is for parameters, variable assignment etc. Looks for types,
        for example ' for strings, or numbers for ints. Also controls operators, eg. 1 + 1.
        TODO: split this function
        """
        value = self.__get_up_to(c.open_tag)
        # makes it exclusive
        value = list(value[:-1])
        self.__code.insert(0, c.open_tag)

        while value:
            # deal with strings
            if value[0] == c.open_string:
                value.pop(0)
                string_value = util.get_up_to_in(''.join(value), c.close_string)
                # remove the string from the temporary queue 'value'
                for i in range(len(string_value)):
                    value.pop(0)
                self.__current_value = util.remove_char_word(string_value, -1)

            # for arrays
            if value[0] == c.open_array:
                value.pop(0)
                string_value = util.get_up_to_in(''.join(value), c.close_array)
                # remove the string from the temporary queue 'value'
                for i in range(len(string_value)):
                    value.pop(0)
                self.__current_value = util.remove_char_word(string_value, -1)

            # deal with whitespace
            elif value[0] in c.ignore:
                value.pop(0)

            else:
                try:
                    # deal with numbers

                    # deal with negative sign
                    if value[0] == c.negative_sign:
                        number = c.negative_sign
                        value.pop(0)
                    else:
                        float(value[0])
                        number = ''

                    go = True
                    while go:
                        # check for if there are no spaces between the var name and the next tag
                        if len(value) > 0:
                            if value[0] == c.decimal_point:
                                number += c.decimal_point
                                value.pop(0)
                            else:
                                try:
                                    # need to be separate because number is a string
                                    float(value[0])
                                    number += value[0]
                                    value.pop(0)
                                except:
                                    go = False
                        else:
                            go = False

                        try:
                            self.__current_value = float(number)
                        except KeyError:
                            raise NameError(f"Number '{number}' is not valid.")

                except:
                    # deal with operators
                    try:
                        print(value[10000])
                    except IndexError:
                        # try to get the whole variable name from the code
                        var_name = ''
                        go = True
                        while go:
                            # check for if there are no spaces between the var name and the next tag
                            if len(value) > 0:
                                if value[0] in c.variable_characters:
                                    var_name += value[0]
                                    value.pop(0)
                                else:
                                    go = False
                            else:
                                go = False

                        if var_name == '':
                            # variable name is not valid, and so there are no more options. Error
                            # called.
                            raise SyntaxError(f"Character '{value[0]}' not found.")
                        else:
                            # otherwise, the var name was valid, and a variable is retrieved and the
                            # program moves on. If no var of that name can be found, another error is
                            # called.
                            try:
                                self.__current_value = self.__variables[var_name]
                            except KeyError:
                                raise NameError(f"variable '{var_name}' could not be found.")

        if self.__debug:
            return self.__current_value

    def __run(self, function_name: str):
        """
        Runs a function. First checks for defined functions, then built in functions to run. This
        means that defined functions take priority of built in functions of the same name.

        Passes in self.__current_value to the function, which should have been set inside the run
        tags. If not, then None is passed through. All functions have exactly one parameter.

        To run a defined function, the contents of the function are simply added to self.__code to be
        be run.

        Any variable named 'param' in this is automatically replaced with the parameter of the
        function. This is static, so you can't change or assign to param, and if the variables
        which are included in the definition of param change, the value of param will not change
        with it.
        """
        try:
            function_code = self.__functions[function_name].get_contents()

            # removes instances of 'param' and replaces them with the passed in variable
            temp_code = ''.join(function_code)

            # keep the same type
            value_type = type(self.__current_value)
            if value_type == str:
                # the quotes have been taken away for strings
                to_pass_in = c.open_string + self.__current_value + c.close_string
            else:
                to_pass_in = self.__current_value

            # get the typed replacement value
            replacement = list(str(to_pass_in))
            replacement.reverse()
            replacement = ''.join(replacement)

            # 'marap' because the function code is reversed
            function_code = list(temp_code.replace(c.reversed_parameter_name, replacement))

            # add the new code to the current code
            for i in range(len(function_code)):
                self.__code.insert(0, function_code[i])

        except KeyError:  # the function has not been defined by the user
            try:
                # checks if the function is in the built-in functions, and if so then it runs it
                self.__current_value = c.built_in_functions[function_name](self.__current_value)

            except KeyError:
                raise NameError(f"Function '{function_name}' could not be found.")

    def __tag(self):
        """
        Controls tags.
        Called when a tag is detected. Controls whether or not it should add a new tag to the
        hierarchy, or delete an old one.
        """
        tag = self.__get_up_to(c.close_tag)
        if tag[1] == c.closing_tag_sign:
            self.__remove_tag(tag)
        else:
            self.__new_tag(tag)

    def __new_tag(self, tag: str):
        """
        Adds a new tag to the tag hierarchy. The tag added will be a bool with two elements:
        tag[0] == the type of tag,
        tag[1] == the contents of the tag.
        For example:
            ('run', 'print')
        would be a function running tag which runs the print function. The second element is the
        one which in the closing tag.

        Parameters:  tag - the name of the tag to add
        """
        if ''.join(tag[:len(c.open_comment)]) == c.open_comment:
            self.__remove_comment()
        else:

            tag_type = util.get_up_to_in(tag[1:], c.tag_divider, inclusive=False)

            # remove the hanging tag divider
            tag = util.remove_char_word(tag, 0)

            tag_value = tag[1 + len(tag_type):-1]

            if tag_type == c.function_declaration:
                # new function with the name given in the opening tag
                # NOTE: could be different to name given in closing tag, there are checks though
                self.__new_function(tag_value)
            else:
                # if your not declaring a function, then open a new tag.
                # A function tag is not opened because a Function object (which is added to
                # self.functions) needs the raw code, and opening a tag won't allow that
                self.__tag_hierarchy.append(Tag(tag_type, tag_value))

            # reset the current value whenever a new tag is opened
            self.__current_value = None

    def __remove_tag(self, tag: str):
        """
        Removes the last tag. Only does so if the last tag == the tag it is trying to remove, so
        you can only move up and down one tag at a time.

        Parameters:  tag - the name of the tag to remove
        """

        # some conditioning for the tag name coming in, as it is in the form [- * ]
        tag = tag[2:]
        tag = util.remove_char_word(tag, -1)

        # checks that the opening and closing tags are the same
        if self.__tag_hierarchy[-1].value == tag:
            tag_type = self.__tag_hierarchy[-1].type
            if tag_type == c.run_function:
                # run the function with the current value as the parameter
                self.__run(tag)

            elif tag_type == c.variable_declaration:
                # new variable with the name given in the opening tag
                # NOTE: could be different to name given in closing tag, there are checks tho
                self.__assign(self.__tag_hierarchy[-1].value)
            else:
                raise ValueError(
                    f"Tag type '{tag_type}' is invalid. \n  (in {self.__tag_hierarchy[-1]})")

            self.__tag_hierarchy.pop(-1)

        else:
            raise SyntaxError(f'Tag {self.__tag_hierarchy[-1].value} incorrectly closed with {tag}')

    def __remove_comment(self):
        """
        Called when a comment is detected, and the opening comment tag has been removed.
        This function removes the rest of the comment.
        """
        self.__get_up_to(c.close_comment)

    def __assign(self, var_name: str):
        """
        Creates a new variable with the given name, and the current value on the interpreter.
        """
        self.__variables[var_name] = self.__current_value

    def __new_function(self, func_name):
        """
        Creates a new function. Adds the contents of the program up until the close tag to the
        func_name index of self.functions. Each function takes in exactly one argument, param, which
        is automatically replaced with the value.
        """
        function_contents = self.__get_up_to(f"[-{func_name}]", inclusive=False)

        if self.__debug > 1:
            print(f"func '{func_name}' contains '{function_contents}'")
        elif self.__debug == 1:
            print(f"new function: '{func_name}'")

        # creates a new Function which is added to the current list of functions
        self.__functions[func_name] = Function(func_name, function_contents, functions=self.__functions)

        # clear up the remaining closing tag. +3 is needed because of the [- and ]
        for i in range(len(func_name) + 3):
            self.__code.pop(0)
