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



'''Collection of functions to handle database management'''
import os
import sqlite3
import sys

import performance_pkg.extraction_functions as ef

HASH_DB = "create_hash_database.py"
CUMULATIVE_DB = "create_cumulative_times_database.py"
CUMULATIVE_TABLE = "cumulative_times"
COMBINED_HASH_COL = "combined_hash"
MACHINE_COLUMNS = '''
                  "hash",
                  "hash_type",
                  "machine_name",
                  "cpu",
                  "cores_available",
                  "ram",
                  "storage_device",
                  "sd_notes",
                  "notes"
                  '''
GUFI_COMMAND_COLUMNS = '''
                       "hash",
                       "hash_type",
                       "gufi_command",
                       "a",
                       "n",
                       "I",
                       "S",
                       "E",
                       "J",
                       "K",
                       "G",
                       "B",
                       "tree",
                       "notes"
                       '''
FULL_HASH_COLUMNS = f'''
                     "{COMBINED_HASH_COL}",
                     "hash_type",
                     "machine_hash",
                     "gufi_hash",
                     "notes"
                     '''

def check_if_database_exists(database: str,
                             util: str):
    '''
    Checks if a database exists. If it does not, inform the user of a
    util to use to create one

    ...

    Inputs
    ------
    database : str
        path to database
    util : str
        name of util user can use to create database

    Returns
    -------
    None
    '''
    if not os.path.isfile(database):
        print(f"'{database}' does not exist!!!\nCreate using: {util}")
        sys.exit()

def create_cumulative_times_table(con: sqlite3.Connection,
                                  table_name: str):
    '''
    Create a table to store cumulative times gathered

    ...

    Inputs
    ------
    con : sqlite3.Connection
        Connection to database to add the full hash table to
    table_name : str
        What to name the cumulative times table in the database

    Returns
    -------
    None
    '''
    create_table_list = []
    for column_name, column_type in ef.GUFI_QUERY_COLUMNS:
        sqlite_column_type = ef.TYPE_TO_SQLITE[column_type]
        create_table_list += [f"'{column_name}' {sqlite_column_type}"]
    create_table_str = ", ".join(create_table_list)
    con.execute(f"CREATE TABLE {table_name} ({create_table_str});")
