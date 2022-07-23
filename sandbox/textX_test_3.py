from textx import metamodel_from_file

ba1_meta = metamodel_from_file(r'..\src\naive\data\ba1_utf8.tx')


ba1_sample_1 = r'(b1 ∧ b2)'

ba1_model = ba1_meta.model_from_str(ba1_sample_1)

print(ba1_model)
