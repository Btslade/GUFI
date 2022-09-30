import argparse

from performance_pkg import graphing_functions as gf

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database", dest="database", help="Database to read from")
    parser.add_argument("config", nargs='+', help="Config file(s)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    for filename in args.config:
        gf.define_graph(filename, args.database)
