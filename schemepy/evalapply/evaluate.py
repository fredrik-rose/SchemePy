""""
Generic evaluate.
"""
from schemepy.evalapply import thunk, trampoline


class EvalError(TypeError):
    """"
    Evaluate exception.
    """
    pass


@trampoline.Trampoline
def evaluate(exp, env):
    """
    Evaluates the expression in an environment.

    Tail call optimized.
    """
    if hasattr(exp, 'evaluate'):
        return exp.evaluate(env)
    else:
        raise EvalError("Unknown expression type.")


def tail_call_evaluate(exp, env):
    """
    Performs a tail call to evaluate.
    """
    return trampoline.bounce(evaluate)(exp, env)


def evaluate_sequence(seq, env):
    """
    Evaluates a sequence.
    """
    for exp in seq[:-1]:
        evaluate(exp, env)
    return tail_call_evaluate(seq[-1], env) if len(seq) > 0 else None


def force_evaluate(exp, env):
    """
    Evaluates an expression and forces eventual thunks.
    """
    return thunk.unpack(evaluate(exp, env))


def delay_evaluate(exp, env):
    """
    Delays a call to evaluate.
    """
    return thunk.Thunk(evaluate, exp, env)


def delay_memo_evaluate(exp, env):
    """
    Delays a call to evaluate (with memoization).
    """
    return thunk.ThunkMemo(evaluate, exp, env)
