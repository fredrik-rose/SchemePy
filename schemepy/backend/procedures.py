"""
The procedures of the language.
"""
import abc
from schemepy.evalapply import evaluate


class Procedure(metaclass=abc.ABCMeta):
    """"
    Procedure abstract base class.
    """
    @abc.abstractmethod
    def apply(self, arguments, env):
        """
        Applies a function on arguments.
        """
        pass


class Parameter:
    """"
    Parameter base class.
    """
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """
        Get parameter name.
        """
        return self._name


class Strict(Parameter):
    """"
    Strict parameter type.
    """
    def __str__(self):
        return "<Strict {}>".format(self._name)

    @staticmethod
    def evaluate(exp, env):
        """
        Evaluates the expression.
        """
        return evaluate.force_evaluate(exp, env)


class Lazy(Parameter):
    """"
    Lazy parameter type.
    """
    def __str__(self):
        return "<Lazy {}>".format(self._name)

    @staticmethod
    def evaluate(exp, env):
        """
        Delays the evaluation.
        """
        return evaluate.delay_evaluate(exp, env)


class LazyMemo(Parameter):
    """"
    Lazy (with memoization) parameter type.
    """
    def __str__(self):
        return "<LazyMemo {}>".format(self._name)

    @staticmethod
    def evaluate(exp, env):
        """
        Delays the evaluation (with memoization).
        """
        return evaluate.delay_memo_evaluate(exp, env)


class Primitive(Procedure):
    """
    Primitive procedure.
    """
    def __init__(self, function):
        assert callable(function)
        self.__function = function

    def __str__(self):
        return "<Primitive procedure>"

    def apply(self, arguments, env):
        return self.__function([evaluate.force_evaluate(a, env) for a in arguments], env)


class Compound(Procedure):
    """
    Compound procedure.
    """
    def __init__(self, parameters, body, env):
        self.__parameters = parameters
        self.__parameter_names = [p.name for p in parameters]
        self.__body = body
        self.__env = env

    def __str__(self):
        return "<Compound procedure {} {{body}} {{environment}}>"\
            .format([str(p) for p in self.__parameters])


    def apply(self, arguments, env):
        new_env = self.__env.extend(self.__parameter_names,
                                    [p.evaluate(a, env)
                                     for p, a in zip(self.__parameters, arguments)])
        return evaluate.evaluate_sequence(self.__body, new_env)
