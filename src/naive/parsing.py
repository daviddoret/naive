from textx import metamodel_from_file, metamodel_from_str
import pkg_resources

import log
import core
import ba1


def parse_string_utf8(code):

    metamodel_source = None
    try:
        metamodel_source = pkg_resources.resource_string('naive', 'data/ba1_utf8.tx').decode('utf-8')
    except:
        with open(r'c:\users\David\pycharmprojects\naive\src\naive\data\ba1_utf8.tx', 'r', encoding='utf-8') as source_file:
            metamodel_source = source_file.read()
    #log.debug(metamodel_source=metamodel_source)
    metamodel = metamodel_from_str(metamodel_source)
    model = metamodel.model_from_str(code)
    if model.token:
        formula = inflate_object(model)
        log.debug(parsed_formula=formula)
        return formula
    else:
        log.warning('Parsing result is empty.')

def inflate_object(model_object):
    arguments = []
    if hasattr(model_object, 'arguments'):
        for model_argument in model_object.arguments:
            argument = inflate_object(model_argument)
            arguments.append(argument)
    class_name = model_object._tx_fqn
    token = model_object.token
    # TODO: To scale this to multiple languages, implement a solution where
    #   every language is subscribed to the parsing function.
    match class_name:
        case 'BA1ConjunctionFormula':
            return core.f(ba1.conjunction, *arguments)
        case 'BA1DisjunctionFormula':
            return core.f(ba1.disjunction, *arguments)
        case 'BA1NegationFormula':
            return core.f(ba1.negation, *arguments)
        case 'BA1TruthFormula':
            return ba1.truth
        case 'BA1FalsumFormula':
            return ba1.falsum
        case 'BA1AtomicVariableFormula':
            return core.v(ba1.b, token)

def parse_file_utf8():
    # TODO: Implement this.
    pass