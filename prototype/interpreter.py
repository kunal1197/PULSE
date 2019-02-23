from constants import *

class NodeVisitor(object):
    def visit(self, node, custom_name=""):
        method_name = "visit_" + type(node).__name__
        if(custom_name != ""):
            method_name = custom_name
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        import collections
        self.GLOBAL_SCOPE = collections.OrderedDict()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for (statement, stype) in zip(node.statements, node.stypes):
            if stype == "singles":
                self.visit(statement, "visit_Single")

    def visit_Single(self, node):
        if(node.stype == "show"):
            self.visit(node.statement, "visit_Show")

    def visit_Show(self, node):
        self.visit(node.expr)

    def visit_Num(self, node):
        print(node.token.value)

    def visit_expr(self, node):
        print(node)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)
