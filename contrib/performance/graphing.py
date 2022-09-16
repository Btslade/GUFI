
from performance_pkg import graphing_functions as gf
import sys
import os

if len(sys.argv) < 2:
    print("Please provide a path to an ini file or a directory containing ini files")

for i in sys.argv[1:]:
    if i[-4:] == '.ini':
        gf.define_graph(i)
    else: #assume its a directory with configs inside
        try:
            configs = os.listdir(i)
        except FileNotFoundError:
            print(f'File \'{i}\' could not be found, Continuing')
            continue
        except NotADirectoryError:
            print(f'File \'{i}\' is not a directory or a .ini file, Exiting')
            exit()
        if len(configs) == 0:
            print(f'Path \'{i}\' is empty ')
            continue
        else:
            for j in configs:
                if j[-4:] != '.ini': #skip file if not an ini
                    continue
                else:
                    full_path = os.path.join(i, j)
                    gf.define_graph(full_path)