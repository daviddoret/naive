from textx import metamodel_from_file
from textx.export import metamodel_export

entity_mm = metamodel_from_file('ba1_utf8.tx')
metamodel_export(entity_mm, 'ba1_utf8.dot')
