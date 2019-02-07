from token import Token

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
