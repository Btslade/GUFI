import argparse
import sqlite3
import sys

from performance_pkg import extraction_functions as ef
from performance_pkg import hashing_functions as hf
from performance_pkg import create_table_functions as ct



def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--combined_hash',
                        metavar='combined_hash',
                        help='Combined hash ',
                        required = True)
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

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line_arguments()
    if args.path:
        args.combined_hash=f'{args.path}/{args.combined_hash}.db'
        print(f'Writing to {args.combined_hash}')

    try:
        # open the database containing the actual data
        # TODO: Check if database exists, if not error out. (Make util files to create database)
        
        
        #TODO: check if file exists 
        
        data_con = sqlite3.connect(f'{args.combined_hash}.db')
        
        #Create table inside of new hashed database
        table_name = args.table
        table = data_con.execute(f"PRAGMA table_info({table_name});").fetchall()
        if table == []:
            ct.create_times_table(data_con, ef.GUFI_QUERY_COLUMNS, table_name)

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
