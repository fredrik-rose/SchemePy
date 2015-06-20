class EvalError(TypeError):
    pass


def evaluate(exp, env):
    if hasattr(exp, 'evaluate'):
        return exp.evaluate(env)
    else:
        raise EvalError("Unknown expression type.")


def evaluate_sequence(seq, env):
    result = None
    for exp in seq:
        result = evaluate(exp, env)
    return result
