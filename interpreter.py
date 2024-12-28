import re

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
        
        if result.lower() == 'if':
          return Token(IF, result)
        elif result.lower() == 'else':
          return Token(ELSE, result)
        elif result.lower() == 'while':
          return Token(WHILE, result)
        elif result.lower() == 'print':
          return Token(PRINT, result)
        elif result.lower() == 'input':
          return Token(INPUT, result)

        return Token(ID, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
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
    def __init__(self):
        pass

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
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == WHILE:
            node = self.while_statement()
        elif self.current_token.type == PRINT:
            node = self.print_statement()
        elif self.current_token.type == INPUT:
            node = self.input_statement()
        else:
            node = self.empty()
        return node
    
    def if_statement(self):
        """if_statement : IF comparison compound_statement (ELSE compound_statement)?"""
        self.eat(IF)
        condition = self.comparison()
        then_branch = self.compound_statement()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_branch = self.compound_statement()
        else:
            else_branch = None
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
        expr = self.expr()
        self.eat(RPAREN)
        return Print(expr)
        
    def input_statement(self):
      """input_statement: INPUT LPAREN RPAREN"""
      self.eat(INPUT)
      self.eat(LPAREN)
      self.eat(RPAREN)
      return Input()

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
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
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | DIV | MOD) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
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
            node = self.variable()
            return node

    def comparison(self):
      """
      comparison : expr (( EQ | NE | LT | LTE | GT | GTE ) expr)
      """
      node = self.expr()
      
      while self.current_token.type in (EQ, NE, LT, LTE, GT, GTE):
        token = self.current_token
        if token.type == EQ:
          self.eat(EQ)
        elif token.type == NE:
          self.eat(NE)
        elif token.type == LT:
          self.eat(LT)
        elif token.type == LTE:
          self.eat(LTE)
        elif token.type == GT:
          self.eat(GT)
        elif token.type == GTE:
          self.eat(GTE)
          
        node = BinOp(left=node, op=token, right=self.expr())
      
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
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == LT:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == LTE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == GTE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == EQ:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NE:
            return self.visit(node.left) != self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        if self.GLOBAL_SCOPE.get(var_name) is None:
          self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        else:
          raise Exception('Error: variable was previously declared')

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(var_name)
        else:
            return val

    def visit_NoOp(self, node):
        pass
        
    def visit_If(self, node):
        if self.visit(node.condition):
            self.visit(node.then_branch)
        elif node.else_branch is not None:
            self.visit(node.else_branch)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)
    
    def visit_Print(self, node):
        print(self.visit(node.expr))

    def visit_Input(self, node):
        val = int(input())
        return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def execute_simplepy(code):
  """Executes SimplePy code and returns the content printed to standard output."""
  lexer = Lexer(code)
  parser = Parser(lexer)
  interpreter = Interpreter(parser)
  interpreter.interpret()

# --- Example Usage ---
def main():
    import sys
    
    if len(sys.argv) < 2:
      print("Usage: python interpreter.py <filename.simpy>")
      return
    
    filename = sys.argv[1]
    
    if not filename.endswith(".simpy"):
        print("Error: Input file must have a .simpy extension")
        return

    try:
      with open(filename, 'r') as file:
          code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
        
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

if __name__ == '__main__':
    main()
