from schemepy.evalapply import trampoline


class EvalError(TypeError):
    pass


@trampoline.Trampoline
def evaluate(exp, env):
    if hasattr(exp, 'evaluate'):
        return exp.evaluate(env)
    else:
        raise EvalError("Unknown expression type.")


def tail_call_evaluate(exp, env):
    return trampoline.bounce(evaluate)(exp, env)


def evaluate_sequence(seq, env):
    for exp in seq[:-1]:
        evaluate(exp, env)
    return tail_call_evaluate(seq[-1], env) if len(seq) > 0 else None
