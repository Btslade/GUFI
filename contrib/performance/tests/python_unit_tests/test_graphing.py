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



'''tests functions in performance/graphing.py'''
# pylint: disable=import-error, invalid-name, wrong-import-position
import os
import sys
import unittest
import sqlite3

# Add performance package to system path
root = "@CMAKE_BINARY_DIR@" # this will be root when merged with master
root = "/home/braeden/Desktop/work/gufi/my_fork/GUFI"
performance = os.path.join(root, "contrib/performance/")
sys.path.insert(0, performance)

import graphing as g
import performance_pkg.commit_object as co
import performance_pkg.database_functions as db
import performance_pkg.extraction_functions as ef

COMMIT = "commit to use"
RAW_VALUES = (1,2,3,4,5)
RAW_MIN = 1
RAW_MAX = 5
RAW_AVERAGE = 3
RAW_AVG_MIN_DIF = 2
RAW_AVG_MAX_DIF = 2

def setup_database(con):
    db.create_cumulative_times_table(con, db.CUMULATIVE_TABLE)
    for i in range(5):
        cols = []
        values = []
        for column in ef.GUFI_QUERY_COLUMNS:
            cols += [column[0]]
            values += [str(i+1)]
        values[0] = COMMIT
        values[1] = "branch"
        cols = ", ".join("'" + event + "'" for event in cols)
        values = ", ".join("'" + value + "'" for value in values)
        con.execute(f"INSERT INTO {db.CUMULATIVE_TABLE} ( {cols} ) VALUES ( {values} );")

class Commit(co.CommitInformation):

    def __init__(self):
        super().__init__()

    # https://igeorgiev.eu/python/tdd/python-unittest-assert-custom-objects-are-equal/
    def __eq__(self, other):
        '''Check if self equals another CommitInformation Object'''
        return self.xs_to_plot == other.xs_to_plot and \
               self.ys_to_plot == other.ys_to_plot and \
               self.lower_error_bar_range == other.lower_error_bar_range and \
               self.upper_error_bar_range == other.upper_error_bar_range and \
               self.lower_annotation == other.lower_annotation and \
               self.upper_annotation == other.upper_annotation

    def __repr__(self):
        return f"Commit({self.xs_to_plot},{self.ys_to_plot},{self.lower_error_bar_range}" \
               f"{self.upper_error_bar_range},{self.lower_annotation}{self.upper_annotation})"

class TestGraphing(unittest.TestCase):

    con = sqlite3.connect(":memory:")

    def test_set_hash_len(self):
        hash = "abcdef123456"
        hash_len = 6
        self.assertEqual("abcdef", g.set_hash_len(hash, hash_len))
        self.assertEqual("123456", g.set_hash_len(hash, -hash_len))

    def test_gather_raw_commit_data(self):
        col = "Total Thread Time (not including main)"
        setup_database(self.con)
        self.assertEqual(RAW_VALUES, g.gather_raw_commit_data(col, db.CUMULATIVE_TABLE,
                                                            COMMIT, self.con))

    def test_process_raw_data(self):
        commit_len = 6

        commit_data_expected = Commit()
        commit_data_expected.xs_to_plot.append(COMMIT[:commit_len])
        commit_data_expected.ys_to_plot.append(RAW_AVERAGE)
        commit_data_expected.lower_error_bar_range.append(RAW_AVG_MIN_DIF)
        commit_data_expected.upper_error_bar_range.append(RAW_AVG_MAX_DIF)
        commit_data_expected.lower_annotation.append(RAW_MIN)
        commit_data_expected.upper_annotation.append(RAW_MAX)

        commit_data = Commit()

        g.process_raw_data(commit_data, RAW_VALUES, COMMIT, commit_len)
        self.assertEqual(commit_data_expected, commit_data)

if __name__ == "__main__":
    unittest.main()
