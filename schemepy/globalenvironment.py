"""
The global environment, contain bindings for primitives.
"""
from schemepy.backend import primitives
from schemepy import environment


def create():
    """
    Creates a global environment.
    """
    env = environment.Environment()
    env.update({
        '#t': primitives.TRUE,
        '#f': primitives.FALSE,
        'null': primitives.NULL,
        '+': primitives.add,
        '-': primitives.sub,
        '*': primitives.mul,
        '/': primitives.div,
        '<': primitives.less,
        '<=': primitives.less_or_equal,
        '=': primitives.equal,
        '!=': primitives.not_equal,
        '>=': primitives.greater_or_equal,
        '>': primitives.greater,
        'null?': primitives.is_null,
        'cons': primitives.cons,
        'car': primitives.car,
        'cdr': primitives.cdr,
        'list': primitives.make_list,
        'append': primitives.append,
        'display': primitives.display,
        'eval': primitives.eval_primitive,
        'apply': primitives.apply_primitive,
        })
    return env
