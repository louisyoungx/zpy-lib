import sys
if ".." not in sys.path: sys.path.insert(0,"..")
from zpylib import compiler

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

r = compiler.run(data, 'zpy')
print(r)