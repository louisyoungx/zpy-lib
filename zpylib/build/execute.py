from .build import Build
import subprocess


def execute(filename, target_type='py'):
    building = Build(filename, target_type)
    code = building.build()
    return subprocess.call(['python', '-c', code])
