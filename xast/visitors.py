import ast


class Counter(ast.NodeVisitor):

    def generic_visit(self, node):
        if not isinstance(node, ast.AST):
            return 0
        counts = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list) and len(value) > 0:
                counts.append(sum(self.visit(item) for item in value))
            elif isinstance(value, ast.AST):
                counts.append(self.visit(value))
        return 1 + sum(counts)


class DepthsTracer(ast.NodeVisitor):
    def __init__(self):
        self.__depths = {}

    def generic_visit(self, node):
        if not isinstance(node, ast.AST):
            return -1
        depths = [0]
        for field, value in ast.iter_fields(node):
            if isinstance(value, list) and len(value) > 0:
                depths.append(max(self.visit(item) for item in value) + 1)
            elif isinstance(value, ast.AST):
                depths.append(self.visit(value) + 1)
        d = max(depths)

        self.__depths[d] = self.__depths.get(d, []) + [node]
        return d

    def get_depths(self):
        return self.__depths


class NamesCollector(ast.NodeVisitor):
    def __init__(self):
        self.__names = set()

    def generic_visit(self, node):
        super().generic_visit(node)
        return self.__names

    def visit_FunctionDef(self, node):
        self.__names.add(node.name)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.__names.add(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.__names.add(node.id)
        return self.generic_visit(node)

    def visit_arg(self, node):
        self.__names.add(node.arg)
        return self.__names
