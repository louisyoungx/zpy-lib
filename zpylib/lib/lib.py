import os
import json
from .map import MAP

# 依赖
class Lib(object):
    def __init__(self):
        self.path = self.getPath()
        self.pyLib, self.zpyLib = self.libList()

    # 当前所在路径
    def getPath(self):
        project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir = '/Lib'
        path = project + dir
        return path
    
    # 库列表
    def libList(self):
        zpyLib = MAP
        pyLib = {}
        for key in MAP:
            pyLib[MAP[key]] = key
        return pyLib, zpyLib
    
    # 导出依赖项映射表
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

    # 导出json文件内容到字典格式
    def loadFile(self, filename):
        file = self.readFile(filename)
        return json.loads(file)

    # 读取文件内容
    def readFile(self, filename):
        try:
            with open(self.path + '/' + filename) as raw:
                code = raw.read()
                raw.close()
            return code
        except Exception as e:
            raise Exception(f"错误: 找不到文件 {filename}\n目录: {self.path}")