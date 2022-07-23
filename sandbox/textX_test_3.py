from textx import metamodel_from_file

ba1_meta = metamodel_from_file(r'..\src\naive\data\ba1_utf8.tx')


ba1_sample_1 = r'(((⊤ ∨ b1) ∧ (⊥ ∧ ¬⊥)) ∧ ¬((b2)))'
ba1_sample_2 = r'¬⊥'
ba1_sample_3 = r'⊥'
ba1_sample_4 = r'b₇₃'
ba1_sample_5 = r'(p ∨ q)'

ba1_model = ba1_meta.model_from_str(ba1_sample_5)

print(ba1_model)
