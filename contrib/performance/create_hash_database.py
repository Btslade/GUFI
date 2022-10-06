import sqlite3
import argparse
from performance_pkg import hashing_functions as hf
from performance_pkg import database_functions as db
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", dest='database', default=hf.HASH_DATABASE_FILE, help = "Specify database to write to other than the default")
    parser.add_argument('--machine_table', dest='machine_table', default= hf.MACHINE_HASH_TABLE)
    parser.add_argument('--gufi_table', dest='gufi_table', default = hf.GUFI_COMMAND_TABLE)
    parser.add_argument('--full_table', dest='full_table', default=hf.FULL_HASH_TABLE)
    args = parser.parse_args()
    return args





if __name__ == "__main__":
    args = parse_command_line_arguments()
    try:
        con = sqlite3.connect(f'{args.database}')
        db.create_database(con, args, db.HASH_DB)
    finally:
        con.close()
