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



# pylint: disable=import-error, invalid-name, wrong-import-position
'''generate hash based on machine characteristics provided by user'''
import argparse
import sqlite3

from performance_pkg import database_functions as db
from performance_pkg import hashing_functions as hf

# pylint: enable=import-error, invalid-name, wrong-import-position
def add_to_machine_table(con: sqlite3.Connection,
                         hash: str,
                         args: argparse.Namespace):
    '''
    Add data to machine table

    Inputs
    ------
    con : sqlite3.Connectioin
        connection to sql database containing the machine table
    hash : str
        hash describing mahcine characteristics
    args : argparse.Namespace
        arguments user provided at command line

    Returns
    -------
    None
    '''
    machine_pragma = db.MACHINE_COLUMNS.replace("'", "")
    con.execute(f'''
                 INSERT INTO {args.table} ({machine_pragma})
                 VALUES ("{hash}", "{args.hash_type}", "{args.machine_name}",
                 "{args.cpu}", "{args.cores_available}", "{args.ram}",
                 "{args.storage_device}", "{args.sd_notes}", "{args.notes}");
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
    parser.add_argument("--hash_type",
                        default="md5",
                        dest="hash_type",
                        choices=hf.HASHES.keys(),
                        help="Hashing method to use")
    parser.add_argument("-m", "--machine", "--machine_name",
                        dest="machine_name",
                        help="Name of machine",
                        required=True)
    parser.add_argument("--cpu",
                        dest="cpu",
                        help="cpu of machine",
                        required=True)
    parser.add_argument("--cores", "--cores_available",
                        dest="cores_available",
                        help="How many cores in the machine",
                        required=True)
    parser.add_argument("-r", "--ram",
                        dest="ram",
                        help="How much ram available",
                        required=True)
    parser.add_argument("-s", "--storage", "--storage_device",
                        dest="storage_device",
                        help="What storage device is being used",
                        required=True)
    parser.add_argument("--sd_notes",
                        dest="sd_notes",
                        help="Additional storage_device notes")
    parser.add_argument("-n", "--notes",
                        default="None",
                        dest="notes",
                        help="Additional notes")
    parser.add_argument("--database",
                        dest="database",
                        default=hf.HASH_DATABASE_FILE,
                        help="Specify database to write to")
    parser.add_argument("--table",
                        dest="table",
                        default=hf.MACHINE_HASH_TABLE)
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_arguments()
    db.check_if_database_exists(args.database, db.HASH_DB)
    try:
        con = sqlite3.connect(args.database)
        hash_to_use = hf.hash_machine_config(args)
        print(f"{hash_to_use}")
        add_to_machine_table(con, hash_to_use, args)
        con.commit()
    finally:
        con.close()
