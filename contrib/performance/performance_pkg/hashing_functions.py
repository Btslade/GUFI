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

FULL_HASH_TABLE   = 'full_hash'
COMBINED_HASH_COL = 'combined_hash'
DATABASE_FILE = 'performance_configurations.db'


def add_to_table(con, hash):
    con.execute(f'INSERT INTO machine (hash, cpu, ram, machine_name, hash_type, notes) VALUES ("{hash}", "{args.cpu}", "{args.ram}", "{args.machine_name}", "{args.hash}", "{args.notes}");')

def add_to_machine_table(con, hash, args):
    con.execute(f'INSERT INTO machine (hash, cpu, ram, machine_name, hash_type, notes) VALUES ("{hash}", "{args.cpu}", "{args.ram}", "{args.machine_name}", "{args.hash}", "{args.notes}");')

def add_to_gufi_command_table(con, hash, args):
    con.execute(f'INSERT INTO gufi_command (hash, gufi, S, E, tree, hash_type, notes) VALUES ("{hash}", "{args.gufi_command}", "{args.S}", "{args.E}", "{args.tree}", "{args.hash}", "{args.notes}");')

def add_to_full_hash_table(con, full_hash, args):
    con.execute(f'INSERT INTO {FULL_HASH_TABLE} ({COMBINED_HASH_COL}, machine_hash, gufi_hash, hash_type, notes) VALUES ("{full_hash}", "{args.machine_hash}", "{args.gufi_hash}", "{args.hash}", "{args.notes}");')

def hash_machine_config(args):
    string = f'{args.cpu} {args.ram} {args.machine_name}'
    return Hashes[args.hash](string.encode()).hexdigest()

def hash_gufi_command(args):
    string = f'{args.gufi_command} {args.S} {args.E}'
    return Hashes[args.hash](string.encode()).hexdigest()

def hash_all_values(args):
    string = f'{args.gufi_hash} {args.machine_hash}'
    return Hashes[args.hash](string.encode()).hexdigest()
