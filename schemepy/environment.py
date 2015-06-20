class EnvError(Exception):
    pass


class Environment:
    def __init__(self, identifiers=(), values=(), outer=None):
        if not len(identifiers) == len(values):
            raise EnvError("The number of identifiers ({}) do not match the number of values ({})."
                           .format(len(identifiers), len(values)))
        self.__symbol_table = dict(zip(identifiers, values))
        self.__outer = outer

    def __getitem__(self, identifier):
        if identifier in self.__symbol_table:
            return self.__symbol_table[identifier]
        elif self.__outer:
            return self.__outer[identifier]
        else:
            raise EnvError("Undefined identifier: {}".format(identifier))

    def __setitem__(self, identifier, value):
        if identifier in self.__symbol_table:
            self.__symbol_table[identifier] = value
        elif self.__outer:
            self.__outer[identifier] = value
        else:
            raise EnvError("Undefined identifier: {}".format(identifier))

    def __str__(self):
        border = "+{0:-<78}+\n".format("")
        header = "|{:^78}|\n".format("Environment frame")
        rows = "".join(["|{0:>20.20} : {1:<55.55}|\n".format(str(identifier), str(value))
                        for identifier, value in self.__symbol_table.items()])
        arrow = (("{0:>39}\n" * 3) + "{1:>39}\n").format("|", "V")
        outer_frame = arrow + str(self.__outer) if self.__outer else ""
        return border + header + border + rows + border + outer_frame

    def update(self, bindings):
        self.__symbol_table.update(bindings)

    def extend(self, identifiers=(), values=()):
        return Environment(identifiers, values, self)
