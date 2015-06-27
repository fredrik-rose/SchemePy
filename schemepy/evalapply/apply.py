""""
Generic apply.
"""
class ApplyError(TypeError):
    """"
    Apply exception.
    """
    pass


def apply(procedure, arguments, env):
    """
    Applies a procedure on arguments.
    """
    if hasattr(procedure, 'apply'):
        return procedure.apply(arguments, env)
    else:
        raise ApplyError("Unknown application type.")
