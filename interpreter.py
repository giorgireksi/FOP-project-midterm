import re
import sys

# --- Token Types ---
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
SEMI = 'SEMI'
IF = 'IF'
ELSE = 'ELSE'
WHILE = 'WHILE'
PRINT = 'PRINT'
INPUT = 'INPUT'
LT = 'LT'
GT = 'GT'
LTE = 'LTE'
GTE = 'GTE'
EQ = 'EQ'
NE = 'NE'
EOF = 'EOF'

# --- Token Class ---
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# --- Lexer ---
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = ID  # Default to ID
        # Keywords:
        if result.lower() == 'if':
            token_type = IF
        elif result.lower() == 'else':
            token_type = ELSE
        elif result.lower() == 'while':
            token_type = WHILE
        elif result.lower() == 'print':
            token_type = PRINT
        elif result.lower() == 'input':
            token_type = INPUT

        return Token(token_type, result)

    def get_next_token(self):
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            # Identifier or Keyword
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            # Single-char tokens
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQ, '==')
                return Token(ASSIGN, '=')
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LTE, '<=')
                return Token(LT, '<')
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GTE, '>=')
                return Token(GT, '>')
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NE, '!=')

            self.error()

        return Token(EOF, None)

    def error(self):
        raise Exception('Invalid character')

# --- AST Nodes ---
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class If(AST):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        
class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class Input(AST):
    def __init__(self, var_name):
        self.var_name = var_name

# --- Parser ---
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """program : compound_statement"""
        node = self.compound_statement()
        return node

    def compound_statement(self):
        """compound_statement : statement_list"""
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | if_statement
                  | while_statement
                  | print_statement
                  | input_statement
                  | empty
        """
        tok_type = self.current_token.type

        if tok_type == ID:
            node = self.assignment_statement()
        elif tok_type == IF:
            node = self.if_statement()
        elif tok_type == WHILE:
            node = self.while_statement()
        elif tok_type == PRINT:
            node = self.print_statement()
        elif tok_type == INPUT:
            node = self.input_statement()
        else:
            node = self.empty()
        return node

    def if_statement(self):
        """if_statement : IF comparison compound_statement (ELSE compound_statement)?"""
        self.eat(IF)
        condition = self.comparison()
        then_branch = self.compound_statement()
        else_branch = None
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_branch = self.compound_statement()
        return If(condition, then_branch, else_branch)

    def while_statement(self):
        """while_statement : WHILE comparison compound_statement"""
        self.eat(WHILE)
        condition = self.comparison()
        body = self.compound_statement()
        return While(condition, body)

    def print_statement(self):
        """print_statement : PRINT LPAREN expr RPAREN"""
        self.eat(PRINT)
        self.eat(LPAREN)
        expr_node = self.expr()
        self.eat(RPAREN)
        return Print(expr_node)

    def input_statement(self):
        """input_statement : INPUT LPAREN RPAREN ID"""
        # For usage like: input() x;
        self.eat(INPUT)
        self.eat(LPAREN)
        self.eat(RPAREN)
        var_name = self.current_token.value
        self.eat(ID)
        return Input(var_name)

    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, op, right)

    def variable(self):
        """variable : ID"""
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        """term : factor ((MUL | DIV | MOD) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL)
            elif op.type == DIV:
                self.eat(DIV)
            elif op.type == MOD:
                self.eat(MOD)
            right = self.factor()
            node = BinOp(node, op, right)
        return node

    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            return self.variable()

    def comparison(self):
        """
        comparison : expr (( EQ | NE | LT | LTE | GT | GTE ) expr)?
        """
        node = self.expr()
        while self.current_token.type in (EQ, NE, LT, LTE, GT, GTE):
            op = self.current_token
            self.eat(op.type)
            right = self.expr()
            node = BinOp(node, op, right)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node

# --- Interpreter ---
class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        op_type = node.op.type
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if op_type == PLUS:
            return left_val + right_val
        elif op_type == MINUS:
            return left_val - right_val
        elif op_type == MUL:
            return left_val * right_val
        elif op_type == DIV:
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val // right_val
        elif op_type == MOD:
            if right_val == 0:
                raise ZeroDivisionError("Modulo by zero")
            return left_val % right_val
        elif op_type == LT:
            return int(left_val < right_val)
        elif op_type == LTE:
            return int(left_val <= right_val)
        elif op_type == GT:
            return int(left_val > right_val)
        elif op_type == GTE:
            return int(left_val >= right_val)
        elif op_type == EQ:
            return int(left_val == right_val)
        elif op_type == NE:
            return int(left_val != right_val)
        else:
            raise Exception(f"Unknown operator {op_type}")

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        val = self.visit(node.expr)
        if node.op.type == PLUS:
            return +val
        elif node.op.type == MINUS:
            return -val

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value

    def visit_Var(self, node):
        var_name = node.value
        if var_name not in self.GLOBAL_SCOPE:
            raise NameError(f"Name '{var_name}' is not defined")
        return self.GLOBAL_SCOPE[var_name]

    def visit_NoOp(self, node):
        pass

    def visit_If(self, node):
        condition_val = self.visit(node.condition)
        # If the expression is nonzero/true
        if condition_val != 0:
            self.visit(node.then_branch)
        else:
            if node.else_branch is not None:
                self.visit(node.else_branch)

    def visit_While(self, node):
        while True:
            cond_val = self.visit(node.condition)
            if cond_val == 0:
                break
            self.visit(node.body)

    def visit_Print(self, node):
        val = self.visit(node.expr)
        print(val)

    def visit_Input(self, node):
        var_name = node.var_name
        try:
            value = int(input(f"Enter an integer value for {var_name}: "))
            self.GLOBAL_SCOPE[var_name] = value
        except ValueError:
            raise Exception("Invalid input: Please enter an integer.")

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <filename.simpy>")
        return

    filename = sys.argv[1]
    if not filename.endswith(".simpy"):
        print("Error: Input file must have a .simpy extension")
        return

    try:
        with open(filename, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    try:
        interpreter.interpret()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
