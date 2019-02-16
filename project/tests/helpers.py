

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
