from schemepy.backend import basictypes, expressions
from schemepy.frontend import syntaxerror


class _AnalyzeTypeError(TypeError):
    pass


def _to_basic_type(exp):
    def to_string():
        if len(exp) >= 2 and exp[0] == '"' and exp[-1] == '"':
            return basictypes.String(exp[1:-1])
        raise _AnalyzeTypeError

    def to_number():
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
    if isinstance(exp, str):
        try:
            _to_basic_type(exp)
        except _AnalyzeTypeError:
            return True
    return False


def _self_evaluating(exp):
    try:
        basic_type = _to_basic_type(exp)
        return expressions.SelfEvaluating(basic_type)
    except _AnalyzeTypeError:
        raise


def _identifier(exp):
    if _is_identifier(exp):
        return expressions.Identifier(exp)
    raise _AnalyzeTypeError


def _analyze_quote(exp):  # TODO: Handle other kind of quotes
    def quote_quotation():
        return exp[0]

    def analyze_quotation(quotation):
        if isinstance(quotation, list):
            if len(quotation) == 3 and quotation[1] == '.':
                return basictypes.Pair(analyze_quotation(quotation[0]), analyze_quotation(quotation[2]))
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
    def set_identifier():
        return exp[0]

    def set_value():
        return exp[1]

    if len(exp) != 2:
        raise syntaxerror.SchemeSyntaxError("set!: 2 parts expected, {} is given.".format(len(exp)))
    if not _is_identifier(set_identifier()):
        raise syntaxerror.SchemeSyntaxError("set!: Not an identifier.")
    return expressions.Assignment(set_identifier(), analyze(set_value()))


def _analyze_define(exp):
    def define_identifier():
        if isinstance(exp[0], list):
            if len(exp[0]) == 0:
                raise syntaxerror.SchemeSyntaxError("define: No identifier in procedure definition.")
            return exp[0][0]
        else:
            return exp[0]

    def define_value():
        # NOTE: The value is analyzed.
        if isinstance(exp[0], list):
            return _analyze_lambda([exp[0][1:]] + exp[1:])
        else:
            return analyze(exp[1])

    if len(exp) < 2:
        raise syntaxerror.SchemeSyntaxError("define: At least 2 parts expected, {} is given.".format(len(exp)))
    if not _is_identifier(define_identifier()):
        raise syntaxerror.SchemeSyntaxError("define: Not an identifier.")
    return expressions.Definition(define_identifier(), define_value())


def _analyze_if(exp):
    def if_predicate():
        return exp[0]

    def if_consequent():
        return exp[1]

    def if_alternative():
        return exp[2]

    if not 2 <= len(exp) <= 3:
        raise syntaxerror.SchemeSyntaxError("if: 2 or 3 parts expected, {} is given.".format(len(exp)))
    return expressions.If(analyze(if_predicate()),
                          analyze(if_consequent()),
                          analyze(if_alternative()) if len(exp) == 3 else None)


def _analyze_lambda(exp):
    def lambda_parameters():
        return exp[0]

    def lambda_body():
        return exp[1:]

    if len(exp) < 2:
        raise syntaxerror.SchemeSyntaxError("lambda: At least 2 parts expected, {} is given.".format(len(exp)))
    if (not isinstance(lambda_parameters(), list)) or any([not _is_identifier(p) for p in lambda_parameters()]):
        raise syntaxerror.SchemeSyntaxError("lambda: Error in parameter declaration.")
    return expressions.Lambda(lambda_parameters(), [analyze(e) for e in lambda_body()])


def _analyze_begin(exp):
    def begin_sequence():
        return exp

    return expressions.Begin([analyze(e) for e in begin_sequence()])


def _analyze_cond(exp):
    def cond_first_clause():
        return exp[0]

    def cond_rest_clauses():
        return exp[1:]

    def cond_clause_predicate():
        return exp[0][0]

    def cond_clause_actions():
        return exp[0][1:]

    def analyze_sequence(seq):
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
    def special_form_type():
        return exp[0]

    def special_form_parts():
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
    if not (isinstance(exp, list) and len(exp) >= 1 and isinstance(exp[0], str) and exp[0] in special_forms):
        raise _AnalyzeTypeError
    return special_forms[special_form_type()](special_form_parts())


def _application(exp):
    def application_operator():
        return exp[0]

    def application_arguments():
        return exp[1:]

    if not isinstance(exp, list):
        raise _AnalyzeTypeError
    if len(exp) == 0:
        raise syntaxerror.SchemeSyntaxError("application: Empty application.")
    return expressions.Application(analyze(application_operator()), [analyze(a) for a in application_arguments()])


def analyze(exp):
    analyzers = [_self_evaluating, _identifier, _special_form, _application]
    for analyzer in analyzers:
        try:
            return analyzer(exp)
        except _AnalyzeTypeError:
            pass
    raise syntaxerror.SchemeSyntaxError("Unknown expression type.")
