
from performance_pkg import graphing_functions as gf
import os
import argparse


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', "--config", dest = "config", nargs='+', help="Config File or dirctory containing ", default=[] )
    parser.add_argument("-d", "--database", dest = "database",  help="Database to read from", required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_command_line_arguments()
    if len(args.config) == 0:
        gf.define_graph('', args.database)
    for i in args.config:
        if i[-4:] == '.ini' and os.path.isfile(i):
            gf.define_graph(i, args.database)
        elif os.path.isdir(i): 
            configs = os.listdir(i)
            if len(configs) == 0:
                print(f'Path \'{i}\' is empty ')
                continue
            else:
                for j in configs:
                    if j[-4:] != '.ini': #skip file if not an ini
                        continue
                    else:
                        full_path = os.path.join(i, j)
                        gf.define_graph(full_path, args.database)
        elif os.path.isfile(i):
            print(f"'{i}' is not an ini file, Skipping...")
            continue
        else:
            print(f"'{i}' does not exist, Skipping...")
            continue
    

if __name__ == "__main__":
    main()