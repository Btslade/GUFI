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



'''Collection of funcitons to help in extracting results from gufi commands'''
import shlex
import sqlite3
import subprocess

def run_get_stdout(command):
    '''
    Run a command and record stdout

    ...

    Inputs
    ------
    command : str
       command to run

    Returns
    -------
    command_result : str
        result of running the command string
    '''
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    command_result, _ = process.communicate()
    return command_result.decode('ascii')

# known gufi_query columns, in the order they are expected and their types
GUFI_QUERY_COLUMNS = [
    # other columns
    ["commit", str],
    ["branch", str],

    # gufi_query debug output
    ["set up globals", float],
    ["set up intermediate databases", float],
    ["thread pool", float],
    ["open directories", float],
    ["attach index", float],
    ["xattrprep", float],
    ["addqueryfuncs", float],
    ["get_rollupscore", float],
    ["descend", float],
    ["check args", float],
    ["check level", float],
    ["check level <= max_level branch", float],
    ["while true", float],
    ["readdir", float],
    ["readdir != null branch", float],
    ["strncmp", float],
    ["strncmp != . or ..", float],
    ["snprintf", float],
    ["lstat", float],
    ["isdir", float],
    ["isdir branch", float],
    ["access", float],
    ["set", float],
    ["clone", float],
    ["pushdir", float],
    ["check if treesummary table exists", float],
    ["sqltsum", float],
    ["sqlsum", float],
    ["sqlent", float],
    ["xattrdone", float],
    ["detach index", float],
    ["close directories", float],
    ["restore timestamps", float],
    ["free work", float],
    ["output timestamps", float],
    ["aggregate into final databases", float],
    ["print aggregated results", float],
    ["clean up globals", float],
    ["Threads run", int],
    ["Queries performed", int],
    ["Rows printed to stdout or outfiles", int],
    ["Total Thread Time (not including main)", float],
    ["Real time (main)", float],
]

TYPE_TO_SQLITE = {int: "INT",
                  float: "FLOAT",
                  str: "TEXT"}

def data_to_db(con: sqlite3.Connection,
               data: dict,
               columns: list,
               table_name: str):
    '''
    store extracted data into an sqlite .db file

    ...

    Inputs
    ------
    con: sqlite3.Connection
        the database to insert into
    data : dictionary
        dictionary containing the data to insert into the database
    columns: list
        list of known columns to process
    table_name:
        the table to insert into

    Returns
    -------
    None
    '''
    events = []
    values = []
    for col, _ in columns:
        events += [col]
        values += [data[col]]
    events = ", ".join("'" + event + "'" for event in events)
    values = ", ".join("'" + value + "'" for value in values)
    con.execute(f"INSERT INTO {table_name} ( {events} ) VALUES ( {values} );")

def process_debug_line(line: str,
                       sep: chr = ':',
                       rstrip: chr = None):
    '''
    split a line with sep
    the left hand side is the event/column name
    the right hand side has the debug data
    the trailing characters from the data are removed

    ...

    Inputs
    ------
    line : str
        the line to parse
    sep: chr
        the character to split the event from the data
    rstrip: chr
        the character to remove from the data

    Returns
    -------
    dictionary of event -> value
    '''
    event, value = line.split(sep)
    event = event.strip()
    value = value.strip().rstrip(rstrip)
    return {event: value}

def gufi_query(con: sqlite3.Connection,
               debug_output,  # : iterable object
               table_name: str):
    '''
    parse the debug output from gufi_query and store it into the database

    ...

    Inputs
    ------
    con: sqlite3.Connection
        the database to insert into
    debug_output : iterable
        debug output (timings, counts, etc.)
    table_name : str
        name of table to insert to

    Returns
    -------
    None
    '''
    data = {
        'commit': run_get_stdout("git rev-parse HEAD")[:-1],
        'branch': run_get_stdout("git rev-parse --abbrev-ref HEAD")[:-1],
    }
    for line in debug_output:
        if line in ["", "\n"]:
            continue
        data.update(process_debug_line(line, ":", "s"))
    # write the parsed data to the database
    data_to_db(con, data, GUFI_QUERY_COLUMNS, table_name)
