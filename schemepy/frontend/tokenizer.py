"""
Scheme tokenizer, reads tokens from a stream and creates Scheme expressions.
"""
import re
from schemepy.frontend import syntaxerror


def _tokgen(regexp, stream):
    """
    Generates tokens from a stream.
    """
    text = ""
    while True:
        if not text:
            text = next(stream)
        token, text = re.match(regexp, text).groups()
        if token:
            yield token
        elif text:
            yield syntaxerror.SchemeSyntaxError(text)
            text = ""


class Tokenizer:
    """
    Scheme tokenizer.
    """
    __regexp = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''
    __quotes = {
        "'": "quote",
        "`": "quasiquote",
        ",": "unquote",
        ",@": "unquotesplicing",
        }

    def __init__(self, stream):
        self.__token_stream = _tokgen(Tokenizer.__regexp, stream)

    def tokenize(self):
        """
        Get the next expression.
        """
        def next_token():
            """
            Get next token.
            """
            token = next(self.__token_stream)
            try:
                raise token
            except TypeError:
                return token

        def read_token(token=None):
            """
            Handle a token.
            """
            if token is None:
                token = next_token()
            if token.startswith(";"):
                return read_token()
            elif token == "(":
                return read_list()
            elif token in Tokenizer.__quotes:
                return [Tokenizer.__quotes[token], read_token()]
            elif token == ")":
                raise syntaxerror.SchemeSyntaxError("Unexpected ')'")
            else:
                return token

        def read_list():
            """
            Handle list tokens.
            """
            tokens = []
            while True:
                token = next_token()
                if token == ")":
                    return tokens
                else:
                    tokens.append(read_token(token))

        return read_token()
