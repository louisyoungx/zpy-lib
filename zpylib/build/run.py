from .build import Build
from .execute import execute

# 传入文件名，目标格式，生成代码字符串，执行
def run(filename, targetType):
    building = Build(filename, targetType)
    code = building.build()
    execute(code, targetType)
