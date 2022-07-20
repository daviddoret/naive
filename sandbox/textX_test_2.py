import textx

ba1_source = """

ConjunctionFormula:
    arguments+=AtomicVariable symbol=ConjunctionOperator arguments+=AtomicVariable
;

ConjunctionOperator:
    '∧' | 'and' | 'land'
;

/*
TODO: Split this into VariableBaseName, VariableExponent and VariableIndexes
References:
- https://stackoverflow.com/questions/5555613/does-w-match-all-alphanumeric-characters-defined-in-the-unicode-standard
*/

AtomicVariable:
    /[\w,\⊥,\⊤]+/
;


"""



ba1_meta = textx.metamodel_from_str(ba1_source)


ba1_sample_1 = r'b1 ∧ b2'

ba1_model = ba1_meta.model_from_str(ba1_sample_1)

print(ba1_model)
