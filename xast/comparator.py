import ast


class Comparator:

    def __compare_in_order(self, node_list, other_list):
        if len(node_list) != len(other_list):
            return False
        for i in range(len(node_list)):
            if not self.compare(node_list[i], other_list[i]):
                return False
        return True

    def compare(self, node, other):
        # print(node, other)
        if type(node) is not type(other):
            return False

        if isinstance(node, list):
            return self.__compare_in_order(node, other)
        if not isinstance(node, ast.AST):
            return True

        all = True
        for (_, node_value), (_, other_value) in \
                zip(ast.iter_fields(node), ast.iter_fields(other)):
            all = all and self.compare(node_value, other_value)
        return all


class WeightedComparator(Comparator):
    def __init__(self, weights):
        self.weight = weights

    def __eval_Lists(self, node_list, other_list, node_parent):
        if len(node_list) != len(other_list):
            return self.weight['list_different_len']

        prod = self.weight['list_same_len']
        for i in range(len(node_list)):
            prod *= self.__eval(node_list[i], other_list[i], node_parent) * \
                    self.weight['list_item']
        return prod

    def __eval_Names(self, node, other):
        if node.id == other.id:
            if node.ctx == other.ctx:
                return self.weight['name_same_id_same_ctx']
            else:
                return self.weight['name_same_id_different_ctx']
        else:
            if node.ctx == other.ctx:
                return self.weight['name_different_id_same_ctx']
            else:
                return self.weight['name_different_id_different_ctx']

    def __eval_Values(self, val, other_val):
        if val == other_val:
            return self.weight['values_are_equal']
        else:
            return self.weight['values_are_not_equal']

    def __eval(self, node, other, node_parent = None, other_parent = None):

        if type(node) is not type(other):
            return self.weight['subtree_different_node_type']

        if isinstance(node, list):
            return self.__eval_Lists(node, other)
        if not isinstance(node, ast.AST):
            return self.__eval_Values(node, other)
        if isinstance(node, ast.Name):
            return self.__eval_Names(node, other)

        summ = 0
        pairs = zip(ast.iter_fields(node), ast.iter_fields(other))
        for (_, node_value), (_, other_value) in pairs:
            summ += self.__eval(node_value, other_value, node) * \
                    self.weight[f'{type(node).__name__}_child_node_{type(node_value).__name__}']
        summ /= len(pairs)
        return summ

    def compare(self, node, other):
        if isinstance(node, SyntaxTree):
            self.__eval_Trees(node, other)
        return self.__eval(node, other) > self.weight['subtrees_are_equal_threshold']
