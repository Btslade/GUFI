import sqlite3
import argparse
from performance_pkg import database_functions as db
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", dest='database', required=True, help = "Specify database to write to")
    parser.add_argument("--table", dest='table', default=db.CUMULATIVE_TABLE)
    args = parser.parse_args()
    return args





if __name__ == "__main__":
    args = parse_command_line_arguments()
    try:
        con = sqlite3.connect(f'{args.database}')
        db.create_database(con, args, db.CUMULATIVE_DB)
    finally:
        con.close()