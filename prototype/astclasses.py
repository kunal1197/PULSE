class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    def __str__(self):
        return "BinOp({left}, {token}, {op}, {right})".format(
            left = self.left,
            token = self.token,
            op = self.op,
            right = self.right
        )

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __str__(self):
        return "Num({token}, {value})".format(
            token = self.token,
            value = self.value
        )

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
    def __str__(self):
        return "UnaryOp({token}, {op}, {expr})".format(
            token = self.token,
            op = self.op,
            expr = self.expr
        )

class Compound(AST):
    def __init__(self):
        self.children = []
    def __str__(self):
        return "Compound({children})".format(
            children = self.children
        )

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    def __str__(self):
        return "Assign({left}, {token}, {op}, {right})".format(
            left = self.left,
            token = self.token,
            op = self.op,
            right = self.right
        )

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __init__(self):
        return "Var({token}, {value})".format(
            token = self.token,
            value = self.value
        )

class NoOp(AST):
    pass

class Program(AST):
    def __init__(self, block):
        self.block = block
    def __str__(self):
        return "Program({block})".format(
            block = self.block
        )

class Block(AST):
    def __init__(self):
        self.statements = []
        self.stypes = []
    def __str__(self):
        return "Block({statements}, {stypes})".format(
            statements = self.statements,
            stypes = self.stypes
        )

class Single(AST):
    def __init__(self, statement, stype):
        self.statement = statement
        self.stype = stype
    def __str__(self):
        return "Single({statement}, {stype})".format(
            statement = self.statement,
            stype = self.stype
        )

class Show(AST):
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return "Show({expr})".format(
            expr = self.expr
        )

class For(AST):
    def __init__(self, iterator, begin, end, increment, compound_statement):
        self.iterator = iterator
        self.begin = begin
        self.end = end
        self.increment = increment
        self.compound_statement = compound_statement
    def __str__(self):
        return "For({iterator}, {begin}, {end}, {increment}, {compound_statement})".format(
            iterator = self.iterator,
            begin = self.begin,
            end = self.end,
            increment = self.increment,
            compound_statement = self.compound_statement
        )

class While(AST):
    def __init__(self, expr, compound_statement):
        self.expr = expr
        self.compound_statement = compound_statement
    def __str__(self, expr, compound_statement):
        return "While({expr}, {compound_statement})".format(
            expr = self.expr,
            compound_statement = self.compound_statement
        )

class Dowhile(AST):
    def __init__(self, epxr, compound_statement):
        self.expr = expr
        self.compound_statement = compound_statement
    def __str__(self):
        return "Dowhile({expr}, {compound_statement})".format(
            expr = self.expr,
            compound_statement = self.compound_statement
        )

class While(AST):
    def __init__(self, expr, consts, compound_statements):
        self.expr = expr
        self.consts = consts
        self.compound_statements = compound_statements
    def __str__(self):
        return "While({expr}, {consts}, {compound_statements})".format(
            expr = self.expr,
            consts = self.consts,
            compound_statements = self.compound_statements
        )

class If(AST):
    def __init__(self, if_expr, if_compound_statement, elseif_exprs, elseif_compound_statments, else_expr, else_compound_statment):
        self.if_expr = if_expr
        self.if_compound_statement = if_compound_statement
        self.elseif_exprs = elseif_exprs
        self.elseif_compound_statments = elseif_compound_statments
        self.else_expr = else_expr
        self.else_compound_statment = else_compound_statment
    def __str__(self):
        return "If({if_expr}, {if_compound_statement}, {elseif_exprs}, {elseif_compound_statments}, {else_expr}, {else_compound_statment})".format(
            if_expr = self.if_expr,
            if_compound_statement = self.if_compound_statement,
            elseif_exprs = self.elseif_exprs,
            elseif_compound_statments = self.elseif_compound_statments,
            else_expr = self.else_expr,
            else_compound_statment = self.else_compound_statment
        )

class Switch(AST):
    def __init__(self, expr, consts, compound_statements):
        self.expr = expr
        self.consts = consts
        self.compound_statements = compound_statements
    def __str__(self, expr, consts, compound_statements):
        return "Switch({expr}, {consts}, {compound_statements})".format(
            expr = self.expr,
            consts = self.consts,
            compound_statements = self.compound_statements
        )

class Fun(AST):
    def __init__(self, func_name, var_types, var_names, compound_statement):
        self.func_name = func_name
        self.var_types = var_types
        self.var_names = var_names
        self.compound_statement = compound_statement
    def __str__(self):
        return "Fun({func_name}, {var_types}, {var_names}, {compound_statement})".format(
            func_name = self.func_name,
            var_types = self.var_types,
            var_names = self.var_names,
            compound_statement = self.compound_statement
        )
