import sys
from performance_pkg import extraction_functions as ef 
import argparse
from performance_pkg import hashing_functions as hf
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', "--machine", dest = "machine_hash",  help="What machine hash to use", required=True )
    parser.add_argument("-g", "--gufi", dest = "gufi_hash",  help="", required=True)
    parser.add_argument("--hash", default="md5", dest = "hash", choices=hf.Hashes.keys(), help = "Hashing method to use")
    parser.add_argument("-n", "--notes", default="None", dest = "notes",  help = "Additional notes")
    parser.add_argument("--database", dest='database', help = "Specify database to write to other than the default")
    args = parser.parse_args()
    return args




#for key, val in zip(d.keys(), d.values()):
#    print(key)
#    print(val)


def main():
    args = parse_command_line_arguments()
    command_output = sys.stdin.read()
    hash_to_use = hf.hash_all_values(args)
    print(f'Resulting hash: {hash_to_use}')
    hf.add_to_full_hash_table(hash_to_use, args)
    ef.gufi_query(command_output, hash_to_use)

if __name__ == "__main__":
    main()



