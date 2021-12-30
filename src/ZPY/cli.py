import argparse
from Build import execute, save

def main():
    parser = argparse.ArgumentParser(description='Execute Zpy program')
    subparser = parser.add_subparsers(title="Zpy", help="Zpy Toolkit")

    run_parser = subparser.add_parser('run', help='Build Zpy program')
    run_file = run_parser.add_argument('runFile', help='Taget file')

    build_parser = subparser.add_parser('build', help='Build Zpy program')
    build_file = build_parser.add_argument('buildFile', help='Taget file')
    to_py = build_parser.add_argument('-to', help='Build to Python file')
    
    args = parser.parse_args()

    try:
        args.runFile
    except Exception as e:
        file_exists = False
    else:
        file_exists = True

    try:
        args.buildFile
    except Exception as e:
        buildFile_exists = False
    else:
        buildFile_exists = True

    if buildFile_exists:
        save(args.buildFile, args.to)
    elif file_exists:
        execute(args.runFile)
    else:
        print(args)
        raise Exception("Error: Could not execute or build")

main()
