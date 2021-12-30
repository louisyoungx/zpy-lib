import re
from Grammar import function, grammar, operator
from Lib import lib


def replaceKey(file, key, value, grammarType, target_type):
    if target_type == 'zpy':
        value, key = key, value
    pattern = eval(f"f'{grammar[grammarType]}'")
    file = re.sub(key, value, file, count=0, flags=0)
    return file

# operator
def operatorCompile(file, target_type='py'):
    for item in operator:
        file = replaceKey(file, item, operator[item], 'operator', target_type)
    return file

# function
def functionCompile(file, target_type='py'):
    for item in function:
        file = replaceKey(file, item, function[item], 'method', target_type)
    return file

# lib_item
def libCollect(file):
    libs = []

    import_pattern = re.compile(grammar['lib']['import'], re.M)
    import_lib = import_pattern.findall(file)

    from_pattern = re.compile(grammar['lib']['from'], re.M)
    from_lib = from_pattern.findall(file)

    for lib_item in import_lib:
        lib_str = re.search(grammar['lib']['import_cut'], lib_item).group()
        lib_list = lib_str.split(',')
        for item in lib_list:
            item = item.replace(' ', '')
            libs.append(item)

    for lib_item in from_lib:
        lib_str = re.search(grammar['lib']['from_cut'], lib_item).group()
        lib_str = lib_str.replace(' ', '')
        libs.append(lib_str)

    return libs

def libCompile(file, target_type='py'):
    libs = libCollect(file)
    method_list = []
    for lib_item in libs:
        info = lib.load(lib_item, target_type)
        if info is not None:
            method_list.append(info)
    for lib_item in method_list:
        file = replaceKey(file, lib_item['zpy'], lib_item['name'], 'method', target_type)
        for func in lib_item['functions']:
            file = replaceKey(file, func['zpy'], func['name'], 'method', target_type)
            if 'args' in func:
                for arg in func['args']:
                    file = replaceKey(file, arg['zpy'], arg['name'], 'method', target_type)
    return file

zpy_file = '''导入 时间, 随机, 请求
导入 app
    导入 app 2
从 flask 导入 app
打印(时间.时间)
获取线程cpu时钟id()
'''

zpy_file = operatorCompile(zpy_file, 'py')
zpy_file = functionCompile(zpy_file, 'py')
zpy_file = libCompile(zpy_file, 'py')
print(zpy_file)
