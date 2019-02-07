from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import sys

text = open(sys.argv[1], "r").read()

text = text.replace("    ", "~")
text = text.replace("\n", " ^ ")
text = "BEGIN " + text + " END"

lex = Lexer(text)
parser = Parser(lex)
interpreter = Interpreter(parser)
interpreter.interpret()
