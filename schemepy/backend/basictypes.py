import abc


class BasicType(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def value(self):
        pass


class Boolean(BasicType):
    def __init__(self, value):
        assert isinstance(value, bool)
        self.__value = value

    def __str__(self):
        return "<Boolean {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Integer(BasicType):
    def __init__(self, value):
        assert isinstance(value, int)
        self.__value = value

    def __str__(self):
        return "<Integer {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Float(BasicType):
    def __init__(self, value):
        assert isinstance(value, float)
        self.__value = value

    def __str__(self):
        return "<Float {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Complex(BasicType):
    def __init__(self, value):
        assert isinstance(value, complex)
        self.__value = value

    def __str__(self):
        return "<Complex {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Symbol(BasicType):
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def __str__(self):
        return "<Symbol {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class String(BasicType):
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def __str__(self):
        return "<String {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Pair(BasicType):
    def __init__(self, car, cdr):
        self.__car = car
        self.__cdr = cdr

    def __str__(self):
        return "<Pair {} {}>".format(self.__car, self.__cdr)

    @property
    def value(self):
        return [self.__car, self.__cdr]

    @property
    def car(self):
        return self.__car

    @property
    def cdr(self):
        return self.__cdr


class List(BasicType, list):
    def __str__(self):
        return "<List {}>".format([str(e) for e in self])

    @property
    def value(self):
        return self
