class Thunk:
    def __init__(self, func, *args, **kwargs):
        self.__call = lambda: func(*args, **kwargs)

    def __call__(self):
        return self.__call()


def unpack(obj):
    while isinstance(obj, Thunk):
        obj = obj()
    return obj
