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



from performance_pkg.extraction import common

TABLE_NAME = 'cumulative_times'

# ordered cumulative times columns (Most recent commit -> commit 908c161 "reorganize gufi_query")
COLUMN_FORMATS = [
    [
        # from gufi_query
        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('attach index',                               float),
        ('xattrprep',                                  float),
        ('addqueryfuncs',                              float),
        ('get_rollupscore',                            float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('check if treesummary table exists',          float),
        ('sqltsum',                                    float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('xattrdone',                                  float),
        ('detach index',                               float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Threads run',                                  int),
        ('Queries performed',                            int),
        ('Rows printed to stdout or outfiles',           int),
        ('Total Thread Time (not including main)',     float),
        ('Real time (main)',                           float),
    ],

# ORDERED cumulative times columns (commit 8060d30 "split build_and_install function" -> commit 61c0a9d "count queries instead of multiplying")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('xattrprep',                                  float),
        ('get_rollupscore',                            float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('check if treesummary table exists',          float),
        ('sqltsum',                                    float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Threads run',                                  int),
        ('Queries performed',                            int),
        ('Rows printed to stdout or outfiles',           int),
        ('Total Thread Time (not including main)',     float),
        ('Real time (main)',                           float),
    ],

# ordered cumulative times columns (commit 4164985 "change querydb macro into a function" -> commit 7cd35f8 "xattrprep from Gary")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('xattrprep',                                  float),
        ('get_rollupscore',                            float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('check if treesummary table exists',          float),
        ('sqltsum',                                    float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
        ('Total Thread Time (not including main)',     float),
    ],

# ordered cumulative times columns (commit 216ef5b "accidentally added argument to -w flag" -> commit a13a330 "gufi_query does not need a modifydb timer")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('check if treesummary table exists',          float),
        ('sqltsum',                                    float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
        ('Total Thread Time (not including main)',     float),
    ],

# ordered cumulative times columns (commit 00ba871 "remove --delim option from gufi_find" -> commit 75e2c5b "update tsum to use sqlite3_exec instead of rawquerydb")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('check if treesummary table exists',          float),
        ('sqltsum',                                    float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
        ('Total Thread Time (not including main)',     float),
    ],

# ordered cumulative times columns (commit "3235400 also print git branch name"  -> commit 093dc32 "Added total time spent in threads to cumulative times output")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
        ('Total Thread Time (not including main)',     float),
    ],

# ordered cumulative times columns (97fabf7 dirents not of type d, f, or l are ignored -> commit 941e8ca "use per-executable wrappers around timestamp macros")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
    ],

# ordered cumulative times columns (commit aad5b08 "use struct start_end instead of individual timespecs")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('sqlsum',                                     float),
        ('sqlent',                                     float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('clean up intermediate databases',            float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
    ],

# ordered cumulative times columns (commit aaa5b89 "remove travis user in docker" -> commit 90611bf "more DRY timestamp printing")
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('sqlite3_exec',                               float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('output timestamps',                          float),
        ('aggregate into final databases',             float),
        ('clean up intermediate databases',            float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
    ],


# ordered cumulative times columns (commit a9a1ef7 "update scripts Makefile" -> 86d3d0e gufi_query updates )
    [

        ('set up globals',                             float),
        ('set up intermediate databases',              float),
        ('thread pool',                                float),
        ('open directories',                           float),
        ('open databases',                             float),
        ('sqlite3_open_v2',                            float),
        ('create tables',                              float),
        ('set pragmas',                                float),
        ('load extensions',                            float),
        ('addqueryfuncs',                              float),
        ('descend',                                    float),
        ('check args',                                 float),
        ('check level',                                float),
        ('check level <= max_level branch',            float),
        ('while true',                                 float),
        ('readdir',                                    float),
        ('readdir != null branch',                     float),
        ('strncmp',                                    float),
        ('strncmp != . or ..',                         float),
        ('snprintf',                                   float),
        ('lstat',                                      float),
        ('isdir',                                      float),
        ('isdir branch',                               float),
        ('access',                                     float),
        ('set',                                        float),
        ('clone',                                      float),
        ('pushdir',                                    float),
        ('attach intermediate databases',              float),
        ('sqlite3_exec',                               float),
        ('detach intermediate databases',              float),
        ('close databases',                            float),
        ('close directories',                          float),
        ('restore timestamps',                         float),
        ('free work',                                  float),
        ('aggregate into final databases',             float),
        ('clean up intermediate databases',            float),
        ('print aggregated results',                   float),
        ('clean up globals',                           float),
        ('Rows returned',                                int),
        ('Queries performed',                            int),
        ('Real time',                                  float),
    ],
]

COLUMNS_COMBINED = [
    # not from gufi_query
    ('id',                                          None),
    ('commit',                                       str),
    ('branch',                                       str),

]

for COLUMN_FORMAT in COLUMN_FORMATS:
    COLUMNS_COMBINED += COLUMN_FORMAT

# Remove duplicate entries
COLUMNS = list(set(COLUMNS_COMBINED))

def create_table(con):
    common.create_table(con, TABLE_NAME, COLUMNS)

def extract(src, commit, branch):
    return common.cumulative_times_extract(src, commit, branch, COLUMNS, COLUMN_FORMATS)

def insert(con, parsed):
    common.insert(con, parsed, TABLE_NAME, COLUMNS)
