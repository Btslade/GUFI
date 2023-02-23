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



from performance_pkg import common

# common functions used to process multiple debug prints

def create_table(con, table_name, columns):
    # all column names need to be surrounded by quotation marks, even ones that don't have spaces
    cols = ', '.join('"{0}" {1}'.format(col, common.TYPE_TO_SQLITE[type]) for col, type in columns)
    con.execute('CREATE TABLE {0} ({1});'.format(table_name, cols))

def process_line(line, event, rstrip=None):
    return {event: line.strip().rstrip(rstrip)}

# helper function
def format_value(value, type): # pylint: disable=redefined-builtin
    # pylint: disable=no-else-return
    if type is None:
        return 'NULL'
    elif type == str:
        return '"{0}"'.format(value)
    return str(value)

def get_columns_format(parsed, columns):
    column_format = []
    for col_type in columns:
        if col_type[0] in parsed.keys():
            column_format.append(col_type)
    return column_format

def insert(con, parsed, table_name, columns):
    columns_format = get_columns_format(parsed, columns)
    cols = ', '.join('"{0}"'.format(col) for col, _ in columns_format)
    vals = ', '.join(format_value(parsed[col], type) for col, type in columns_format)
    con.execute('INSERT INTO {0} ({1}) VALUES ({2});'.format(table_name, cols, vals))

def cumulative_times_extract(src, commit, branch, db_columns, column_formats):
    # these aren't obtained from running gufi_query
    data = {
        'id'    : None,
        'commit': commit,
        'branch': branch,
    }

    # Organize Column Names longest->shortest
    #
    # Column names that are substrings of other column names will be
    # processed last to avoid parsing the longer column name incorrectly
    sorted_db_columns = [value[0] for value in db_columns]
    sorted_db_columns.sort(key=len)
    sorted_db_columns.reverse()

    # parse input
    for line in src:
        line = line.strip()
        if line == '':
            continue

        line_in_columns = False

        # Ensure line extracted is a known column
        for value in sorted_db_columns:

            if value == line[:len(value)]:
                line = line[len(value):]
                if line == '':
                    continue

                if line[0] == ':':
                    line = line[1:]

                data.update(process_line(line, value, 's'))
                line_in_columns = True
                break

        if not line_in_columns:
            raise ValueError('Unknown column extracted on commit {0}'.format(commit))

    # check for missing input
    column_format_match = False
    for column_format in column_formats:

        #If match found, break early
        if column_format_match:
            break

        if len(column_format) + 3 != len(data):
            column_format_match = False
            continue

        for col, _ in column_format:
            if col not in data:
                column_format_match = False
                break
            column_format_match = True

    if not column_format_match:
        raise ValueError('Cumulative times data matches no known format on commit {0}'.format(commit))

    return data
