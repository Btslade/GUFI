from base64 import urlsafe_b64encode, urlsafe_b64decode
from binascii import hexlify, unhexlify
import hashlib
import os
import sqlite3

# copied from trace_anonymizer.py
# Known hashes
Hashes = {
    'md5'         : hashlib.md5,
    'sha1'        : hashlib.sha1,
    'sha224'      : hashlib.sha224,
    'sha256'      : hashlib.sha256,
    'sha384'      : hashlib.sha384,
    'sha512'      : hashlib.sha512,
}

#


def add_to_table(hash, args):
    if args.database != None:
        con = sqlite3.connect(f'{args.database}')
    else:
        con = sqlite3.connect('hash_database.db')
    cur = con.cursor()
    table = cur.execute("PRAGMA table_info(machine);").fetchall()
    if table == []:
        create_table_str = "'hash', 'cpu', 'ram', 'machine_name', 'hash_type', 'notes',  PRIMARY KEY (hash)"
        cur.execute(f"CREATE TABLE machine ({create_table_str});")
    # https://softhints.com/python-3-convert-dictionary-to-sql-insert/
    
    sql = f"INSERT INTO machine ('hash', 'cpu', 'ram', 'machine_name', 'hash_type', 'notes') VALUES ('{hash}', '{args.cpu}', '{args.ram}', '{args.machine_name}', '{args.hash}', '{args.notes}');"
    
    try:
        con.execute(sql)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    cur.close()
    con.close()

def add_to_machine_table(hash, args):
    if args.database != None:
        con = sqlite3.connect(f'{args.database}')
    else:
        con = sqlite3.connect('hash_database.db')
    cur = con.cursor()
    table = cur.execute("PRAGMA table_info(machine);").fetchall()
    if table == []:
        create_table_str = "'hash', 'cpu', 'ram', 'machine_name', 'hash_type', 'notes',  PRIMARY KEY (hash)"
        cur.execute(f"CREATE TABLE machine ({create_table_str});")
    # https://softhints.com/python-3-convert-dictionary-to-sql-insert/
    
    sql = f"INSERT INTO machine ('hash', 'cpu', 'ram', 'machine_name', 'hash_type', 'notes') VALUES ('{hash}', '{args.cpu}', '{args.ram}', '{args.machine_name}', '{args.hash}', '{args.notes}');"
    
    try:
        con.execute(sql)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    cur.close()
    con.close()

#anonymize(column, hash=Hashes[args.hash])

def add_to_gufi_command_table(hash, args):
    if args.database != None:
        con = sqlite3.connect(f'{args.database}')
    else:
        con = sqlite3.connect('hash_database.db')
    cur = con.cursor()
    table = cur.execute("PRAGMA table_info(gufi_command);").fetchall()
    if table == []:
        create_table_str = "'hash', 'gufi', '-S', '-E', 'tree', 'hash_type', 'notes', PRIMARY KEY (hash)"
        cur.execute(f"CREATE TABLE gufi_command ({create_table_str});")
    # https://softhints.com/python-3-convert-dictionary-to-sql-insert/
    
    sql = f"INSERT INTO gufi_command ('hash', 'gufi', '-S', '-E', 'tree', 'hash_type', 'notes') VALUES ('{hash}', '{args.gufi_command}', '{args.S}', '{args.E}', '{args.tree}', '{args.hash}', '{args.notes}');"
    
    try:
        con.execute(sql)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    cur.close()
    con.close()


def add_to_full_hash_table(hash, args):
    if args.database != None:
        con = sqlite3.connect(f'{args.database}')
    else:
        con = sqlite3.connect('hash_database.db')
    cur = con.cursor()
    table = cur.execute("PRAGMA table_info(full_hash);").fetchall()
    if table == []:
        create_table_str = "'combined_hash', 'machine_hash', 'gufi_hash', 'hash_type', 'notes',  PRIMARY KEY (combined_hash)"
        cur.execute(f"CREATE TABLE full_hash ({create_table_str});")
    # https://softhints.com/python-3-convert-dictionary-to-sql-insert/
    
    sql = f"INSERT INTO full_hash ('combined_hash', 'machine_hash', 'gufi_hash', 'hash_type', 'notes') VALUES ('{hash}', '{args.machine_hash}', '{args.gufi_hash}',  '{args.hash}', '{args.notes}');"
    
    try:
        con.execute(sql)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    cur.close()
    con.close()

def hash_machine_values(args):
    hash = Hashes[args.hash]
    string = f"{args.cpu} {args.ram} {args.machine_name}"
    hash_to_use = hash(string.encode()).hexdigest()
    return hash_to_use

def hash_gufi_command_values(args):
    hash = Hashes[args.hash]
    string = f"{args.gufi_command} {args.S} {args.E}"
    hash_to_use = hash(string.encode()).hexdigest()
    return hash_to_use

def hash_all_values(args):
    hash = Hashes[args.hash]
    string = f"{args.gufi_hash} {args.machine_hash}"
    hash_to_use = hash(string.encode()).hexdigest()
    return hash_to_use