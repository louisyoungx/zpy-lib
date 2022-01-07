import sys
if ".." not in sys.path: sys.path.insert(0,"..")
import zpylib.ast.lexer as lex
from zpylib.grammar import *

# Test it out
data = """
# TEST
Apple = 3 + 4 * 10 + -20 *2
def Print(what):
    if True:
        go(what + 10)
    如果 错:
    x = 'yoo what's up'
'''what fuck'''
{:.2f}.format(name)
"""


class Compiler():
    def __init__(self, data):
        # Build the lexer
        self.lexer = lex.lex()
        # Give the lexer some input
        self.lexer.input(data)
        self.data = data
        self.positionOffset = 0
        self.tokenize()

    def tokenize(self):
        print(self.data)
        # Tokenize
        while True:
            tok = self.lexer.token()
            if tok:
                self.update(tok)
            else:
                break      # No more input
        print(self.data)

    def update(self, tok):
        #print(tok.type, tok.value, tok.lexpos, tok.lineno)
        if tok.type == 'NAME':
            self.subData(tok.value, tok.value+'_', tok.lexpos)

    def subData(self, oldStr, newStr, index):
        start = index + self.positionOffset
        end = start + len(oldStr)
        self.data = self.data[:start] + newStr + self.data[end:]
        self.positionOffset = self.positionOffset - (len(oldStr) - len(newStr))

Compiler(data)
