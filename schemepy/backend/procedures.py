import abc
from schemepy.evalapply import evaluate


class Procedure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, arguments):
        pass


class Primitive(Procedure):
    def __init__(self, function):
        assert callable(function)
        self.__function = function

    def __str__(self):
        return "<Primitive procedure>"

    def apply(self, arguments):
        return self.__function(arguments)


class Compound(Procedure):
    def __init__(self, parameters, body, env):
        self.__parameters = parameters
        self.__body = body
        self.__env = env

    def __str__(self):
        return "<Compound procedure {} {{body}} {{environment}}>".format([str(p) for p in self.__parameters])

    def apply(self, arguments):
        env = self.__env.extend(self.__parameters, arguments)
        return evaluate.evaluate_sequence(self.__body, env)
