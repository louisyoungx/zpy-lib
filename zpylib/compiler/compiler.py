import re
from zpylib.grammar.token import tokens, keywords
from zpylib.grammar.type import *
from zpylib.grammar.keyword import py_invert_RESERVED, zpy_invert_RESERVED
from zpylib.grammar.builtin import builtInFunctions, invertBuiltInFunctions
from zpylib.lib import lib
import zpylib.ast.lexer as lex


class Compiler(object):

    def compile(self, file, targetType):
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
        self.varMap = self.variableMap()

    def variableMap(self):
        varMap = {}
        libMap = libCollection.map(self.data, self.targetType)
        if self.targetType == 'py':
            builtInMap = builtInFunctions
        elif self.targetType == 'zpy':
            builtInMap = invertBuiltInFunctions
        varMap.update(libMap)
        varMap.update(builtInMap)
        return varMap

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
        
        if tok.type == 'IMPORT':
            # TODO perf import dependency libs
            pass

        if tok.type in keywords:
            if self.targetType == 'py':
                reservedValue = py_invert_RESERVED[tok.type]
            elif self.targetType == 'zpy':
                reservedValue = zpy_invert_RESERVED[tok.type]
            self.subData(tok.value, reservedValue, tok.lexpos)

        if tok.type == 'NAME': 
            if tok.value in self.varMap:
                newValue = self.varMap[tok.value]
                self.subData(tok.value, newValue, tok.lexpos)
            else:
                # TODO feature do some thing
                newValue = tok.value
            
        if tok.type == 'ZNAME':
            if tok.value in self.varMap:
                newValue = self.varMap[tok.value]
                self.subData(tok.value, newValue, tok.lexpos)
            else:
                # TODO feature do some thing
                # parse some args and translate something
                newValue = tok.value

    def subData(self, oldStr, newStr, index):
        start = index + self.positionOffset
        end = start + len(oldStr)
        self.data = self.data[:start] + newStr + self.data[end:]
        self.positionOffset = self.positionOffset - (len(oldStr) - len(newStr))

class LibCollection():

    def map(self, data, targetType):
        libs = self.collect(data)
        varMap = {}
        for lib_item in libs:
            libInfo = lib.load(lib_item, targetType)
            if libInfo is not None:
                key = libInfo['name']
                value = libInfo['zpy']
                if targetType == 'py':
                    key, value = value, key
                varMap[key] = value
                for item in libInfo['functions']:
                    key = item['name']
                    value = item['zpy']
                    if targetType == 'py':
                        key, value = value, key
                    varMap[key] = value
                for item in libInfo['args']:
                    key = item['name']
                    value = item['zpy']
                    if targetType == 'py':
                        key, value = value, key
                    varMap[key] = value
        return varMap

    def collect(self, data):
        pyLibs = self.collectPy(data)
        zpyLibs = self.collectZpy(data)
        return pyLibs + zpyLibs

    @staticmethod
    def collectPy(file):
        libs = []

        import_pattern = re.compile(r'^\s*import.+$', re.M)
        import_lib = import_pattern.findall(file)

        from_pattern = re.compile(r'^\s*from.+$', re.M)
        from_lib = from_pattern.findall(file)

        for lib_item in import_lib:
            lib_str = re.search(r'(?<=import\s).+$', lib_item).group()
            lib_list = lib_str.split(',')
            for item in lib_list:
                item = item.replace(' ', '')
                libs.append(item)

        for lib_item in from_lib:
            lib_str = re.search(r'(?<=from\s).+(?=\simport)', lib_item).group()
            lib_str = lib_str.replace(' ', '')
            libs.append(lib_str)

        return libs

    @staticmethod
    def collectZpy(file):
        libs = []

        import_pattern = re.compile(r'^\s*导入.+$', re.M)
        import_lib = import_pattern.findall(file)

        from_pattern = re.compile(r'^\s*从.+$', re.M)
        from_lib = from_pattern.findall(file)

        for lib_item in import_lib:
            lib_str = re.search(r'(?<=导入\s).+$', lib_item).group()
            lib_list = lib_str.split(',')
            for item in lib_list:
                item = item.replace(' ', '')
                libs.append(item)

        for lib_item in from_lib:
            lib_str = re.search(r'(?<=从\s).+(?=\s导入)', lib_item).group()
            lib_str = lib_str.replace(' ', '')
            libs.append(lib_str)

        return libs

    @staticmethod
    def compile(file, libs, targetType='py'):
        methodList = []
        for lib_item in libs:
            info = lib.load(lib_item, targetType)
            if info is not None:
                methodList.append(info)
        for lib_item in methodList:
            file = LibCollection.replaceKey(file, lib_item['zpy'], lib_item['name'], targetType)
            for func in lib_item['functions']:
                file = LibCollection.replaceKey(file, func['zpy'], func['name'], targetType)
                if 'args' in func:
                    for arg in func['args']:
                        file = LibCollection.replaceKey(file, arg['zpy'], arg['name'], targetType)
        return file

    @staticmethod
    def replaceKey(file, key, value, targetType):
        if targetType == 'zpy':
            value, key = key, value
        pattern = eval(f"f'(?<=([^\u4e00-\u9fa5\w])){key}(?=\(.*\))'")
        file = re.sub(key, value, file, count=0, flags=0)
        return file

libCollection = LibCollection()
