import os
import json
from .info import info


class Lib(object):
    def __init__(self):
        self.path = self.getPath()
        self.pyLib, self.zpyLib = self.libList()

    def getPath(self):
        project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir = '/Lib'
        path = project + dir
        return path
    
    def libList(self):
        zpyLib = info
        pyLib = {}
        for key in info:
            pyLib[info[key]] = key
        return pyLib, zpyLib
    
    def load(self, lib, target_type='py'):
        if target_type == 'py':
            if lib in self.zpyLib:
                filename = self.zpyLib[lib] + '.json'
                return self.loadFile(filename)
            else:
                return None
        elif target_type == 'zpy':
            if lib in self.pyLib:
                filename = lib + '.json'
                return self.loadFile(filename)
            else:
                return None
        else:
            raise Exception(f"错误: 目标格式 {self.target_type} 只能是 py 或 zpy")

    def loadFile(self, filename):
        file = self.readFile(filename)
        return json.loads(file)

    def readFile(self, filename):
        try:
            with open(self.path + '/' + filename) as raw:
                script = raw.read()
                raw.close()
            return script
        except Exception as e:
            raise Exception(f"错误: 找不到文件 {filename}\n目录: {self.path}")