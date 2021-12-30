import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo')
sub = parser.add_subparsers()
for i in range(1,4):
    sp = sub.add_parser('cmd%i'%i)
    sp.add_argument('--foo%i'%i) # optionals have to be distinct

rest = '--foo 0 cmd2 --foo2 2 cmd3 --foo3 3 cmd1 --foo1 1'.split() # or sys.argv
args = argparse.Namespace()
while rest:
    args, rest =  parser.parse_known_args(rest,namespace=args)
    print(args, rest)