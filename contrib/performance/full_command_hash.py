#!/usr/bin/env @PYTHON_INTERPRETER@
# This file is part of GUFI, which is part of MarFS, which is released
# under the BSD license.
#
#
# Copyright (c) 2017, Los Alamos National Security (LANS), LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# From Los Alamos National Security, LLC:
# LA-CC-15-039
#
# Copyright (c) 2017, Los Alamos National Security, LLC All rights reserved.
# Copyright 2017. Los Alamos National Security, LLC. This software was produced
# under U.S. Government contract DE-AC52-06NA25396 for Los Alamos National
# Laboratory (LANL), which is operated by Los Alamos National Security, LLC for
# the U.S. Department of Energy. The U.S. Government has rights to use,
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR LOS
# ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is
# modified to produce derivative works, such modified software should be
# clearly marked, so as not to confuse it with the version available from
# LANL.
#
# THIS SOFTWARE IS PROVIDED BY LOS ALAMOS NATIONAL SECURITY, LLC AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL LOS ALAMOS NATIONAL SECURITY, LLC OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.



'''create full hash based on machine and gufi hash'''
import argparse
import sqlite3

from performance_pkg import database_functions as db
from performance_pkg import hashing_functions as hf

def add_to_full_hash_table(con: sqlite3.Connection,
                           full_hash: str,
                           args: argparse.Namespace):
    '''
    Add data to full hash table

    Inputs
    ------
    con : sqlite3.Connectioin
        connection to sql database containing the full hash table
    hash : str
        hash generated with machine and gufi command hash as inputs
    args : argparse.Namespace
        arguments user provided at command line

    Returns
    -------
    None
    '''
    full_hash_pragma = db.FULL_HASH_COLUMNS.replace("'", "")
    con.execute(f'''
                 INSERT INTO {args.table} ({full_hash_pragma})
                 VALUES ("{full_hash}", "{args.hash_type}",
                 "{args.machine_hash}", "{args.gufi_hash}", "{args.notes}");
                 ''')


def parse_arguments(argv: list = None):
    '''
    parse arguments provided inside of ArgumentParser object

    ...

    Input
    -----
    argv : list
        list of arguments to parse

    Returns
    -------
    parsed argument list
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--hashdb",
                        default=hf.HASH_DATABASE_FILE,
                        metavar="filename",
                        help="Database file to save this configuration to")
    parser.add_argument("--hash_type",
                        default="md5",
                        choices=hf.Hashes.keys(),
                        metavar="hash_function",
                        help="Hashing method to use")
    parser.add_argument("--override",
                        default=None,
                        metavar="basename",
                        help="Database name. Overrides machine and gufi hash")
    parser.add_argument("--machine_hash",
                        metavar="machine_hash",
                        help="Hash of machine configuration",
                        required=True)
    parser.add_argument("--gufi_hash",
                        metavar="gufi_hash",
                        help="Hash of GUFI command",
                        required=True)
    parser.add_argument("--notes",
                        default="",
                        dest="notes",
                        help="Additional notes")
    parser.add_argument("--table",
                        dest="table",
                        default=hf.FULL_HASH_TABLE)
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_arguments()
    db.check_if_database_exists(args.hashdb, db.HASH_DB)
    
    if args.override:
        combined_hash = args.override
    else:
        combined_hash = hf.hash_all_values(args)

    try:
        known_hashes = sqlite3.connect(args.hashdb)
        if known_hashes.execute(f"SELECT COUNT({db.COMBINED_HASH_COL}) " +
                                f"FROM {hf.FULL_HASH_TABLE} " +
                                f"WHERE {db.COMBINED_HASH_COL} == '{combined_hash}';"
                                ).fetchall()[0][0] == 0:
            add_to_full_hash_table(known_hashes, combined_hash, args)
            known_hashes.commit()
    finally:
        known_hashes.close()
    # TODO find out which GUFI command was used to generate this combined hash
    print(f'{combined_hash}')
