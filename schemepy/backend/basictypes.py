"""
The basic types of the language.
"""
import abc


class BasicType(metaclass=abc.ABCMeta):
    """"
    Basic type abstract base class.
    """
    @abc.abstractproperty
    def value(self):
        """"
        Get the value of the type.
        """
        pass


class Boolean(BasicType):
    """"
    Boolean basic type.
    """
    def __init__(self, value):
        assert isinstance(value, bool)
        self.__value = value

    def __str__(self):
        return "<Boolean {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Integer(BasicType):
    """"
    Integer basic type.
    """
    def __init__(self, value):
        assert isinstance(value, int)
        self.__value = value

    def __str__(self):
        return "<Integer {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Float(BasicType):
    """"
    Float basic type.
    """
    def __init__(self, value):
        assert isinstance(value, float)
        self.__value = value

    def __str__(self):
        return "<Float {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Complex(BasicType):
    """"
    Complex basic type.
    """
    def __init__(self, value):
        assert isinstance(value, complex)
        self.__value = value

    def __str__(self):
        return "<Complex {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Symbol(BasicType):
    """"
    Symbol basic type.
    """
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def __str__(self):
        return "<Symbol {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class String(BasicType):
    """"
    String basic type.
    """
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def __str__(self):
        return "<String {}>".format(self.__value)

    @property
    def value(self):
        return self.__value


class Pair(BasicType):
    """"
    Pair basic type.
    """
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
        """
        Get first value.
        """
        return self.__car

    @property
    def cdr(self):
        """
        Get second value.
        """
        return self.__cdr


class List(BasicType, list):
    """"
    List basic type.
    """
    def __str__(self):
        return "<List {}>".format([str(e) for e in self])

    @property
    def value(self):
        return self
