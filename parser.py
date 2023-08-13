import math
from numbers import Complex
from string import whitespace
from sys import maxunicode

lowercase = ''.join([chr(i) for i in range(maxunicode) if chr(i).islower()])

class Parser:
    def __init__(self, input: str):
        self.input = input
        self.tokens = []
        self.i = 0
        self.vars = {'e': math.e,
                     'π': math.pi}

    def end(self):
        return len(self.input) == 0

    def getchar(self):
        return self.input[0] if not self.end() else ''

    def nextchar(self):
        self.input = self.input[1:]
        return self.getchar()

    def reset_counter(self):
        self.i = 0

    def _token_number(self, inc: int, st: int = 0):
        c = self.getchar()
        i = 0
        p = st
        
        while not self.end() and c.isdigit():
            if inc < 0:
                i += (int(c) * 10**p)
            else:
                i *= 10**p
                i += int(c)
            p += inc
            c = self.nextchar()
        return i

    def last_token(self):
        return self.tokens[-1] if len(self.tokens) > 0 else None
    
    def tokenize(self):
        while not self.end():
            c = self.getchar()

            if c in ['(', ')', '+', '-', '*', '/', '^', '='] or c in lowercase:
                if c in lowercase and (isinstance(self.last_token(), Complex) or self.last_token() == ')')\
                   or  c == '(' and (isinstance(self.last_token(), Complex) or (isinstance(self.last_token(), str) and self.last_token() in lowercase)):
                    self.tokens.append('*') # Product

                if c in self.vars:
                    self.tokens.append(self.vars[c])
                else:
                    self.tokens.append(c)
                self.nextchar()
            elif c.isdigit():
                i = self._token_number(1, 0)
                c = self.getchar()

                if not self.end() and c == '.':
                    self.nextchar()

                i += self._token_number(-1, -1)

                lst = self.last_token()

                if lst is not None and (lst in lowercase or lst == ')'):
                    self.tokens.append('*') # Product

                self.tokens.append(i)
            elif c in whitespace:
                self.nextchar()
            else:
                raise Exception(f'Invalid token: `{c}`')
        return self.tokens
    
    def check_tok(self, check):
        if self.i < len(self.tokens) and (check(self.tokens[self.i])):
            self.i += 1
            return True
        return False

    # =; + -; * /; ^; -x; ( )
    def parse_expr(self):
        left = self.parse_add()

        while self.check_tok(lambda x: x == '='):
            right = self.parse_add()
            left = ['=', left, right]

        return left

    def parse_add(self):
        left = self.parse_times()

        while self.check_tok(lambda x: x in ['+', '-']):
            op = self.tokens[self.i - 1]
            right = self.parse_times()

            left = [op, left, right]

        return left

    def parse_times(self):
        left = self.parse_exp()

        while self.check_tok(lambda x: x in ['*', '/']):
            op = self.tokens[self.i - 1]
            right = self.parse_exp()

            left = [op, left, right]

        return left
    # TODO: Fix ()
    def parse_exp(self):
        left = self.parse_neg()

        while self.check_tok(lambda x: x == '^'):
            right = self.parse_neg()
            left = ['^', left, right]

        return left

    def parse_neg(self):
        if self.check_tok(lambda x: x == '-'):
            return ['-', self.parse_atom()]
        return self.parse_atom()

    def parse_atom(self):
        if self.check_tok(lambda x: x == '('):
            expr = self.parse_expr()
            if not self.check_tok(lambda x: x == ')'):
                raise Exception('Expected closing parenthesis (`)`) after expression')
            return expr
        else:
            self.i += 1
            return self.tokens[self.i - 1] if self.i < len(self.tokens) + 1 else None

def eval_expr(expr):
    if isinstance(expr, list) and expr[0] == '=':
        return eval_expr(expr[1]), eval_expr(expr[2])
    elif isinstance(expr, list):
        op=expr[0] 

        if op == '+':
            lhs = expr[1]
            rhs = expr[2]
            return eval_expr(lhs) + eval_expr(rhs)
        elif op == '-':
            lhs = expr[1]
            if len(expr) == 2:
                return -eval_expr(lhs)
            else:
                rhs = expr[2]
                return eval_expr(lhs) - eval_expr(rhs)
        elif op == '*':
            lhs = expr[1]
            rhs = expr[2]
            return eval_expr(lhs) * eval_expr(rhs)
        elif op == '/':
            lhs = expr[1]
            rhs = expr[2]
            return eval_expr(lhs) / eval_expr(rhs)
        elif op == '^':
            lhs = expr[1]
            rhs = expr[2]
            return eval_expr(lhs) ** eval_expr(rhs)
        else:
            return None
    elif isinstance(expr, Complex):
        return expr
    else:
        raise Exception(f'Unbound variable: `{expr}`')
