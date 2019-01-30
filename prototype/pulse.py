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
        """compound_statement: FOR | WHILE | DOWHILE | FUN | ID | SWITCH"""
        if self.current_token.type == "FOR":
            node = self.for()
        elif self.current_token.type == "WHILE":
            node = self.while()
        elif self.current_token.type == "DOWHILE":
            node = self.dowhile()
        elif self.current_token.type == "FUN":
            node = self.fun()
        elif self.current_token.type == "IF":
            node = self.if()
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

import sys

text = open(sys.argv[1], "r").read()

text = text.replace("    ", "~")
text = text.replace("\n", "^")

lex = Lexer(text)

lex.lexer()
