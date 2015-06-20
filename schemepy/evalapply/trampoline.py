"""
Tail call optimizer

Usage:
 * Decorate the function with @Trampoline
 * Wrap all tail calls with bounce

Example:
Original:
def fact(n, acc=1):
    if n <= 1:
        return acc
    else:
        return fact(n - 1, acc * n)

Tail call optimized:
@Trampoline  # This line is added.
def fact(n, acc=1):
    if n <= 1:
        return acc
    else:
        return bounce(fact)(n - 1, acc * n)  # This line is changed.
"""
from schemepy.evalapply import thunk


class Trampoline:
    def __init__(self, func):
        self.__func = func

    @property
    def func(self):
        return self.__func

    def __call__(self, *args, **kwargs):
        continuation = self.__func(*args, **kwargs)
        return thunk.unpack(continuation)


def bounce(call):
    def tail_call(*args, **kwargs):
        return thunk.Thunk(func, *args, **kwargs)

    func = call.func if isinstance(call, Trampoline) else call  # Do not bounce a trampoline.
    return tail_call
