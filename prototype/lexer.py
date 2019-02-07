from constants import *
from token import Token

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
