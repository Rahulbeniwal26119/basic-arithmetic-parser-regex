from gc import collect
import re 
import collections
from typing import OrderedDict 


NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pattern = re.compile('|'.join(
    [NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]
))

# Tokenizer
# namedtuple uses less memory than dict 

Token = collections.namedtuple('Token', ['type', 'value'])

def tokenizer(text):
    # scanner method repeatdly matches the pattern against 
    # the regex untill no match is found 
    scanner = master_pattern.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok 
            

class Parser:
    
    def parse(self, text):
        self.tokens = tokenizer(text)
        self.token = None 
        self.nexttoken = None
        self.order_list = []
        self._advance()
        return self.expr() 
    
    
    
    def _advance(self):
        tok = next(self.tokens, None)
        '''Advance one token ahead'''
        self.tok, self.nexttoken = self.nexttoken, tok

    def __accept(self, toktype):
        if self.nexttoken and self.nexttoken.type == toktype:
            self._advance()
            return True 
        return False
    
    def _except(self, toktype):
        if not self.__accept(toktype):
            raise SyntaxError('Error -> Expected ' + toktype)
    
    def expr(self):
        exprval = self.term()
        self.order_list.append(exprval)
        while self.__accept('PLUS') or self.__accept('MINUS') \
            or self.__accept('RPAREN'):
            
            # token is ) then return the calculated value in a () 
            if self.tok.type == 'RPAREN':
                return exprval
            op = self.tok.type 
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right
        return exprval 
    
    
    def term(self):
        termval = self.factor()
        while self.__accept('TIMES') or self.__accept("DIVIDE"):
            op = self.tok.type
            right = self.factor() # get the operand 
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval
    
    
    def factor(self):
        if self.__accept('NUM'):
            val = self.tok.value
            return int(val)
        elif self.__accept('LPAREN'):
            exprval = self.expr()
            return exprval
        else:
            raise SyntaxError('Error -> Expected NUM or LPAREN')
        