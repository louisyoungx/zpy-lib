import re
from zpylib.grammar.token import tokens, keywords
from zpylib.grammar.type import *
from zpylib.grammar.keyword import py_invert_RESERVED, zpy_invert_RESERVED
from zpylib.lib import lib
import zpylib.ast.lexer as lex

class Compiler(object):
    
    def run(self, file, targetType):
        self.file = file
        self.targetType = targetType
        self.result = ''
        if self.targetType == 'zpy':
            return self.pyToZpy(self.file)
        elif self.targetType == 'py':
            return self.zpyToPy(self.file)
        else:
            raise Exception(f"错误: 目标格式 {self.targetType} 只能是 py 或 zpy")
    
    @staticmethod
    def pyToZpy(file):
        pyFile = file
        # TODO py to zpy
        tokenHandler = TokenHandler(pyFile, 'zpy')
        zpyFile = tokenHandler.tokenize()
        return zpyFile

    @staticmethod
    def zpyToPy(file):
        zpyFile = file
        # TODO py to py
        tokenHandler = TokenHandler(zpyFile, 'py')
        pyFile = tokenHandler.tokenize()
        return pyFile

class TokenHandler():
    def __init__(self, data, targetType):
        self.targetType = targetType
        if self.targetType not in ['py', 'zpy']:
            raise Exception(f"错误: 目标格式 {self.targetType} 只能是 py 或 zpy")
        
        # Build the lexer
        self.lexer = lex.lex()
        # Give the lexer some input
        self.lexer.input(data)
        self.data = data
        self.positionOffset = 0
        self.importLib()
        
    def importLib(self):
        pass

    def tokenize(self):
        # Tokenize
        while True:
            tok = self.lexer.token()
            if tok:
                self.update(tok)
            else:
                break      # No more input
        return self.data

    def update(self, tok):
        if tok.type in keywords:
            if self.targetType == 'py':
                reservedValue = py_invert_RESERVED[tok.type]
            elif self.targetType == 'zpy':
                reservedValue = zpy_invert_RESERVED[tok.type]
            self.subData(tok.value, reservedValue, tok.lexpos)

        if tok.type == 'NAME':
            newValue = tok.value # TODO feature do some thing
            self.subData(tok.value, newValue, tok.lexpos)
        
        if tok.type == 'ZNAME':
            newValue = tok.value # TODO feature do some thing
            self.subData(tok.value, newValue, tok.lexpos)

    def subData(self, oldStr, newStr, index):
        start = index + self.positionOffset
        end = start + len(oldStr)
        self.data = self.data[:start] + newStr + self.data[end:]
        self.positionOffset = self.positionOffset - (len(oldStr) - len(newStr))


# def replaceKey(file, key, value, grammarType, targetType):
#     if targetType == 'zpy':
#         value, key = key, value
#     pattern = eval(f"f'{grammar[grammarType]}'")
#     file = re.sub(key, value, file, count=0, flags=0)
#     return file

# # operator
# def operatorCompile(file, targetType='py'):
#     for item in operator:
#         file = replaceKey(file, item, operator[item], 'operator', targetType)
#     return file

# # function
# def functionCompile(file, targetType='py'):
#     for item in function:
#         file = replaceKey(file, item, function[item], 'method', targetType)
#     return file

# # lib_item
# def libCollect(file):
#     libs = []

#     import_pattern = re.compile(grammar['lib']['import'], re.M)
#     import_lib = import_pattern.findall(file)

#     from_pattern = re.compile(grammar['lib']['from'], re.M)
#     from_lib = from_pattern.findall(file)

#     for lib_item in import_lib:
#         lib_str = re.search(grammar['lib']['import_cut'], lib_item).group()
#         lib_list = lib_str.split(',')
#         for item in lib_list:
#             item = item.replace(' ', '')
#             libs.append(item)

#     for lib_item in from_lib:
#         lib_str = re.search(grammar['lib']['from_cut'], lib_item).group()
#         lib_str = lib_str.replace(' ', '')
#         libs.append(lib_str)

#     return libs

# def libCompile(file, targetType='py'):
#     libs = libCollect(file)
#     method_list = []
#     for lib_item in libs:
#         info = lib.load(lib_item, targetType)
#         if info is not None:
#             method_list.append(info)
#     for lib_item in method_list:
#         file = replaceKey(file, lib_item['zpy'], lib_item['name'], 'method', targetType)
#         for func in lib_item['functions']:
#             file = replaceKey(file, func['zpy'], func['name'], 'method', targetType)
#             if 'args' in func:
#                 for arg in func['args']:
#                     file = replaceKey(file, arg['zpy'], arg['name'], 'method', targetType)
#     return file