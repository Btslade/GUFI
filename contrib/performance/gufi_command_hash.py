import argparse
from performance_pkg import hashing_functions as hf
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-g' "--gufi", dest = "gufi_command",  help="What gufi command you used", required= True )
    parser.add_argument("-s", "-S", "--summary", dest = "S", default = "", help="Summary command", required = True)
    parser.add_argument("-e", "-E", "--entires", dest = "E", default = "", help="Name of machine")
    parser.add_argument("-t", "--tree", dest = "tree",  help="What tree you are running on", required= True)
    parser.add_argument('--hash', "--print", default='md5', dest = "hash", choices=hf.Hashes.keys(), help = "Hashing mehtods available to use")
    parser.add_argument("--notes", default="", dest = "notes",  help = "Additional notes")
    args = parser.parse_args()
    return args



def main():
    args = parse_command_line_arguments()
    hash_to_use = hf.hash_gufi_command_values(args)
    print(f'Resulting hash: {hash_to_use}')
    hf.add_to_gufi_command_table(hash_to_use, args)

if __name__ == "__main__":
    main()