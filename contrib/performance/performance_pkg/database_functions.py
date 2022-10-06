from . import extraction_functions as ef
import os

HASH_DB = 'create_hash_database.py'
CUMULATIVE_DB = 'create_cumulative_times_database.py'
CUMULATIVE_TABLE = 'cumulative_times'

def check_if_database_exists(database, util):
        if not os.path.isfile(database):
            print(f"'{database}' does not exist!!!\nCreate using: {util}")
            exit()

def create_database(con, args, db):
        if db == HASH_DB:
            create_machine_table(con, args.machine_table)
            create_gufi_command_table(con, args.gufi_table)
            create_full_hash_table(con, args.full_table)
        if db == CUMULATIVE_DB:
            create_times_table(con, ef.GUFI_QUERY_COLUMNS, args.table)
        con.commit()

def create_machine_table(con, table_name):
    create_table_str = "'hash', 'cpu', 'ram', 'machine_name', 'hash_type', 'notes',  PRIMARY KEY (hash)"
    con.execute(f"CREATE TABLE {table_name} ({create_table_str});")
    
def create_gufi_command_table(con, table_name):
    create_table_str = "'hash', 'gufi', 'S', 'E', 'tree', 'hash_type', 'notes', PRIMARY KEY (hash)"
    con.execute(f"CREATE TABLE {table_name} ({create_table_str});")

def create_full_hash_table(con, table_name):
    create_table_str = "'combined_hash', 'machine_hash', 'gufi_hash', 'hash_type', 'notes',  PRIMARY KEY (combined_hash)"
    con.execute(f"CREATE TABLE {table_name} ({create_table_str});")

def process_table_string(create_table_str):
    create_table_str = create_table_str.replace("'commit' FLOAT", "'commit'")
    create_table_str = create_table_str.replace("'branch' FLOAT", "'branch'")
    create_table_str = create_table_str.replace("'Threads run' FLOAT,", "'Threads run' INT,")
    create_table_str = create_table_str.replace("'Queries performed' FLOAT,", "'Queries performed' INT,")
    create_table_str = create_table_str.replace("'Rows printed to stdout or outfiles' FLOAT,", "'Rows printed to stdout or outfiles' INT,")
    return create_table_str.replace("'Real time (main)' FLOAT,", "'Real time (main)' FLOAT") 
    

def create_times_table(con,columns, table_name):
    create_table_str = ''
    for x in columns:
        create_table_str += f"'{x[0]}' FLOAT,"
    #create_table_str = ' FLOAT,'.join("'" + str(x) + "'" for x in columns)
    create_table_str = process_table_string(create_table_str)
    con.execute(f"CREATE TABLE {table_name} ({create_table_str});")