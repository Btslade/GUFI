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



import os
import sys
if sys.version_info.major >= 3:
    import configparser
else:
    import ConfigParser             # pylint: disable=import-error

import performance_pkg.graph.stats  # pylint: disable=wrong-import-position
import gufi_common                  # pylint: disable=wrong-import-position

# converter functions for input read from ConfigParser
def pos_float(value):
    val = float(value)
    if val <= 0:
        raise ValueError('Positive float got a non-positive number: {0}'.format(val))
    return val

def to_list(value, convert=str):
    # don't return empty list if input is None
    if value is None:
        return None
    return [convert(item.strip()) for item in value.split(',')]

def str_list(value):
    return to_list(value)

def pos_float_list(value):
    values = to_list(value, float)
    for val in values:
        if val <= 0:
            raise ValueError('Positive float list got a non-positive number: {0}'.format(val))
    return values

# config sections and keys
RAW_DATA = 'raw_data'                      # section
RAW_DATA_COMMITS = 'commits'               # string list
RAW_DATA_COLUMNS = 'columns'               # string list

OUTPUT = 'output'                          # section
OUTPUT_PATH = 'path'                       # string
OUTPUT_GRAPH_TITLE = 'graph_title'         # string
OUTPUT_DIMENSIONS = 'graph_dimensions'     # postive float pair

LINES = 'lines'                            # section
LINES_COLORS = 'colors'                    # string list
LINES_TYPES = 'types'                      # string list
LINES_MARKERS = 'markers'                  # string list

AXES = 'axes'                              # section
AXES_X_HASH_LEN = 'hash_len'               # integer
AXES_X_LABEL_SIZE = 'x_label_size'         # string
AXES_X_LABEL_ROTATION = 'x_label_rotation' # floating point
AXES_X_FULL_RANGE = 'x_full_range'         # bool
AXES_Y_LABEL = 'y_label'                   # string
AXES_Y_STAT = 'y_stat'                     # string
AXES_Y_MIN = 'y_min'                       # float
AXES_Y_MAX = 'y_max'                       # float
AXES_ANNOTATE = 'annotate'                 # bool

ERROR_BAR = 'error_bar'                    # section
ERROR_BAR_BOTTOM = 'bottom'                # string
ERROR_BAR_TOP = 'top'                      # string
ERROR_BAR_COLORS = 'colors'                # string list
ERROR_BAR_CAP_SIZE = 'cap_size'            # positive float
ERROR_BAR_ANNOTATE = 'annotate'            # bool

ANNOTATIONS = 'annotations'                # section
ANNOTATIONS_PRECISION = 'precision'        # positive integer
ANNOTATIONS_X_OFFSET = 'x_offset'          # float
ANNOTATIONS_Y_OFFSET = 'y_offset'          # float
ANNOTATIONS_TEXT_COLORS = 'text_colors'    # string list

DEFAULTS = {
    RAW_DATA : {
        RAW_DATA_COMMITS : [str_list, []],
        RAW_DATA_COLUMNS : [str_list, []],
    },

    OUTPUT : {
        OUTPUT_PATH        : [os.path.abspath, ''],
        OUTPUT_GRAPH_TITLE : [str, ''],
        OUTPUT_DIMENSIONS  : [pos_float_list, [0.0, 0.0]],
    },

    LINES : {
        LINES_COLORS  : [str_list, []],
        LINES_TYPES   : [str_list, []],
        LINES_MARKERS : [str_list, []],
    },

    AXES: {
        AXES_X_HASH_LEN       : [int, 0],
        AXES_X_LABEL_SIZE     : [str, None],
        AXES_X_LABEL_ROTATION : [float, None],
        AXES_X_FULL_RANGE     : [bool, False],
        AXES_Y_LABEL          : [str, 'Y Axis'],
        AXES_Y_STAT           : [str, performance_pkg.graph.stats.AVERAGE],
        AXES_Y_MIN            : [float, None],
        AXES_Y_MAX            : [float, None],
        AXES_ANNOTATE         : [bool, False]
    },

    ERROR_BAR : {
        ERROR_BAR_BOTTOM    : [str, None],
        ERROR_BAR_TOP       : [str, None],
        ERROR_BAR_COLORS    : [str_list, []],
        ERROR_BAR_CAP_SIZE  : [pos_float, 10],
        ERROR_BAR_ANNOTATE  : [bool, False]
    },

    # affects both AXES_Y_STAT and ERROR_BAR
    ANNOTATIONS : {
        ANNOTATIONS_PRECISION   : [gufi_common.get_non_negative, 3],
        ANNOTATIONS_X_OFFSET    : [float, 5],
        ANNOTATIONS_Y_OFFSET    : [float, 5],
        ANNOTATIONS_TEXT_COLORS : [str_list, []],
    },
}

def read_value(conf, parser, defaults, section, key, modify_val=None): # pylint: disable=too-many-arguments
    convert, default = defaults[section][key]
    try:
        value = convert(parser.get(section, key))
    except Exception: # pylint: disable=broad-except
        value = default

    conf[section][key] = value if modify_val is None else modify_val(value)

def read_bool(conf, parser, defaults, section, key):
    _, default = defaults[section][key]
    try:
        value = parser.getboolean(section, key)
    except Exception: # pylint: disable=broad-except
        value = default

    conf[section][key] = value

def config_file(filename):
    '''
    Parse settings found in config file

    This function creates a complete configuration for graphing. The
    graphing function may modify the values even further but will not
    require any more sections or keys.
    '''

    if sys.version_info.major >= 3:
        parser = configparser.ConfigParser(interpolation=None)

        # raise exception if file doesn't exist
        with open(filename, 'r') as f: # pylint: disable=unspecified-encoding
            parser.read_file(f)
    else:
        parser = ConfigParser.ConfigParser()

        # raise exception if file doesn't exist
        with open(filename, 'r') as f: # pylint: disable=unspecified-encoding
            parser.readfp(f)

    conf = {section : {} for section in DEFAULTS}

    read_value(conf, parser, DEFAULTS, RAW_DATA, RAW_DATA_COMMITS)
    read_value(conf, parser, DEFAULTS, RAW_DATA, RAW_DATA_COLUMNS)

    read_value(conf, parser, DEFAULTS, OUTPUT, OUTPUT_PATH)
    read_value(conf, parser, DEFAULTS, OUTPUT, OUTPUT_GRAPH_TITLE)
    read_value(conf, parser, DEFAULTS, OUTPUT, OUTPUT_DIMENSIONS)

    read_value(conf, parser, DEFAULTS, LINES, LINES_COLORS)
    read_value(conf, parser, DEFAULTS, LINES, LINES_TYPES)
    read_value(conf, parser, DEFAULTS, LINES, LINES_MARKERS)

    read_value(conf, parser, DEFAULTS, AXES, AXES_X_HASH_LEN)
    read_value(conf, parser, DEFAULTS, AXES, AXES_X_LABEL_SIZE)
    read_value(conf, parser, DEFAULTS, AXES, AXES_X_LABEL_ROTATION)
    read_bool (conf, parser, DEFAULTS, AXES, AXES_X_FULL_RANGE)
    read_value(conf, parser, DEFAULTS, AXES, AXES_Y_LABEL)
    read_value(conf, parser, DEFAULTS, AXES, AXES_Y_STAT)
    read_value(conf, parser, DEFAULTS, AXES, AXES_Y_MIN)
    read_value(conf, parser, DEFAULTS, AXES, AXES_Y_MAX)
    read_bool (conf, parser, DEFAULTS, AXES, AXES_ANNOTATE)

    read_value(conf, parser, DEFAULTS, ERROR_BAR, ERROR_BAR_BOTTOM)
    read_value(conf, parser, DEFAULTS, ERROR_BAR, ERROR_BAR_TOP)
    read_value(conf, parser, DEFAULTS, ERROR_BAR, ERROR_BAR_COLORS)
    read_value(conf, parser, DEFAULTS, ERROR_BAR, ERROR_BAR_CAP_SIZE)
    read_bool (conf, parser, DEFAULTS, ERROR_BAR, ERROR_BAR_ANNOTATE)

    read_value(conf, parser, DEFAULTS, ANNOTATIONS, ANNOTATIONS_PRECISION)
    read_value(conf, parser, DEFAULTS, ANNOTATIONS, ANNOTATIONS_X_OFFSET)
    read_value(conf, parser, DEFAULTS, ANNOTATIONS, ANNOTATIONS_Y_OFFSET)
    read_value(conf, parser, DEFAULTS, ANNOTATIONS, ANNOTATIONS_TEXT_COLORS)

    return conf

def override_name(section, key):
    return '{0}_{1}'.format(section, key)

def override_args(parser):
    '''Add extra arguments to command line argument parser'''
    for section, keys in DEFAULTS.items():
        for key, setting in keys.items():
            convert, _ = setting # pylint: disable=redefined-builtin
            dest = override_name(section, key)
            flag = '--{0}'.format(dest)

            # do not set default to allow for override() to detect that the value wasn't overridden
            parser.add_argument(flag, dest=dest, type=convert,
                                help='Override [{0}][{1}] set ''in the config file'.format(
                                    section, key))

    return parser

def override(conf, args):
    for section, keys in DEFAULTS.items():
        for key, _ in keys.items():
            dest = override_name(section, key)
            value = getattr(args, dest)

            if value is not None:
                try:
                    conf[section][key] = value
                except Exception: # pylint: disable=broad-except
                    pass

    return conf

def process(filename, args):
    '''Read config file first and then override with values from the command line'''
    return override(config_file(filename), args)
