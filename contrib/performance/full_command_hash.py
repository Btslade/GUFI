import sqlite3
import argparse
from performance_pkg import hashing_functions as hf


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--hashdb',
                        default=hf.DATABASE_FILE,
                        metavar='filename',
                        help='Database file to save this configuration to')
    parser.add_argument('--hash',
                        default='md5', choices=hf.Hashes.keys(),
                        metavar='hash_function',
                        help='Hashing method to use')
    parser.add_argument('--override',
                        default=None,
                        metavar='basename',
                        help='Database name. Overrides machine_hash and gufi_hash')
    parser.add_argument('--machine_hash',
                        metavar='machine_hash',
                        help='Hash of machine configuration',
                        required= True)
    parser.add_argument('--gufi_hash',
                        metavar='gufi_hash',
                        help='Hash of GUFI command',
                        required = True)
    parser.add_argument( "--notes",
                        default="", 
                        dest = "notes",  
                        help = "Additional notes")

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_command_line_arguments()

    if args.override:
        combined_hash = args.override
    else:
        combined_hash = hf.hash_all_values(args)

    try:
        
        # open the database of all known hashes
        known_hashes = sqlite3.connect(args.hashdb)
        # check if this hash already exists THIS IS BEING DONE BELOW
        if known_hashes.execute(f"SELECT COUNT({hf.COMBINED_HASH_COL}) FROM {hf.FULL_HASH_TABLE} WHERE {hf.COMBINED_HASH_COL} == '{combined_hash}';").fetchall()[0][0] == 0:
            hf.add_to_full_hash_table(known_hashes, combined_hash, args)
            known_hashes.commit()
    finally:
        known_hashes.close()
    # TODO: find out which GUFI command was used to generate this combined hash
    print(f'Resulting hash: {combined_hash}')



