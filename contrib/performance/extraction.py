import argparse
import sqlite3
import sys

from performance_pkg import extraction_functions as ef
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
    parser.add_argument('--table',
                        default='cumulative_times',
                        metavar='name',
                        help='Name of table to write parsed input to')
    parser.add_argument('--notes',
                        default='',
                        help='Additional notes')
    parser.add_argument('--path',
                        default=None,
                        metavar='dir',
                        help='Directory to create new database files. Defaults to the current directory')
    parser.add_argument('--override',
                        default=None,
                        metavar='basename',
                        help='Database name. Overrides machine_hash and gufi_hash')
    parser.add_argument('--machine_hash',
                        metavar='machine_hash',
                        help='Hash of machine configuration')
    parser.add_argument('--gufi_hash',
                        metavar='gufi_hash',
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
        print(known_hashes.execute(f"SELECT COUNT({hf.COMBINED_HASH_COL}) FROM {hf.FULL_HASH_TABLE} WHERE {hf.COMBINED_HASH_COL} == '{combined_hash}';").fetchall())
        # check if this hash already exists THIS IS BEING DONE BELOW
        if known_hashes.execute(f"SELECT COUNT({hf.COMBINED_HASH_COL}) FROM {hf.FULL_HASH_TABLE} WHERE {hf.COMBINED_HASH_COL} == '{combined_hash}';").fetchall()[0][0] == 0:
            hf.add_to_full_hash_table(known_hashes, combined_hash, args)
            known_hashes.commit()
    finally:
        known_hashes.close()

    # TODO: find out which GUFI command was used to generate this combined hash

    # fixed/known format
    if args.path:
        combined_hash=f'{args.path}/{combined_hash}.db'
        print(f'Writing to {combined_hash}')



    try:
        # open the database containing the actual data
        # TODO: Check if database exists, if not error out. (Make util files to create database)
        
        
        #TODO: check if file exists 
        
        data_con = sqlite3.connect(f'{combined_hash}.db')

        # TODO: Run checks below 
        
        '''
        check if file exists
        check if database
        check if tables exist
        check if tables have columns
        '''

        # if gufi_hash came from gufi_query
        ef.gufi_query(data_con, sys.stdin, args.table)
        data_con.commit()
    finally:
        data_con.close()
