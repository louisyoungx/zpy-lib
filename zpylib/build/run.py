from .build import Build

def run(filename, targetType):
    building = Build(filename, targetType)
    code = building.build()