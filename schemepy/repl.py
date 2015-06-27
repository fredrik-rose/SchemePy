"""
Read-eval-print loop.
"""
import logging
import sys
from schemepy.evalapply import evaluate, apply
from schemepy.frontend import inout, syntaxerror
from schemepy import environment, globalenvironment


def repl():
    """
    Read-eval-print loop.
    """
    def get_input():
        """
        Input generator.
        """
        while True:
            yield input("> ")

    print("Welcome to SchemePy!")
    env = globalenvironment.create()
    reader = inout.read(get_input())
    while True:
        try:
            exp = reader()
        except syntaxerror.SchemeSyntaxError as error:
            print("Syntax error: {}".format(error))
            continue
        logging.debug("Expression: %s", exp)
        try:
            evaluated_exp = evaluate.force_evaluate(exp, env)
        except environment.EnvError as error:
            print(error)
            continue
        except (evaluate.EvalError, apply.ApplyError) as error:
            print(error)
            sys.exit(-1)
        logging.debug("Environment:\n%s", env)
        print(inout.disp(evaluated_exp))
