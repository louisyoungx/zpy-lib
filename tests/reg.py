import re

test = '''

导入 时间'''
reg = '(?<=\s){key}(?=[\s:])'
key = '导入'
to = 'import'
dynamicReg = eval(f"f'{reg}'")
print(dynamicReg)
res = re.sub(dynamicReg, to, test, count=0, flags=0)
print(res)