import os
from zpylib.compiler import compiler


class Build(object):

    def __init__(self, filename, target_type):
        self.cwd = os.getcwd()
        self.filename = filename
        self.target_type = target_type
        self.file_type = self.getFileType()
        self.file = self.readFile()
        self.build()

    def getFileType(self):
        return self.filename.split('.')[1]

    def readFile(self):
        try:
            with open(self.filename) as raw:
                script = raw.read()
                raw.close()
            return script
        except Exception as e:
            raise Exception(f"错误: 找不到文件 {self.filename}\n目录: {self.cwd}")

    def build(self):
        if self.target_type and self.target_type not in ['py', 'zpy']:
            raise Exception(f"错误: 目标格式 {self.target_type} 只能是 py 或 zpy")
            return
        elif self.file_type not in ['py', 'zpy']:
            raise Exception(f"错误: 文件格式 {self.file_type} 只能是 py 或 zpy")
            return
        elif self.target_type == self.file_type:
            print("警告: 原格式与目标格式相同")
            return
        elif self.target_type is None:
            if self.file_type == 'zpy': self.target_type ='py'
            elif self.file_type == 'py': self.target_type ='zpy'
            else: raise Exception(f"错误: 文件格式 {self.file_type} 只能是 py 或 zpy")

        result = compiler.run(self.file, self.target_type)
        return result
