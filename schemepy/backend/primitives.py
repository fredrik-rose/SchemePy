import functools
import operator
from schemepy.backend import procedures, basictypes


TRUE = basictypes.Boolean(True)
FALSE = basictypes.Boolean(False)
NULL = basictypes.List([])


def _converter(func):
    def scheme2python(operands):
        return [o.value for o in operands]

    def python2scheme(value):
        if isinstance(value, bool):
            return basictypes.Boolean(value)
        elif isinstance(value, int):
            return basictypes.Integer(value)
        elif isinstance(value, float):
            return basictypes.Float(value)
        elif isinstance(value, complex):
            return basictypes.Complex(value)
        elif isinstance(value, str):
            return basictypes.String(value)
        else:
            raise ValueError("Could not convert Python value to Scheme value")

    def convert(operands, *args, **kwargs):
        operands = scheme2python(operands)
        result = func(operands, *args, **kwargs)
        return python2scheme(result)
    return convert


@procedures.Primitive
@_converter
def add(operands):
    return functools.reduce(operator.add, operands, 0)


@procedures.Primitive
@_converter
def sub(operands):
    return -operands[0] if len(operands) == 1 else functools.reduce(operator.sub, operands)


@procedures.Primitive
@_converter
def mul(operands):
    return functools.reduce(operator.mul, operands, 1)


@procedures.Primitive
@_converter
def div(operands):
    return 1 / operands[0] if len(operands) == 1 else functools.reduce(operator.truediv, operands)


def _cmp(operands, func):
    return all(func(operands[i], operands[i + 1]) for i in range(len(operands) - 1))


@procedures.Primitive
@_converter
def less(operands):
    return _cmp(operands, operator.lt)


@procedures.Primitive
@_converter
def less_or_equal(operands):
    return _cmp(operands, operator.le)


@procedures.Primitive
@_converter
def equal(operands):
    return _cmp(operands, operator.eq)


@procedures.Primitive
@_converter
def not_equal(operands):
    return _cmp(operands, operator.ne)


@procedures.Primitive
@_converter
def greater_or_equal(operands):
    return _cmp(operands, operator.ge)


@procedures.Primitive
@_converter
def greater(operands):
    return _cmp(operands, operator.gt)


@procedures.Primitive
def is_null(args):
    return basictypes.Boolean(isinstance(args[0], basictypes.List) and len(args[0].value) == 0)


@procedures.Primitive
def cons(args):
    if isinstance(args[1], basictypes.List):
        return basictypes.List([args[0]] + args[1])
    else:
        return basictypes.Pair(args[0], args[1])


@procedures.Primitive
def car(args):
    if isinstance(args[0], basictypes.Pair):
        return args[0].car
    else:
        return args[0][0]


@procedures.Primitive
def cdr(args):
    if isinstance(args[0], basictypes.Pair):
        return args[0].cdr
    else:
        return basictypes.List(args[0][1:])


@procedures.Primitive
def make_list(args):
    return basictypes.List(args)


@procedures.Primitive
def append(args):
    return basictypes.List(args[0] + args[1])


@procedures.Primitive
def display(args):  # This is a hack
    from schemepy.frontend import inout
    print(inout.disp(args[0]))
