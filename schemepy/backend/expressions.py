import abc
from schemepy.evalapply import evaluate, apply
from schemepy.backend import procedures, basictypes


class Expression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, env):
        pass


class SelfEvaluating(Expression):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return "<SelfEvaluating {}>".format(self.__value)

    def evaluate(self, env):
        return self.__value


class Identifier(Expression):
    def __init__(self, identifier):
        self.__identifier = identifier

    def __str__(self):
        return "<Identifier {}>".format(self.__identifier)

    def evaluate(self, env):
        return env[self.__identifier]


class Quote(Expression):
    def __init__(self, quotation):
        self.__quotation = quotation

    def __str__(self):
        return "<Quote {}>".format(self.__quotation)

    def evaluate(self, env):
        return self.__quotation


class Definition(Expression):
    def __init__(self, identifier, value):
        self.__identifier = identifier
        self.__value = value

    def __str__(self):
        return "<Definition {} {}>".format(self.__identifier, self.__value)

    def evaluate(self, env):
        env.update({self.__identifier: evaluate.evaluate(self.__value, env)})
        return self.__identifier


class Assignment(Expression):
    def __init__(self, identifier, value):
        self.__identifier = identifier
        self.__value = value

    def __str__(self):
        return "<Assignment {} {}>".format(self.__identifier, self.__value)

    def evaluate(self, env):
        env[self.__identifier] = evaluate.evaluate(self.__value, env)
        return self.__identifier


class If(Expression):
    def __init__(self, predicate, consequent, alternative=None):
        self.__predicate = predicate
        self.__consequent = consequent
        self.__alternative = alternative

    def __str__(self):
        return "<If {} {} {}>".format(self.__predicate, self.__consequent, self.__alternative)

    def evaluate(self, env):
        predicate = evaluate.evaluate(self.__predicate, env)
        if not isinstance(predicate, basictypes.Boolean) or predicate.value:
            return evaluate.evaluate(self.__consequent, env)
        else:
            return evaluate.evaluate(self.__alternative, env) if self.__alternative else basictypes.Boolean(False)


class Lambda(Expression):
    def __init__(self, parameters, body):
        self.__parameters = parameters
        self.__body = body  # TODO: Handle internal definitions?

    def __str__(self):
        return "<Lambda {} {{body}}>".format(self.__parameters)

    def evaluate(self, env):
        return procedures.Compound(self.__parameters, self.__body, env)


class Begin(Expression):
    def __init__(self, sequence):
        self.__sequence = sequence

    def __str__(self):
        return "<Begin {sequence}>"

    def evaluate(self, env):
        return evaluate.evaluate_sequence(self.__sequence, env)


class Application(Expression):
    def __init__(self, operator, operands):
        self.__operator = operator
        self.__operands = operands

    def __str__(self):
        return "<Application {} {}>".format(self.__operator, [str(o) for o in self.__operands])

    def evaluate(self, env):
        return apply.apply(evaluate.evaluate(self.__operator, env), [evaluate.evaluate(o, env) for o in self.__operands])
