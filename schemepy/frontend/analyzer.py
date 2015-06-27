"""
Parse Scheme tokenized expressions and create backend objects.
"""
from schemepy.backend import basictypes, expressions, procedures
from schemepy.frontend import syntaxerror


class _AnalyzeTypeError(TypeError):
    """
    Analyze exception.
    """
    pass


def _to_basic_type(exp):
    """
    Creates a basic type.
    """
    def to_string():
        """
        Creates a string basic type.
        """
        if len(exp) >= 2 and exp[0] == '"' and exp[-1] == '"':
            return basictypes.String(exp[1:-1])
        raise _AnalyzeTypeError

    def to_number():
        """
        Creates a number basic type.
        """
        try:
            value = int(exp)
            return basictypes.Integer(value)
        except ValueError:
            pass
        try:
            value = float(exp)
            return basictypes.Float(value)
        except ValueError:
            pass
        try:
            value = complex(exp.replace('j', 'x').replace('i', 'j', 1))
            return basictypes.Complex(value)
        except ValueError:
            pass
        raise _AnalyzeTypeError

    if isinstance(exp, str):
        try:
            return to_string()
        except _AnalyzeTypeError:
            pass
        try:
            return to_number()
        except _AnalyzeTypeError:
            pass
    raise _AnalyzeTypeError


def _is_identifier(exp):
    """
    Checks if the expression is an identifier.
    """
    if isinstance(exp, str):
        try:
            _to_basic_type(exp)
        except _AnalyzeTypeError:
            return True
    return False


def _self_evaluating(exp):
    """
    Creates a self evaluating expression.
    """
    try:
        basic_type = _to_basic_type(exp)
        return expressions.SelfEvaluating(basic_type)
    except _AnalyzeTypeError:
        raise


def _identifier(exp):
    """
    Creates an identifier expression.
    """
    if _is_identifier(exp):
        return expressions.Identifier(exp)
    raise _AnalyzeTypeError


def _analyze_quote(exp):  # TODO: Handle other kind of quotes
    """
    Creates a quote expression.
    """
    def quote_quotation():
        """
        Get the quote part.
        """
        return exp[0]

    def analyze_quotation(quotation):
        """
        Analyze the quote.
        """
        if isinstance(quotation, list):
            if len(quotation) == 3 and quotation[1] == '.':
                return basictypes.Pair(analyze_quotation(quotation[0]),
                                       analyze_quotation(quotation[2]))
            else:
                return basictypes.List([analyze_quotation(q) for q in quotation])
        else:
            try:
                return _to_basic_type(quotation)
            except _AnalyzeTypeError:
                return basictypes.Symbol(quotation)

    if len(exp) != 1:
        raise syntaxerror.SchemeSyntaxError("quote: 1 part expected, {} is given.".format(len(exp)))
    return expressions.Quote(analyze_quotation(quote_quotation()))


def _analyze_set(exp):
    """
    Creates an assignment expression.
    """
    def set_identifier():
        """
        Get the identifier part.
        """
        return exp[0]

    def set_value():
        """
        Get the value part.
        """
        return exp[1]

    if len(exp) != 2:
        raise syntaxerror.SchemeSyntaxError("set!: 2 parts expected, {} is given.".format(len(exp)))
    if not _is_identifier(set_identifier()):
        raise syntaxerror.SchemeSyntaxError("set!: Not an identifier.")
    return expressions.Assignment(set_identifier(), analyze(set_value()))


def _analyze_define(exp):
    """
    Creates a definition expression.
    """
    def define_identifier():
        """
        Get the identifier part.
        """
        if isinstance(exp[0], list):
            if len(exp[0]) == 0:
                raise syntaxerror.SchemeSyntaxError("define: No identifier in procedure definition.")
            return exp[0][0]
        else:
            return exp[0]

    def define_value():
        """
        Get and analyze the value part.
        """
        if isinstance(exp[0], list):
            return _analyze_lambda([exp[0][1:]] + exp[1:])
        else:
            return analyze(exp[1])

    if len(exp) < 2:
        raise syntaxerror.SchemeSyntaxError("define: At least 2 parts expected, {} is given."
                                            .format(len(exp)))
    if not _is_identifier(define_identifier()):
        raise syntaxerror.SchemeSyntaxError("define: Not an identifier.")
    return expressions.Definition(define_identifier(), define_value())


def _analyze_if(exp):
    """
    Creates a if expression.
    """
    def if_predicate():
        """
        Get the predicate part.
        """
        return exp[0]

    def if_consequent():
        """
        Get the consequent part.
        """
        return exp[1]

    def if_alternative():
        """
        Get the alternative part.
        """
        return exp[2]

    if not 2 <= len(exp) <= 3:
        raise syntaxerror.SchemeSyntaxError("if: 2 or 3 parts expected, {} is given."
                                            .format(len(exp)))
    return expressions.If(analyze(if_predicate()),
                          analyze(if_consequent()),
                          analyze(if_alternative()) if len(exp) == 3 else None)


def _analyze_lambda(exp):
    """
    Creates a lambda expression.
    """
    def lambda_parameters():
        """
        Get the parameters part.
        """
        return exp[0]

    def lambda_body():
        """
        Get the body part.
        """
        return exp[1:]

    def parameter_identifier(param):
        """
        Get the identifier part of a parameter.
        """
        return param[0]

    def parameter_type(param):
        """
        Get the type part of a parameter.
        """
        return param[1]

    def analyze_parameter(param):
        """
        Analyze a parameter.
        """
        strict = 's'
        lazy = 'l'
        lazy_memo = 'm'
        types = {
            strict: procedures.Strict,
            lazy: procedures.Lazy,
            lazy_memo: procedures.LazyMemo,
        }
        if not isinstance(param, list):
            param = [param, strict]
        if len(param) != 2:
            raise syntaxerror.SchemeSyntaxError("lambda: Error in parameter declaration.")
        if not _is_identifier(parameter_identifier(param)):
            raise syntaxerror.SchemeSyntaxError("lambda: Parameter is not an identifier.")
        try:
            return types[parameter_type(param)](parameter_identifier(param))
        except KeyError:
            raise syntaxerror.SchemeSyntaxError("lambda: Unknown parameter type.")

    if len(exp) < 2:
        raise syntaxerror.SchemeSyntaxError("lambda: At least 2 parts expected, {} is given."
                                            .format(len(exp)))
    if not isinstance(lambda_parameters(), list):
        raise syntaxerror.SchemeSyntaxError("lambda: Error in parameter declaration.")
    return expressions.Lambda([analyze_parameter(p) for p in lambda_parameters()],
                              [analyze(e) for e in lambda_body()])


def _analyze_begin(exp):
    """
    Creates a begin expression.
    """
    def begin_sequence():
        """
        Get the sequence part.
        """
        return exp

    return expressions.Begin([analyze(e) for e in begin_sequence()])


def _analyze_cond(exp):
    """
    Transforms a cond expression to if and begin expressions.
    """
    def cond_first_clause():
        """
        Get the first clause part.
        """
        return exp[0]

    def cond_rest_clauses():
        """
        Get the rest of the clauses.
        """
        return exp[1:]

    def cond_clause_predicate():
        """
        Get the predicate part of a clause.
        """
        return exp[0][0]

    def cond_clause_actions():
        """
        Get the actions part of a clause.
        """
        return exp[0][1:]

    def analyze_sequence(seq):
        """
        Analyze the action part of a clause.
        """
        assert len(seq) > 0
        if len(seq) == 1:
            return analyze(seq[0])
        else:
            return _analyze_begin(seq)

    if len(exp) > 0:
        if (not isinstance(cond_first_clause(), list)) or len(cond_first_clause()) < 2:
            raise syntaxerror.SchemeSyntaxError("cond: Clause syntax error.")
    if len(exp) == 0:
        return expressions.SelfEvaluating(basictypes.Boolean(False))
    elif cond_clause_predicate() == "else":
        if len(exp) > 1:
            raise syntaxerror.SchemeSyntaxError("cond: Else clause not last.")
        return analyze_sequence(cond_clause_actions())
    else:
        return expressions.If(analyze(cond_clause_predicate()),
                              analyze_sequence(cond_clause_actions()),
                              _analyze_cond(cond_rest_clauses()))


def _special_form(exp):
    """
    Creates a special form expression.
    """
    def special_form_type():
        """
        Get the type part.
        """
        return exp[0]

    def special_form_parts():
        """
        Get the rest of the special form.
        """
        return exp[1:]

    special_forms = {
        'quote': _analyze_quote,
        'set!': _analyze_set,
        'define': _analyze_define,
        'if': _analyze_if,
        'lambda': _analyze_lambda,
        'begin': _analyze_begin,
        'cond': _analyze_cond,
        # TODO: let (let->lambda), let* (let*->nested lets), for, while, ...
        }
    if not (isinstance(exp, list)
            and len(exp) >= 1
            and isinstance(exp[0], str)
            and exp[0] in special_forms):
        raise _AnalyzeTypeError
    return special_forms[special_form_type()](special_form_parts())


def _application(exp):
    """
    Creates an application expression.
    """
    def application_operator():
        """
        Get the operator part.
        """
        return exp[0]

    def application_arguments():
        """
        Get the arguments part.
        """
        return exp[1:]

    if not isinstance(exp, list):
        raise _AnalyzeTypeError
    if len(exp) == 0:
        raise syntaxerror.SchemeSyntaxError("application: Empty application.")
    return expressions.Application(analyze(application_operator()),
                                   [analyze(a) for a in application_arguments()])


def analyze(exp):
    """
    Analyzes a tokenized expression and creates backend objects.
    """
    analyzers = [_self_evaluating, _identifier, _special_form, _application]
    for analyzer in analyzers:
        try:
            return analyzer(exp)
        except _AnalyzeTypeError:
            pass
    raise syntaxerror.SchemeSyntaxError("Unknown expression type.")
