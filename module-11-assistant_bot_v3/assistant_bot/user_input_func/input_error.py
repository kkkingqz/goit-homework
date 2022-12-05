def input_error(func):
    def inner(string):
        try:
            ret = func(string)
            return ret
        except (KeyError, ValueError, IndexError) as err:
            if func.__name__ in ('change', 'phone', 'show', 'remove', 'birthday'):
                return 'record not found'
            return err
    return inner