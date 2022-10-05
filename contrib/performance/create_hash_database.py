import sqlite3
import argparse
from performance_pkg import hashing_functions as hf
from performance_pkg import create_table_functions as ct
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", dest='database', default=hf.DATABASE_FILE, help = "Specify database to write to other than the default")
    args = parser.parse_args()
    return args





if __name__ == "__main__":
    args = parse_command_line_arguments()
    try:
        con = sqlite3.connect(f'{args.database}')
        ct.create_machine_table(con)
        ct.create_gufi_command_table(con)
        ct.create_full_hash_table(con)
        con.commit()
    finally:
        con.close()
