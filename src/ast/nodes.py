# Define your tree before you walk it.
class ASTNode:
    pass


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class CellNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Cell({self.name})"


class RangeNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Range({self.value})"


class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"


class FunctionCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"
