import logging
from schemepy.backend import procedures, basictypes
from schemepy.frontend import analyzer, tokenizer


def read(stream):
    token = tokenizer.Tokenizer(stream)

    def read_next():
        tokens = token.tokenize()
        logging.debug("Tokens: " + str(tokens))
        exp = analyzer.analyze(tokens)
        return exp

    return read_next


def disp(exp):
    printers = {
        str: lambda: exp,
        basictypes.Boolean: lambda: "#t" if exp.value else "#f",
        basictypes.Integer: lambda: str(exp.value),
        basictypes.Float: lambda: str(exp.value),
        basictypes.Complex: lambda: str(exp.value).replace("(", "").replace("j", "i").replace(")", ""),
        basictypes.Symbol: lambda: exp.value,
        basictypes.String: lambda: '"{}"'.format(exp.value),
        basictypes.Pair: lambda: "({} . {})".format(disp(exp.car), disp(exp.cdr)),
        basictypes.List: lambda: "(" + " ".join([disp(e) for e in exp]) + ")",
        procedures.Primitive: lambda: "#<primitive procedure>",
        procedures.Compound: lambda: "#<compound procedure>",
    }
    return printers[type(exp)]() if exp else ""
