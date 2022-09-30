import argparse
import sqlite3
import sys

from performance_pkg import extraction_functions as ef
from performance_pkg import hashing_functions as hf

def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hashdb',
                        default='hash_database.db',
                        metavar='filename',
                        help='Database file to save this configuration to')
    parser.add_argument('--hash',
                        default='md5', choices=hf.Hashes.keys(),
                        help='Hashing method to use')
    parser.add_argument('--table',
                        default='t',
                        metavar='name',
                        help='Name of table to write parsed input to')
    parser.add_argument('-n', '--notes',
                        default='',
                        help='Additional notes')
    parser.add_argument('--path',
                        default=None,
                        help='Directory to create new database files. Defaults to the current directory')
    parser.add_argument('--override',
                        default=None,
                        metavar='basename',
                        help='Database name. Overrides machine_hash and gufi_hash')
    parser.add_argument('machine_hash',
                        help='Hash of machine configuration')
    parser.add_argument('gufi_hash',
                        help='Hash of GUFI command')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line_arguments()

    # generate filename of debug data database
    if args.override:
        combined_hash = args.override
    else:
        combined_hash = hf.hash_all_values(args)

    try:
        # open the database of all known hashes
        known_hashes = sqlite3.connect(args.hashdb)

        # add this configuration to the list of configurations
        # check if this hash already exists
        if known_hashes.execute(f"SELECT COUNT({hf.COMBINED_HASH_COL}) FROM {hf.FULL_HASH_TABLE} WHERE {hf.COMBINED_HASH_COL} == '{combined_hash}';").fetchall()[0] == 0:
            hf.add_to_full_hash_table(known_hashes, combined_hash, args)
    finally:
        known_hashes.close()

    # TODO: find out which GUFI command was used to generate this gufi_hash

    # fixed/known format
    db_name = f'{combined_hash}.db'
    if args.path:
        db_name=f'{args.path}/{db_name}'
        print(f'Writing to {db_name}')

    try:
        # open the database containing the actual data
        data_con = sqlite3.connect(db_name)

        # TODO: if this database didn't exist before it was opened, set it up
        # ef.gufi_query_setup

        # if gufi_hash came from gufi_query
        ef.gufi_query(data_con, sys.stdin, args.table)
    finally:
        data_con.close()
