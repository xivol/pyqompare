import ast
import sys, inspect
import json

weights = {}
for pname, pt in inspect.getmembers(sys.modules['ast'], inspect.isclass):
    for name, t in inspect.getmembers(sys.modules['ast'], inspect.isclass):
        if issubclass(pt, ast.AST) and issubclass(t, ast.AST):
            weights[f'{pname}_child_node_{name}'] = 1
            weights[f'{pname}_list_item_{name}'] = 1
    weights[f'{pname}_list_same_len'] = 1
    weights[f'{pname}_list_different_len'] = 0

print(json.dumps(weights))