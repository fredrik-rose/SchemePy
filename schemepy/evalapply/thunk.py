class Thunk:
    def __init__(self, func, *args, **kwargs):
        self._call = lambda: func(*args, **kwargs)

    def __call__(self):
        return self._call()


class ThunkMemo(Thunk):
    def __init__(self, func, *args, **kwargs):
        self.__evaluated = False
        self.__memo = None
        super().__init__(func, *args, **kwargs)

    def __call__(self):
        if not self.__evaluated:
            self.__memo = self._call()
            del self._call
            self.__evaluated = True
        return self.__memo


def unpack(obj):
    while isinstance(obj, Thunk):
        obj = obj()
    return obj
