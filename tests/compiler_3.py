import sys
if ".." not in sys.path: sys.path.insert(0,"..")
from zpylib import compiler, execute

# Test it out
data = """
# 数字形态转换
阿拉伯数字 = '127686688665'
汉字数字 = "零一二三四五六七八九"
对于 数字 在 阿拉伯数字:
    打印(汉字数字[评估(数字)], end="")
"""

r = compiler.compile(data, 'py')
print(r)
execute(r, 'py')