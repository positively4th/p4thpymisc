

def items(o, sort=False, str_as_vector=False):
    if str_as_vector or not isinstance(o, str):
        try:
            return sorted(o.items()) if sort else o.items()
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        try:
            return enumerate(sorted(o) if sort else o)
        except TypeError as e:
            pass
        try:
            return enumerate(o)
        except TypeError as e:
            pass

    return {None: o}.items()
