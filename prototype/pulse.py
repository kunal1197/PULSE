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
    'show': Token('SHOW', 'SHOW')
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

            if self.current_char == '=' and self.peek() != '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                return Token(ASSIGN, '==')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

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
                return Token(INTEGER_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

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

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Program(AST):
    def __init__(self, block):
        self.block = block

class Block(AST):
    def __init__(self, statement):
        self.statement = statement

class Show(AST):
    def __init__(self, expr):
        self.expr = expr

class For(AST):
    def __init__(self, iterator, begin, end, increment, compound_statement):
        self.iterator = iterator
        self.begin = begin
        self.end = end
        self.increment = increment
        self.compound_statement = compound_statement

class While(AST):
    def __init__(self, expr, compound_statement):
        self.expr = expr
        self.compound_statement = compound_statement

class Dowhile(AST):
    def __init__(self, epxr, compound_statement):
        self.expr = expr
        self.compound_statement = compound_statement

class While(AST):
    def __init__(self, expr, consts, compound_statements):
        self.expr = expr
        self.consts = consts
        self.compound_statements = compound_statements

class If(AST):
    def __init__(self, if_expr, if_compound_statement, elseif_exprs, elseif_compound_statments, else_expr, else_compound_statment):
        self.if_expr = if_expr
        self.if_compound_statement = if_compound_statement
        self.elseif_exprs = elseif_exprs
        self.elseif_compound_statments = elseif_compound_statments
        self.else_expr = else_expr
        self.else_compound_statment = else_compound_statment

class Switch(AST):
    def __init__(self, expr, consts, compound_statements):
        self.expr = expr
        self.consts = consts
        self.compound_statements = compound_statements

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
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
        if self.current_token.type == ID or self.current_token.type == VAL or self.current_token.type == VAL or self.current_token.type == SHOW:
            node = Block(self.single_line())
        else:
            node = Block(self.compound_statement())

        return node

    def single_line(self):
        """single_line: "ID | VAR | VAL | SHOW"""
        if self.current_token.type == ID:
            node = self.id()
        elif self.current_token.type == VAR:
            node = self.var()
        elif self.current_token.type == VAL:
            node = self.val()
        elif self.current_token.type == SHOW:
            node = self.show()

        return node

    def compound_statement():
        """compound_statement: FOR | WHILE | DOWHILE | FUN | IF | SWITCH"""
        # if self.current_token.type == "FOR":
        #     node = self.for()
        # elif self.current_token.type == "WHILE":
        #     node = self.while()
        # elif self.current_token.type == "DOWHILE":
        #     node = self.dowhile()
        # elif self.current_token.type == "FUN":
        #     node = self.fun()
        # elif self.current_token.type == "IF":
        #     node = self.if()
        # elif self.current_token.type == "SWITCH":
        #     node = self.switch()

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
        if(!begin_empty):
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
        if(!increment_empty):
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

            if(!break_flag):
                self.eat(UNINDENT)

            i += 1

        if(i == 0):
            self.error()

        self.eat(UNINDENT)

        node = Switch(expr, consts, compound_statements)

        return node


import sys

text = open(sys.argv[1], "r").read()

text = text.replace("    ", "~")
text = text.replace("\n", "^")

lex = Lexer(text)

lex.lexer()
