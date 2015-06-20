class ApplyError(TypeError):
    pass


def apply(procedure, arguments):
    if hasattr(procedure, 'apply'):
        return procedure.apply(arguments)
    else:
        raise ApplyError("Unknown application type.")
