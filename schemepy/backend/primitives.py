"""
The primitives of the language.
"""
import functools
import inspect
import operator
from schemepy.backend import procedures, basictypes


TRUE = basictypes.Boolean(True)
FALSE = basictypes.Boolean(False)
NULL = basictypes.List([])


def _primitive(func):
    """
    Primitive function decorator.
    """
    def argument_checker(args, env):
        """
        Calls a primitive function with correct arguments.
        """
        num_of_args = len(inspect.getargspec(func).args)
        if num_of_args == 1:
            return func(args)
        elif num_of_args == 2:
            return func(args, env)
        else:
            raise TypeError("Primitive function not supported")

    return procedures.Primitive(argument_checker)


def _converter(func):
    """
    Scheme<->Python decorator.
    """
    def scheme2python(operands):
        """
        Converts a Scheme operand list to a Python operand list.
        """
        return [o.value for o in operands]

    def python2scheme(value):
        """
        Converts a Python value to a Scheme value.
        """
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
        """
        Scheme<->Python converter.

        Converts the Scheme operands to Python operands, applies the function
        and converts the result to a Scheme value.
        """
        operands = scheme2python(operands)
        result = func(operands, *args, **kwargs)
        return python2scheme(result)
    return convert


@_primitive
@_converter
def add(operands):
    """
    Addition primitive function.
    """
    return functools.reduce(operator.add, operands, 0)


@_primitive
@_converter
def sub(operands):
    """
    Subtraction primitive function.
    """
    return -operands[0] if len(operands) == 1 else functools.reduce(operator.sub, operands)


@_primitive
@_converter
def mul(operands):
    """
    Multiplication primitive function.
    """
    return functools.reduce(operator.mul, operands, 1)


@_primitive
@_converter
def div(operands):
    """
    Division primitive function.
    """
    return 1 / operands[0] if len(operands) == 1 else functools.reduce(operator.truediv, operands)


def _cmp(operands, func):
    """
    Reduces a list.
    """
    return all(func(operands[i], operands[i + 1]) for i in range(len(operands) - 1))


@_primitive
@_converter
def less(operands):
    """
    < primitive function.
    """
    return _cmp(operands, operator.lt)


@_primitive
@_converter
def less_or_equal(operands):
    """
    <= primitive function.
    """
    return _cmp(operands, operator.le)


@_primitive
@_converter
def equal(operands):
    """
    = primitive function.
    """
    return _cmp(operands, operator.eq)


@_primitive
@_converter
def not_equal(operands):
    """
    =/= primitive function.
    """
    return _cmp(operands, operator.ne)


@_primitive
@_converter
def greater_or_equal(operands):
    """
    >= primitive function.
    """
    return _cmp(operands, operator.ge)


@_primitive
@_converter
def greater(operands):
    """
    > primitive function.
    """
    return _cmp(operands, operator.gt)


@_primitive
def is_null(args):
    """
    Checks if the argument is null.
    """
    return basictypes.Boolean(isinstance(args[0], basictypes.List) and len(args[0].value) == 0)


@_primitive
def cons(args):
    """
    Inserts the first argument of args in the first position of the second
    argument of args if the second argument of args is a list, else creates a
    cons pair.
    """
    if isinstance(args[1], basictypes.List):
        return basictypes.List([args[0]] + args[1])
    else:
        return basictypes.Pair(args[0], args[1])


@_primitive
def car(args):
    """
    Get the first element.
    """
    if isinstance(args[0], basictypes.Pair):
        return args[0].car
    else:
        return args[0][0]


@_primitive
def cdr(args):
    """
    Get all elements except the first.
    """
    if isinstance(args[0], basictypes.Pair):
        return args[0].cdr
    else:
        return basictypes.List(args[0][1:])


@_primitive
def make_list(args):
    """
    Creates a list.
    """
    return basictypes.List(args)


@_primitive
def append(args):
    """
    Appends two lists.
    """
    return basictypes.List(args[0] + args[1])


@_primitive
def display(args):  # This is a hack
    """
    Displays a value.
    """
    from schemepy.frontend import inout
    print(inout.disp(args[0]))


@_primitive
def eval_primitive(args, env):  # This is a hack
    """
    Evaluates an expression in an environment.
    """
    def gen():
        """
        Input generator.
        """
        yield inout.disp(args[0])

    from schemepy.frontend import inout
    from schemepy.evalapply import evaluate
    exp = inout.read(gen())()
    return evaluate.evaluate(exp, env)


@_primitive
def apply_primitive(args, env):  # This is a hack
    """
    Applies a function on arguments.
    """
    from schemepy.evalapply import apply
    from schemepy.backend import expressions
    return apply.apply(args[0], [expressions.SelfEvaluating(a) for a in args[1]], env)
