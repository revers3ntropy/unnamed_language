"""                                      -{ EntropyTag }-

Programmers: Joseph Coppin

Holds the interpreter, which runs the code.

Imports:                                                                                         """
import util
from tag import Tag
from function import Function
import constants as c

import time


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
        __get_value_from
        __set_value
        __run
        __tag
        __new_tag
        __remove_tag
        __remove_comment
        __assign
        __import
    """

    def __init__(self, code_: str):
        self.__code = list(code_)
        self.__tag_hierarchy = []
        self.__variables = {}
        self.__functions = {}

        self.__current_value = None

        if c.debug_level < 3:
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

        start_time = time.time()

        while self.__code:
            self.__step()

        print(f"\nRan code in {round(time.time() - start_time, 3)}s")

    def __step(self):
        """
        Looks at the queue self.__code, and controls what happens given the current character.
        This character or more will then be deleted from the queue, leaving a new character.
        """
        char = self.__code[0]

        if c.debug_level > 0:
            print(f"code: \n{''.join(self.__code)}\n\n")

        if ''.join(self.__code[:len(c.open_comment)]) == c.open_comment:
            self.__remove_comment()

        elif char == c.open_tag:
            self.__tag()

        elif char in c.ignore:
            self.__code.pop(0)

        else:
            self.__set_value()

    def __get_value_from(self, value: list):
        """
        Goes through a list of code and returns the final value of the code, accounting for type,
        variables, and operators. Very long function.
        """
        current_value = None
        while value:

            # deal with whitespace
            if value[0] in c.ignore:
                value.pop(0)
                
            elif value[0] == c.open_bracket:
                value.pop(0)
                # deal with brackets
                inside_bracket = util.get_up_to_in(value, c.close_bracket)

                for _ in inside_bracket:
                    value.pop(0)

                inside_bracket = util.remove_char_word(inside_bracket, -1)
                current_value = self.__get_value_from(list(inside_bracket))

            # deal with strings
            elif value[0] == c.open_string:
                value.pop(0)
                string_value = util.get_up_to_in(''.join(value), c.close_string)
                # remove the string from the temporary queue 'value'
                for i in range(len(string_value)):
                    value.pop(0)
                current_value = util.remove_char_word(string_value, -1)

            # for arrays
            elif value[0] == c.open_array:
                value.pop(0)
                array_value = util.get_up_to_in(''.join(value), c.close_array)
                # remove the string from the temporary queue 'value'
                for i in range(len(array_value)):
                    value.pop(0)
                array_value = util.remove_char_word(array_value, -1)
                array_value = array_value.split(c.array_separator)

                array = []
                for data in array_value:
                    # calls itself for each item in the array
                    data = self.__get_value_from(list(data))
                    array.append(data)

                current_value = array

            else:
                try:
                    # deals with numbers

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
                                except ValueError:
                                    go = False
                        else:
                            go = False

                        try:
                            current_value = float(number)
                        except KeyError:
                            raise NameError(f"Number '{number}' is not valid.")

                except ValueError:
                    # deal with operators
                    try:
                        operation = c.operators[value[0]]
                        value.pop(0)
                        current_value = operation([current_value, self.__get_value_from(value)])
                    except KeyError:
                        try:
                            operation = c.operators[value[0] + value[1]]
                            value.pop(0)
                            value.pop(0)
                            current_value = operation([current_value, self.__get_value_from(value)])
                        except KeyError:
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
                                raise SyntaxError(f"Character '{value[0]}' not found. In {''.join(value)}.")
                            else:
                                # otherwise, the var name was valid, and a variable is retrieved and the
                                # program moves on. If no var of that name can be found, another error is
                                # called.
                                try:
                                    current_value = c.built_in_variables[var_name]
                                except KeyError:
                                    try:
                                        current_value = self.__variables[var_name]
                                    except KeyError:
                                        raise NameError(f"variable '{var_name}' could not be found.")

        return current_value

    def __set_value(self):
        """
        Gets the value of the current code up until the next open tag, and sets that to
        __current_value.
        """
        value = self.__get_up_to(c.open_tag)
        # makes it exclusive
        value = list(value[:-1])
        self.__code.insert(0, c.open_tag)

        self.__current_value = self.__get_value_from(value)

    def __add_to_code(self, code: list, replace: str = None, with_: str = None):
        """
        Adds some code to the code queue.
        """

        """
        adds typing to the vars, as they are converted to a string when they are added but have
        lost their typing (eg. '' for strings)
        """
        if type(with_) == str:
            # the quotes have been taken away for strings
            new_value = c.open_string + with_ + c.close_string

        elif type(with_) == list:
            new_value = [c.open_array, c.close_array]
            for i in range(len(with_)):
                element = keep_type(with_[i])

                new_value.insert(-1, str(element))

                if i != len(with_) - 1:
                    new_value.insert(-1, c.array_separator)

            new_value = ''.join(new_value)

        else:
            new_value = with_

        # get the typed replacement value
        with_ = list(str(new_value))
        with_.reverse()
        with_ = ''.join(with_)

        code.reverse()
        code = ''.join(code)

        if replace is not None and with_ is not None:
            code = list(code.replace(replace, with_))

        # add the new code to the current code
        for i in range(len(code)):
            self.__code.insert(0, code[i])

    def __run(self, function_name: str):
        """
        Runs a function. First checks for defined functions, then built in functions to run. This
        means that defined functions take priority of built in functions of the same name.

        Passes in self.__current_value to the function, which should have been set inside the run
        tags. If not, then None is passed through. All functions have exactly one parameter.

        To run a defined function, the contents of the function are simply added to self.__code to be
        be run.

        Any variable called the dedicated parameter variable in this is automatically replaced with
        the parameter of the function. This is static, so you can't change or assign to param,
        and if the variables which are included in the definition of param change, the value of
        param will not change with it.
        """
        try:
            # slightly unreadable, basically takes the code in the function given by the name and
            # reversed it, then replaces all instances of the parameter name with the current value
            function = self.__functions[function_name]

            self.__add_to_code(c.open_tag + c.closing_tag_sign + function_name + c.close_tag)

            self.__add_to_code(function, replace=c.parameter_variable,
                               with_=self.__current_value)

            self.__tag_hierarchy.append(Tag(c.function_declaration, function_name))

        except KeyError:  # the function has not been defined by the user
            try:
                # checks if the function is in the built-in functions, and if so then it runs it
                self.__current_value = c.built_in_functions[function_name](self.__current_value)

            except KeyError:
                raise NameError(f"Function '{function_name}' could not be found.")

    def __for_loop(self, tag):
        """
        basically treats the code like a function, creates a new function called '__loop__' and
        then repeats it if the tag says it should go.
        """
        tag = util.remove_char_word(tag, -1)
        close_tag = c.open_tag + c.closing_tag_sign + c.for_loop + c.close_tag
        loop_code = self.__get_up_to(close_tag, inclusive=False)

        # clean up closing tag
        for i in range(len(close_tag)):
            self.__code.pop(0)

        tag_components = tag.split(c.tag_divider)
        if len(tag_components) != 3:
            raise SyntaxError(
                f"For loop must have three parts: for, variable declaration and array "
                f"to loop over")

        loop_var_name = tag_components[1]
        to_loop_over = self.__get_value_from(list(tag_components[2]))
        to_loop_over.reverse()

        # actual loop
        for value in to_loop_over:
            # adds the loop code to the code, replacing that variable
            self.__add_to_code(loop_code, replace=loop_var_name, with_=value)

    def __tag(self):
        """
        Controls tags.
        Called when a tag is detected. Controls whether or not it should add a new tag to the
        hierarchy, or delete an old one.
        """
        tag = self.__get_up_to(c.close_tag)
        if tag[len(c.open_tag)] == c.closing_tag_sign:
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

        tag_type = util.get_up_to_in(tag[1:], c.tag_divider, inclusive=False)

        # remove the hanging tag divider
        tag = util.remove_char_word(tag, 0)

        tag_value = tag[1 + len(tag_type):-1]

        if tag_type == c.function_declaration:
            # new function with the name given in the opening tag
            # NOTE: could be different to name given in closing tag, there are checks though
            self.__new_function(tag_value)
        elif tag_type == c.for_loop:
            # starts looping
            self.__for_loop(tag)
        elif tag_type == c.if_statement:
            # run the if statement
            self.__do_if(tag)
        elif tag[:-1] == c.import_declaration:
            # run the if statement
            self.__import_scripts()
        else:
            # if your not declaring a function, then open a new tag.
            # A function tag is not opened because a Function object (which is added to
            # self.functions) needs the raw code, and opening a tag won't allow that
            self.__tag_hierarchy.append(Tag(tag_type, tag_value))

        # reset the current value whenever a new tag is opened
        self.__current_value = None

    def __remove_tag(self, tag_: str):
        """
        Removes the last tag. Only does so if the last tag == the tag it is trying to remove, so
        you can only move up and down one tag at a time.

        Parameters:  tag - the name of the tag to remove
        """

        # some conditioning for the tag name coming in, as it is in the form [- * ]
        tag = tag_[2:]
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
            raise SyntaxError(f"Tag '{self.__tag_hierarchy[-1].value}' incorrectly closed with '{tag_}'")

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
        function_contents = self.__get_up_to(c.open_tag + c.closing_tag_sign + func_name +
                                             c.close_tag, inclusive=False)

        if c.debug_level > 1:
            print(f"func '{func_name}' contains '{function_contents}'")
        elif c.debug_level == 1:
            print(f"new function: '{func_name}'")

        # creates a new Function which is added to the current list of functions
        self.__functions[func_name] = Function(func_name, function_contents,
                                               functions=self.__functions)

        # clear the closing if tag
        for i in range(len(c.open_tag + c.closing_tag_sign + c.if_statement + c.close_tag)):
            self.__code.pop(0)

        # clear up the remaining closing tag. +3 is needed because of the surrounding tags
        # Note: this needs to be changed if tag declaration changes
        for i in range(len(func_name) + 3):
            self.__code.pop(0)

    def __do_if(self, tag):
        """
        runs an if statement. The tag argument is the front tag, which has already been removed
        from the queue
        """
        if util.get_up_to_in(tag, c.tag_divider, inclusive=False) != c.if_statement:
            raise SyntaxError(f"Cannot open if statement with tag {tag}.")

        condition = tag[len(c.if_statement) + 1: -1]

        # get the condition and the code to run
        condition = self.__get_value_from(list(condition))
        code = self.__get_up_to(c.open_tag + c.closing_tag_sign + c.if_statement + c.close_tag,
                                inclusive=False)

        # clear the end if tag
        for _ in range(len(c.open_tag + c.closing_tag_sign + c.if_statement + c.close_tag)):
            self.__code.pop(0)

        if condition not in (True, False):
            raise TypeError(f"If condition must be of type bool, cannot be {condition}")

        # get the code from the if statement to the next 'else' statement
        while code:
            code_to_run = util.get_up_to_in(code, c.open_tag + c.elif_statement + c.tag_divider)

            # remove the code that has just been run
            for _ in code_to_run:
                code = util.remove_char_word(code, 0)

            # actual if statement
            if condition:
                self.__add_to_code(list(code_to_run))
                code = []

            # checks if it is not already at the end
            if len(code) > 0:
                # get the condition of the next elif statement. The elif thing and the tag divider
                # have already been removed for this, so just need to get up to the end of the tag
                condition = util.get_up_to_in(code, c.close_tag)

                # clear the condition
                for _ in condition:
                    code = util.remove_char_word(code, 0)

                # remove hanging tag closer
                condition = util.remove_char_word(condition, -1)
                condition = self.__get_value_from(list(condition))

                if condition not in (True, False):
                    raise TypeError(f"If condition must be of type bool, cannot be {condition}")

    def __import_scripts(self):
        """
        Called inside the import tags.
        The import function takes in a list of strings.
        Goes through each item in the list, and adds the code from that .txt file to the code.
        """
        imports = self.__get_up_to(c.open_tag + c.closing_tag_sign + c.import_declaration +
                                   c.close_tag, inclusive=False)

        # clear closing tag
        for _ in range(len(c.open_tag + c.closing_tag_sign + c.import_declaration +
                           c.close_tag)):
            self.__code.pop(0)

        # turn it into a list
        imports = self.__get_value_from(list(imports))

        if type(imports) != list:
            raise TypeError(f"Import takes an array of string. Cannot be {imports}, of type "
                            f"{type(imports)}")

        for name in imports:
            try:
                with open(f'{name}.txt') as code:
                    # turn it into a string, rather than a file object
                    code_ = ''
                    for line in code:
                        code_ += line

                    self.__add_to_code(list(code_))
            except:
                raise ImportError(f"Could not import {name}. Make sure the .txt file exists")

    def do_return(self):
        pass
