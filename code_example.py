from main import code

code('''
[#] 

This is some example code to show off features.

[-#]

[func:test_function]
    [run:print]
        param
    [-print]
[-test_function]

[var:message]
    -1234.5
[-message]

[run:test_function]
    message
[-test_function]

''', debug_lvl=0)
