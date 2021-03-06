import os
import sys


def set_python_env():

    MODULE_FOLDER = os.path.join(os.path.split(
        os.path.dirname(__file__))[0], 'befunge')
    print(MODULE_FOLDER)

    if MODULE_FOLDER not in sys.path:
        sys.path.append(MODULE_FOLDER)


def convert_list_to_chars(l):

    def _covert_to_char(o):

        if type(o) is str:
            return o
        elif type(o) is int:
            return str(o)
        elif type(o) is list:
            return [_covert_to_char(i) for i in o]
        else:
            return TypeError('o is ' + type(o))

    return _covert_to_char(l)
