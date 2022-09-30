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



'''Hashes a gufi command based on command itself and flags'''
import argparse
import sqlite3

from performance_pkg import database_functions as db
from performance_pkg import hashing_functions as hf

def add_to_gufi_command_table(con: sqlite3.Connection,
                              hash: str,
                              args: argparse.Namespace):
    '''
    Add data to gufi command table

    Inputs
    ------
    con : sqlite3.Connectioin
        connection to sql database containing the gufi command table
    hash : str
        hash describing gufi command characteristics
    args : argparse.Namespace
        arguments user provided at command line

    Returns
    -------
    None
    '''
    gufi_command_pragma = db.GUFI_COMMAND_COLUMNS.replace("'", "")
    con.execute(f'''
                 INSERT INTO {args.table} ({gufi_command_pragma})
                 VALUES ("{hash}", "{args.hash_type}",
                 "{args.gufi_command}", "{args.a}", "{args.n}", "{args.I}",
                 "{args.S}", "{args.E}", "{args.J}", "{args.K}", "{args.G}",
                 "{args.B}", "{args.tree}", "{args.notes}");
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
                        choices=hf.Hashes.keys(),
                        help="Hashing mehtods available to use")
    parser.add_argument("--gufi",
                        dest="gufi_command",
                        help="What gufi command you used",
                        required=True)
    '''
    COMMENT OUT FOR DEBUG
    parser.add_argument('-H',
                        action= 'store_const',
                        const=1,
                        default='',
                        dest='H',
                        help= "show assigned input values")
    parser.add_argument('-x',
                        action='store_const',
                        const=1,
                        default='',
                        dest='x',
                        help='enable xattr processing')
    parser.add_argument('-p',
                        action='store_const',
                        const=1,
                        default='',
                        dest='p',
                        help='print file-names')
    parser.add_argument('-P',
                        action='store_const',
                        const=1,
                        default='',
                        dest = 'P',
                        help='print directories as they are encountered')
    parser.add_argument('-N',
                        action='store_const',
                        const=1,
                        default='',
                        dest = 'N',
                        help= 'print column-names (header) for DB results')
    parser.add_argument('-V',
                        action='store_const',
                        const=1,
                        default='',
                        dest='V',
                        help= 'print column-values (rows) for DB results')
    parser.add_argument('-s',
                        action='store_const',
                        const=1,
                        default='',
                        dest='s',
                        help='generate tree-summary table (in top-level DB)')
    parser.add_argument('-b',
                        action='store_const',
                        const=1,
                        default='',
                        dest='b',
                        help='build GUFI index tree')
    '''
    parser.add_argument("-a",
                        action="store_const",
                        const=1,
                        default=0,
                        dest="a",
                        help="AND/OR (SQL query combination)")
    parser.add_argument("-n",
                        default=0,
                        dest="n",
                        metavar="<threads>",
                        type=int,
                        help="number of threads")
    '''
     parser.add_argument("-d",
                         default="\x1e",
                         dest = "d",
                         metavar="<delim>",
                         help="delimiter (one char)  [use \'x\' for \\x1E]")
                         # using % before 02X breaks code
     parser.add_argument("-i",
                         default="",
                         dest="i",
                         metavar="<input_dir>",
                         help="input directory path")
     parser.add_argument("-t",
                         default="",
                         dest="t",
                         metavar="<to_dir>",
                         help="build GUFI index (under) here")
     parser.add_argument("-o",
                         default="",
                         dest="o",
                         metavar="<out_fname",
                         help= "output file (one-per-thread, with thread-id suffix)")  # noqa
     parser.add_argument("-O",
                         default="",
                         dest="O",
                         metavar="<out_DB>",
                         help= "output DB")
     '''
    parser.add_argument("-I",
                        default="",
                        dest="I",
                        metavar="<SQL_init>",
                        help="SQL init")
    '''
    parser.add_argument("-T",
                        default="",
                        dest="T",
                        metavar="<SQL_tsum>",
                        help="SQL for tree-summary table")
    '''
    parser.add_argument("-S",
                        default="",
                        dest="S",
                        metavar="<SQL_sum>",
                        help="SQL for summary table")
    parser.add_argument("-E",
                        default="",
                        dest="E",
                        metavar="<SQL_ent>",
                        help="SQL for entries table")
    '''
    parser.add_argument("-F",
                        default="",
                        dest="F",
                        metavar="<SQL_fin>",
                        help="SQL cleanup")
                        # What does this do? Sees like there should be no argument
    parser.add_argument("-r",
                        action="store_const",
                        const=1,
                        default="",
                        dest="r",
                        help="insert files and links into db (for bfwreaddirplus2db)")
                        # gufi_dir2index?
    parser.add_argument("-R",
                        action="store_const",
                        const=1,
                        default="",
                        dest="R",
                        help="insert dires into db (for bfwreaddirplus2db"))
                        #gufi_dir2index?
    parser.add_argument('-D',
                        action="store_const",
                        const=1,
                        default="",
                        dest = "D",
                        help="dont descend the tree")
    parser.add_argument("-Y",
                        action="store_const",
                        const=1,
                        default=0,
                        dest="Y",
                        type=int,
                        help="default to all directories suspect")
    parser.add_argument("-Z",
                        action="store_const",
                        const=1,
                        default="",
                        dest="Z",
                        type=int,
                        help="default to all files/links suspect")')
    parser.add_argument("-W",
                        default="",
                        dest="W",
                        metavar="<INSUSPECT>",
                        help="suspect input file")
#pylint: disable=line-too-long
    parser.add_argument("-A",
                        default="",
                        dest="A",
                        metavar="<suspectmethod>",
                        help="suspect method (0 no suspects, 1 suspect file_dbl, 2 suspect stat d and file_fl, 3 suspect stat_dbl")
#pylint: enable=line-too-long
    parser.add_argument("-g",
                        default="",
                        dest="g",
                        metavar="<stridesize>",
                        help= "stride size for striping inodes")
    parser.add_argument("-c",
                        default="",
                        dest="c",
                        metavar="<suspecttime>",
                        help="number of threads")
    parser.add_argument("-u",
                        action="store_const",
                        const=1,
                        default="",
                        dest="u",
                        help="input mode is from a file so input is a file not a dir") #gufi_dir2index?
    parser.add_argument("-y")
    parser.add_Argument("-z")
    '''
    parser.add_argument("-J",
                        default="",
                        dest="J",
                        metavar="<SQL_interm>",
                        help="SQL for intermediate results")
    parser.add_argument("-K",
                        default="",
                        dest="K",
                        metavar="<create aggregate>",
                        help="SQL to create the final aggregation table")
    parser.add_argument("-G",
                        default="",
                        dest="G",
                        metavar="<SQL_aggregate>",
                        help="SQL for aggregated results")
    parser.add_argument("-B",
                        default="",
                        dest="B",
                        metavar="<buffer size>",
                        help="size of each thread's output buffer in bytes")
    # Non gufi command_flags
    parser.add_argument("--tree",
                        dest="tree",
                        help="What tree you are running on",
                        required=True)
    parser.add_argument("--notes",
                        default="",
                        dest="notes",
                        help="Additional notes")
    parser.add_argument("--database",
                        dest="database",
                        default=hf.HASH_DATABASE_FILE,
                        help="Specify database to write to")
    parser.add_argument("--table",
                        dest="table",
                        default=hf.GUFI_COMMAND_TABLE)
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_arguments()
    db.check_if_database_exists(args.database, db.HASH_DB)
    try:
        hash_to_use = hf.hash_gufi_command(args)
        print(f"{hash_to_use}")
        con = sqlite3.connect(args.database)
        add_to_gufi_command_table(con, hash_to_use, args)
        con.commit()
    finally:
        con.close()
