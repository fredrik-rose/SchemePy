class ApplyError(TypeError):
    pass


def apply(procedure, arguments, env):
    if hasattr(procedure, 'apply'):
        return procedure.apply(arguments, env)
    else:
        raise ApplyError("Unknown application type.")
