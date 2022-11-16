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



'''Collection of methods/functions for reading and storing data from a config file'''
from configparser import ConfigParser

#SECTIONS
DATA = "data"
BASIC_ATTRIBUTES = "basic_attributes"
LINE = "line"
AXES = "axes"
ANNOTATIONS = "annotations"
ERROR_BAR = "error_bar"

# KEYS
PATH_TO_SAVE_TO = "path_to_save_to"
COMMIT_LIST = "commit_list"
COLUMNS_TO_PLOT = "columns_to_plot"
GRAPH_TITLE = "graph_title"
DIMENSIONS = "dimensions"
LINE_COLORS = "line_colors"
LINE_TYPES = "line_types"
MARKERS = "markers"
X_LABEL = "x_label"
Y_LABEL = "y_label"
Y_RANGE = "y-range"
COMMIT_HASH_LEN = "commit_hash_len"
SHOW_ANNOTATIONS = "show_annotaions"
PRECISION_POINTS = "precision_points"
OFFSET = "offset"
TEXT_COLORS = "text_colors"
DEFAULT_TEXT_COLOR = "default_text_color"
SHOW_ERROR_BAR = "show_error_bar"
CAP_SIZE = "cap_size"
MIN_MAX_ANNOTATION = "min_max_annotation"
EB_PRECISION_POINTS = "eb_precision_points"
MIN_COLORS = "min_colors"
MAX_COLORS = "max_colors"

DEFAULTS = {PATH_TO_SAVE_TO: ["./db_test.png", str],
            COMMIT_LIST: ["HEAD~10..HEAD", list],
            COLUMNS_TO_PLOT: ["Real time (main)", list],
            GRAPH_TITLE: ["Graph", str],
            DIMENSIONS: ["12,6", list],
            LINE_COLORS: ["green", list],
            LINE_TYPES: ["solid", list],
            MARKERS: ["o", list],
            X_LABEL: ["Commit Hash", str],
            Y_LABEL: ["Time (seconds)", str],
            Y_RANGE: ["default", list],
            COMMIT_HASH_LEN: [6, int],
            SHOW_ANNOTATIONS: [True, bool],
            PRECISION_POINTS: [2, int],
            OFFSET: [5, int],
            TEXT_COLORS: ["orange", list],
            DEFAULT_TEXT_COLOR: ["orange", str],
            SHOW_ERROR_BAR: [True, bool],
            CAP_SIZE: [10, int],
            MIN_MAX_ANNOTATION: [True, bool],
            EB_PRECISION_POINTS: [2, int],
            MIN_COLORS: ["green", list],
            MAX_COLORS: ["red", list]}

def get_key_value(parser: ConfigParser,
                  section: str,
                  key: str):
    '''
    Gets key value from config file, uses a default value if key cannot be found

    ...

    Inputs
    ------
    parser : ConfigParser
        parser to read data read from a config file
    section : str
        Section from a config file
    key : str
        key from a config file

    Returns
    -------
    key value from config file
    '''
    if DEFAULTS[key][1] == str:
        key_value = parser.get(section,
                               key,
                               fallback=DEFAULTS[key][0])
    if DEFAULTS[key][1] == int:
        key_value = parser.getint(section,
                                  key,
                                  fallback=DEFAULTS[key][0])
    if DEFAULTS[key][1] == bool:
        key_value = parser.getboolean(section,
                                      key,
                                      fallback=DEFAULTS[key][0])
    if DEFAULTS[key][1] == list:
        key_value = parse_config_list(parser.get(section,
                                                 key,
                                                 fallback=DEFAULTS[key][0]))
    return key_value

def parse_config_list(line):
    '''
    parses config entries that are lists

    ...

    Inputs
    ------
    line : str
        line pulled from config file

    Returns
    -------
    line values in list format
    '''
    entries = [item.strip() for item in line.split(',')]
    return [item.replace('"', '') for item in entries]
