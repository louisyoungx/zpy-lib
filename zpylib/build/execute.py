import subprocess


def execute(code, target_type='py'):
    return subprocess.call(['python', '-c', code])
