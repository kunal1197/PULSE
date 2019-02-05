###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
STRING = 'STRING'
INTEGER_CONST = 'INTEGER_CONST'
FLOAT_CONST = 'FLOAT_CONST'
STRING_CONST = 'STRING_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
EQUAL = 'EQUAL'
VAR = 'VAR'
VAL = 'VAL'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'
INDENT = "INDENT"
UNINDENT = "UNINDENT"
AND = "AND"
OR = "OR"
NOT = "NOT"
LESS = "LESS"
LEQ = "LEQ"
EQUAL = "EQUAL"
NOTEQUAL = "NOTEQUAL"
GREAT = "GREAT"
GEQ = "GEQ"
INC = "INC"
DEC = "DEC"
POWER = "POWER"
BEGIN = 'BEGIN'
END = 'END'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER_CONST, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'var': Token('VAR', 'VAR'),
    'val': Token('VAL', 'VAL'),
    'switch': Token('SWITCH', 'SWITCH'),
    'case': Token('CASE', 'CASE'),
    'break': Token('BREAK', 'BREAK'),
    'if': Token('IF', 'IF'),
    'elseif': Token('ELSEIF', 'ELSEIF'),
    'else': Token('ELSE', 'ELSE'),
    'for': Token('FOR', 'FOR'),
    'while': Token('WHILE', 'WHILE'),
    'dowhile': Token('DOWHILE', 'DOWHILE'),
    'fun': Token('FUNCTION', 'FUNCTION'),
    'show': Token('SHOW', 'SHOW'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1

        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # TODO: Implement comments
    def skip_comment(self):
        pass

    def number(self):
        result = ''

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while(self.current_char is not None and self.current_char.isdigit()):
                result += self.current_char
                self.advance()

            token = Token('FLOAT_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))

        # TODO: Implement string constants

        return token

    def _id(self):
        result = ''

        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))

        return token

    def get_next_token(self):
        indented = False

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # TODO: Implement comments

            if self.current_char == "~":
                self.advance()
                indented = True
                return Token(INDENT, "\t")

            if self.current_char == "^" and indented:
                self.advance()
                indented = False
                return Token(UNINDENT, "-T")

            if self.current_char == "^" and not indented:
                self.advance()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == "!" and self.peek() == "=":
                self.advance()
                return Token(NOTEQUAL, "!=")

            if self.current_char == '=' and self.peek() != '=':
                self.advance()
                return Token(EQUAL, '==')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                return Token(ASSIGN, '==')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == "$":
                self.advance()
                return Token(POWER, "$")

            if self.current_char == '+' and self.peek() != '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-' and self.peek() != '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/' and self.peek() != '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '/' and self.peek() == '/':
                self.advance()
                return Token(INTEGER_DIV, '//')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == "<" and self.peek() != "=":
                self.advance()
                return Token(LESS, "<")

            if self.current_char == "<" and self.peek() == "=":
                self.advance()
                return Token(LEQ, "<=")

            if self.current_char == ">" and self.peek() != "=":
                self.advance()
                return Token(GREAT, ">")

            if self.current_char == ">" and self.peek() == "=":
                self.advance()
                return Token(GEQ, ">=")

            if self.current_char == "&" and self.peek() == "&":
                self.advance()
                return Token(AND, "&&")

            if self.current_char == "|" and self.peek() == "|":
                self.advance()
                return Token(OR, "||")

            if self.current_char == "!" and self.peek() != "=":
                self.advance()
                return Token(NOT, "!")

            # TODO: Implement indentation, increment, decrement

            self.error()

        return Token(EOF, None)

    def lexer(self):
        current_token = self.get_next_token()
        while current_token.type != EOF:
            print(current_token)
            current_token = self.get_next_token()

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

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
    def __init__(self, stype, single_line = None, compound_statement = None):
        self.single_line = single_line
        self.compound_statement = compound_statement
        self.stype = stype
    def __str__(self):
        return "Block({single_line}, {compound_statement}, {stype})".format(
            single_statement = self.single_line,
            compound_statement = self.compound_statement,
            stype = self.stype,

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

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax!")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            print(token_type)
            print(self.current_token.type)
            self.current_token = self.lexer.get_next_token()
        else:
            print(token_type)
            print(self.current_token.type)
            self.error()

    def program(self):
        """program: BEGIN block END"""
        self.eat(BEGIN)
        block_node = self.block()
        program_node = Program(block_node)
        self.eat(END)

        return program_node

    def block(self):
        """block: single_line | compound_statement"""
        if self.current_token.type == ID or self.current_token.type == VAL or self.current_token.type == VAL or self.current_token.type == "SHOW":
            node = Block("single", self.single_line(), None)
        else:
            node = Block("compound", None, self.compound_statement())

        return node

    def single_line(self):
        """single_line: "ID | VAR | VAL | SHOW"""
        if self.current_token.type == ID:
            node = self.id()
        elif self.current_token.type == VAR:
            node = self.var()
        elif self.current_token.type == VAL:
            node = self.val()
        elif self.current_token.type == "SHOW":
            node = self.show()

        return node

    def compound_statement():
        """compound_statement: FOR | WHILE | DOWHILE | FUN | IF | SWITCH"""
        if self.current_token.type == "FOR":
            node = self.FOR()
        elif self.current_token.type == "WHILE":
            node = self.WHILE()
        elif self.current_token.type == "DOWHILE":
            node = self.dowhile()
        elif self.current_token.type == "FUN":
            node = self.fun()
        elif self.current_token.type == "IF":
            node = self.IF()
        elif self.current_token.type == "SWITCH":
            node = self.switch()

    def id(self):
        """id: ID ASSIGN expr"""
        left = Var(self.current_token)
        self.eat(ID)
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def var(self):
        """var: VAR ID ASSIGN expr"""
        self.eat("VAR")
        left = Var(self.current_token)
        self.eat(ID)
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def val(self):
        """val: VAL ID ASSIGN expr"""
        self.eat("VAL")
        left = Var(self.current_token)
        self.eat(ID)
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def show(self):
        """show: SHOW expr"""
        self.eat("SHOW")
        exp = self.expr()
        node = Show(exp)

        return node

    def FOR(self):
        """for: FOR VAR ID IN (VAL)? COMMA VAL COMMA (VAL)? COLON INDENT (compound_statement)+"""
        self.eat("FOR")
        self.eat("VAR")
        iterator = self.current_token
        self.eat(ID)
        self.eat("IN")
        token = self.current_token
        begin_empty = False
        begin = 0
        if token.type == COMMA:
            begin = Token(INTEGER_CONST, "0")
            self.eat(COMMA)
            begin_empty = True
        elif token.type == INTEGER_CONST:
            begin = self.current_token
            self.eat(INTEGER_CONST)
        if(not begin_empty):
            self.eat(COMMA)
        end = self.current_token
        self.eat(INTEGER_CONST)
        self.eat(COMMA)
        token = self.current_token
        increment_empty = False
        increment = 0
        if token.type == COLON:
            increment = Token(INTEGER_CONST, "1")
            self.eat(COLON)
            increment_empty = True
        elif token.type == INTEGER_CONST:
            increment = self.current_token
            self.eat(INTEGER_CONST)
        if(not increment_empty):
            self.eat(COLON)
        self.eat(INDENT)
        compound_statement = self.compound_statement()
        self.eat(UNINDENT)

        node = For(iterator, begin, end, increment, compound_statement)

        return node

    def WHILE(self):
        """while: WHILE expr COLON INDENT (compound_statement)+ UNINDENT"""
        self.eat("WHILE")
        expr = self.expr()
        self.eat(COLON)
        self.eat(INDENT)
        compound_statement = self.compound_statement()
        self.eat(UNINDENT)

        node = While(expr, compound_statement)

        return node

    def dowhile(self):
        """dowhile: DOWHILE expr COLON INDENT (compound_statement)+ UNINDENT"""
        self.eat("DOWHILE")
        expr = self.expr()
        self.eat(COLON)
        self.eat(INDENT)
        compound_statement = self.compound_statement()
        self.eat(UNINDENT)

        node = Dowhile(expr, compound_statement)

        return node

    def fun(self):
        """fun: FUN ID LPAREN ((VAR|VAL) ID (COMMA)?)* RPAREN COLON INDENT compound_statement UNINDENT"""
        self.eat("FUN")
        func_name = self.eat(ID)
        self.eat(LPAREN)
        var_types = []
        var_names = []
        while True:
            if self.current_token.type == "VAR":
                var_types.append("VAR")
                self.eat("VAR")
            elif self.current_token.type == "VAL":
                var_types.append("VAL")
                self.eat("VAL")
            var_names.append(self.eat(ID))
            if(self.current_token.type == RPAREN):
                self.eat(RPAREN)
                break
            self.eat(COMMA)

        self.eat(COLON)
        self.eat(INDENT)
        compound_statement = self.compound_statement()
        self.eat(UNINDENT)

        node = Fun(func_name, var_types, var_names, compound_statement)

        return node

    def IF(self):
        self.eat("IF")
        if_expr = self.expr()
        self.eat(COLON)
        self.eat(INDENT)
        if_compound_statement = self.compound_statement()
        self.eat(UNINDENT)

        elseif_exprs = []
        elseif_compound_statments = []

        while self.current_token.type == "ELSEIF":
            self.eat("ELSEIF")
            elseif_exprs.append(self.expr())
            self.eat(COLON)
            self.eat(INDENT)
            elseif_compound_statments.append(self.compound_statement())
            self.eat(UNINDENT)

        if(self.current_token.type == "ELSE"):
            self.eat("ELSE")
            else_expr = self.expr()
            self.eat(COLON)
            self.eat(INDENT)
            elseif_compound_statment = self.compound_statement()
            self.eat(UNINDENT)

        node = If(if_expr, if_compound_statement, elseif_exprs, elseif_compound_statments, else_expr, elseif_compound_statment)

        return node

    def switch(self):
        """switch: SWITCH expr COLON INDENT (CASE (INTEGER_CONST|FLOAT_CONST) COLON INDENT compound_statement BREAK? UNINDENT)+ UNINDENT"""
        self.eat("SWITCH")
        expr = self.expr()
        self.eat(COLON)
        self.eat(INDENT)

        consts = []
        compound_statements = []

        i = 0
        while self.current_token.type == "CASE":
            self.eat(CASE)
            consts.append(self.current_token)
            if(const.type == INTEGER_CONST):
                self.eat(INTEGER_CONST)
            elif(const.type == FLOAT_CONST):
                self.eat(FLOAT_CONST)

            self.eat(COLON)
            self.eat(INDENT)

            compound_statements.append(self.compound_statement())

            token = self.current_token

            break_flag = False

            if(self.current_token.type == "BREAK"):
                self.eat(BREAK)
                break_flag = True
            elif(self.current_token.type == UNINDENT):
                self.eat(UNINDENT)

            if(not break_flag):
                self.eat(UNINDENT)

            i += 1

        if(i == 0):
            self.error()

        self.eat(UNINDENT)

        node = Switch(expr, consts, compound_statements)

        return node

    def expr(self):
        """expr: level7(|| level7)*"""
        node = self.level7()

        while self.current_token == OR:
            self.eat(OR)

            node = BinOp(left=node, op=token, right=self.level7())

        return node

    def level7(self):
        """level7: level6(&& level6)*"""
        node = self.level6()

        while self.current_token == AND:
            self.eat(AND)

            node = BinOp(left=node, op=token, right=self.level6())

        return node

    def level6(self):
        """level6: level5((EQUAL|NOTEQUAL) level5)*"""
        node = self.level5()

        while self.current_token in (EQUAL, NOTEQUAL):
            token = self.current_token

            if token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == NOTEQUAL:
                self.eat(NOTEQUAL)

            node = BinOp(left=node, op=token, right=self.level5())

        return node

    def level5(self):
        """level5: level4((LESS|LEQ|GREAT|GEQ) level4)*"""
        node = self.level4()

        while self.current_token in (LESS, LEQ, GREAT, GEQ):
            token = self.current_token

            if token.type == LESS:
                self.eat(LESS)
            elif token.type == LEQ:
                self.eat(LEQ)
            elif token.type == GREAT:
                self.eat(GREAT)
            elif token.type == GEQ:
                self.eat(GEQ)

            node = BinOp(left=node, op=token, right=self.level4())

        return node

    def level4(self):
        """level4: level3((PLUS|MINUS) level3)*"""
        node = self.level3()

        while self.current_token in (PLUS, MINUS):
            token = self.current_token

            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.level3())

        return node

    def level3(self):
        """level3: level2((MUL|FDIV|IDIV|MODULO) level2)*"""
        node = self.level2()

        while self.current_token in (MUL, FLOAT_DIV, INTEGER_DIV):
            token = self.current_token

            if token.type == MUL:
                self.eat(MUL)
            elif token.type == FDIV:
                self.eat(FDIV)
            elif token.type == IDIV:
                self.eat(IDIV)
            elif token.type == MODULO:
                self.eat(MODULO)

            node = BinaryOp(left=node, op=token, right=self.level2())

        return node

    def level2(self):
        """level2: level1(POWER level1)*"""
        node = self.level1()

        while self.current_token == POWER:
            self.eat(POWER)

            node = BinOp(left=node, op=self.current_token, right=self.level1())

        return node

    def level1(self):
        """"level1: factor((INC|DEC|NOT) factor)*"""
        node = self.factor()

        while self.current_token in (INC, DEC, NOT):
            token = self.current_token

            if token.type == INC:
                self.eat(INC)
            elif token.type == DEC:
                self.eat(DEC)
            elif token.type == NOT:
                self.eat(NOT)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor: PLUS factor|MINUS factor|INTEGER_CONST|FLOAT_CONST|STRING_CONST|LPAREN expr RPAREN"""
        token = self.current_token

        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == FLOAT_CONST:
            self.eat(FLOAT_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return note

    def parse(self):

        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
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
        if node.stype == "single":
            self.visit(node.show)
        elif node.stype == "compound":
            self.visit(node.compound_statement)

    def visit_show(self, node):
        self.visit(node.expr)

    def visit_expr(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)

import sys

text = open(sys.argv[1], "r").read()

text = text.replace("    ", "~")
text = text.replace("\n", " ^ ")
text = "BEGIN " + text + " END"

lex = Lexer(text)
parser = Parser(lex)
print(parser.parse())
interpreter = Interpreter(parser)
print(interpreter.interpret())
