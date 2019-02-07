from constants import *
from astclasses import *

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax!")

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
        """block: (single_line | compound_statement)+"""

        node = Block()

        while True:
            token_type = self.current_token.type
            if token_type == ID or token_type == VAL or token_type == VAL or token_type == "SHOW":
                node.statements.append(self.single_line())
                node.stypes.append("singles")
            elif token_type == "FOR" or token_type == "WHILE" or token_type == "DOWHILE" or token_type == "IF" or token_type == "SWITCH" or token_type == "FUN":
                node.statements.append(self.compound_statement())
                node.stypes.append("compound")
            else:
                break

        return node

    def single_line(self):
        """single_line: "ID | VAR | VAL | SHOW | single_line | compound_statement"""
        if self.current_token.type == ID:
            node = Single(self.id(), "id")
        elif self.current_token.type == VAR:
            node = Single(self.var(), "var")
        elif self.current_token.type == VAL:
            node = Single(self.val(), "val")
        elif self.current_token.type == "SHOW":
            node = Single(self.show(), "show")

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