import ast
from xast.comparator import Comparator, WeightedComparator
from xast.visitors import DepthsTracer, Counter
from pprint import pprint


class SyntaxTree:
    EPSILON = 1E-1
    def __init__(self, root, comparator):
        self.__root = root
        dt = DepthsTracer()
        dt.visit(root)
        self.__comp = comparator
        self.__depths = dt.get_depths()
        self.__count = Counter().visit(root)

    def __str__(self):
        return ast.dump(self.__root)

    def __eq__(self, other):

        # http://leodemoura.github.io/files/ICSM98.pdf

        subtrees_at = {}

        all_depths = set(self.__depths) & set(other.__depths) - {0, 1, 2}

        for d in all_depths:
            nodes_at = self.__depths.get(d, [])
            other_at = other.__depths.get(d, [])
            i, j = 0, 0
            while i < len(nodes_at) and j < len(other_at):
                print('-', end='')
                if self.__comp.compare(nodes_at[i], other_at[j]):
                    subtrees_at[d] = subtrees_at.get(d, []) + \
                                     [(nodes_at.pop(i), other_at.pop(j))]
                else:
                    j += 1
                    if j == len(other_at):
                        i += 1
                        j = 0

        if len(subtrees_at) == 0:
            return False

        max_d = max(subtrees_at.keys())
        sum_all = self.__count + other.__count
        cnt = Counter()
        print(max_d, subtrees_at[max_d])
        sum_sub = sum(cnt.visit(r) + cnt.visit(l) for r, l in subtrees_at[max_d])
        print(sum_all, sum_sub, sum_sub / sum_all)
        return (sum_sub / sum_all) > SyntaxTree.EPSILON


class TreeBuilder:
    @staticmethod
    def build(lines, weights):
        return SyntaxTree(ast.parse(''.join(lines)), WeightedComparator(weights))