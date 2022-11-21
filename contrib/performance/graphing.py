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



# pylint: disable=import-error, invalid-name, wrong-import-position, wrong-import-order, redefined-outer-name
'''create a graph based on user arguments'''
import argparse
import sqlite3

from configparser import ConfigParser, ExtendedInterpolation
from cycler import cycler
from matplotlib import pyplot as plt

from performance_pkg import config_functions as cf
from performance_pkg import commit_object as co
from performance_pkg import database_functions as db
from performance_pkg import extraction_functions as ef
from performance_pkg import graphing_functions as gf

# pylint: enable=import-error, invalid-name, wrong-import-position, wrong-import-order
def parse_args():
    '''parse arguments from command line'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database",
                        dest="database",
                        help="Database to read from")
    parser.add_argument("-c", "--config",
                        nargs="+",
                        help="Config file(s)")
    parser.add_argument("-t", "--table",
                        dest="table",
                        default=db.CUMULATIVE_TABLE)
    return parser.parse_args()

def get_hashes(identifier: str):
    '''
    get hash and hash ranges the user provides

    ...

    Inputs
    ------
    identifier : str
        identifier provided by user eg: performance, c236d..94cca

    Returns
    -------
    list containing all hashes from identifier from oldest to newest
    '''
    if '..' in identifier:
        result = ef.run_get_stdout(f"git rev-list {identifier}")
    else:
        result = ef.run_get_stdout(f"git rev-parse {identifier}")
    return result.split('\n')[-2::-1]  # remove last empty line and reverse list

def set_hash_len(hash: str,
                 hash_len: int):
    '''
    sets the length of the hash label on the x axis of the graph

    ...

    Inputs
    ------
    hash : str
        list of hashes to go through and shorten
    hash_len : int
        how many characters long to plot the hash on the graph

    Returns
    -------
    hash : str
        shortened hash len
    '''
    if hash_len == 0:
        return hash
    if hash_len < 0:
        return hash[hash_len:]  # return the last 'hash_len' characters of hash
    return hash[:hash_len]  # return the first 'hash_len' characters of hash

def identifiers_to_hashes(config_identifiers: list):
    '''
    extract hashes and ranges of hashes based on identifiers provided by user
    ...

    Inputs
    ------
    config_identifiers : list
        list of identifiers provided by user eg: performance~10..performance

    Returns
    -------
    full_hash_list : list
        flattened list of all hashes extracted from user provided identifiers
    '''
    full_hash_list = []
    for identifier in config_identifiers:
        full_hash_list += get_hashes(identifier)
    return full_hash_list

def gather_raw_commit_data(col: str,
                           table_name: str,
                           commit: str,
                           con: sqlite3.Connection):
    '''
    Gather unprocessed data from table based on commit

    ...

    Inputs
    ------
    col : str
        column/columns to select
    table_name : str
        table in database to search through
    commit : str
        commit constraint of data
    con : sqlite3.Connection
        connection to database containing table to search

    Returns
    -------
    None
    '''
    cur = con.execute(f'SELECT "{col}" ' +
                      f'FROM {table_name} ' +
                      f'WHERE "commit" = "{commit}"'
                      )
    rows = cur.fetchall()
    row_values = list(zip(*rows))
    if len(row_values) == 0:  # Does the database contain this commit?
        print(f"No runs on commit '{commit}' recorded")
        return row_values
    return row_values[0]

def process_raw_data(commit_data: co.CommitInformation,
                     raw_values: list,
                     commit: str,
                     hash_len: int):
    '''
    process data gathered into a usable and readable format

    ...

    Inputs
    ------
    commit_data : co.CommitInformation
        Commit information object to store processed data
    raw_values : list
        values to process
    commit : str
        commit to plot on x axis
    hash_len : int
        how many characters of the commit to write out on x axis

    Returns
    -------
    None
    '''
    y_val = sum(raw_values) / len(raw_values)
    commit_data.xs_to_plot.append(set_hash_len(commit, hash_len))
    commit_data.ys_to_plot.append(y_val)
    commit_data.lower_error_bar_range.append(y_val - min(raw_values))
    commit_data.upper_error_bar_range.append(max(raw_values) - y_val)
    commit_data.lower_annotation.append(min(raw_values))
    commit_data.upper_annotation.append(max(raw_values))

if __name__ == "__main__":
    args = parse_args()
    for filename in args.config:
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        parser.read(filename)  # user will provide this at command line
        con = sqlite3.connect(args.database)
        parsed_commits = identifiers_to_hashes(cf.get_key_value(parser,
                                                                cf.DATA,
                                                                cf.COMMIT_LIST,
                                                                [list, "HEAD~10..HEAD"]))
        dimensions = [int(element) for element in cf.get_key_value(parser, cf.BASIC_ATTRIBUTES,
                                                                   cf.DIMENSIONS, [list, "12,6"])]
        fig, ax = plt.subplots(figsize=tuple(dimensions),
                               facecolor="white")  # needs subplot to get access to figure and axes
        columns_to_plot = cf.get_key_value(parser, cf.BASIC_ATTRIBUTES,
                                           cf.COLUMNS_TO_PLOT, [list, "Real time (main)"])
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        line_colors = cf.get_key_value(parser,
                                       cf.LINE,
                                       cf.LINE_COLORS,
                                       [list, ["green"]]) + (colors * len(columns_to_plot))
        line_types = cf.get_key_value(parser,
                                      cf.LINE,
                                      cf.LINE_TYPES,
                                      [list, ["solid"]]) + (["solid"] * len(columns_to_plot))
        line_markers = cf.get_key_value(parser,
                                        cf.LINE,
                                        cf.LINE_MARKERS,
                                        [list, ["o"]]) + (["o"] * len(columns_to_plot))
        min_colors = cf.get_key_value(parser, cf.ERROR_BAR, cf.MIN_COLORS, [list, ["green"]])
        max_colors = cf.get_key_value(parser, cf.ERROR_BAR, cf.MAX_COLORS, [list, ["red"]])
        text_colors = cf.get_key_value(parser, cf.ANNOTATIONS, cf.TEXT_COLORS, [list, ["orange"]])
        for col in columns_to_plot:
            commit_data = co.CommitInformation()
            for commit in parsed_commits:
                raw_values = gather_raw_commit_data(col, args.table,
                                                    commit, con)
                if len(raw_values) == 0:
                    continue
                process_raw_data(commit_data, raw_values,
                                 commit, cf.get_key_value(parser, cf.AXES,
                                                          cf.COMMIT_HASH_LEN, [int, 6]))
            custom_cycler = (cycler(color=[line_colors[0]]) +
                             cycler(linestyle=[line_types[0]]) +
                             cycler(marker=[line_markers[0]]))

            line_colors.pop(0)
            line_types.pop(0)
            line_markers.pop(0)

            ax.set_prop_cycle(custom_cycler)

            if cf.get_key_value(parser, cf.ERROR_BAR, cf.SHOW_ERROR_BAR, [bool, True]):
                ax.errorbar(commit_data.xs_to_plot,
                            commit_data.ys_to_plot,
                            yerr=(commit_data.lower_error_bar_range,
                                  commit_data.upper_error_bar_range
                                  ),
                            capsize=cf.get_key_value(parser, cf.ERROR_BAR, cf.CAP_SIZE, [int, 10]))
            else:
                ax.errorbar(commit_data.xs_to_plot, commit_data.ys_to_plot)

            gf.add_annotations_to_graph(parser,
                                        min_colors,
                                        max_colors,
                                        text_colors,
                                        commit_data.xs_to_plot,
                                        commit_data.ys_to_plot,
                                        ax,
                                        commit_data.lower_annotation,
                                        commit_data.upper_annotation)

        y_range = cf.get_key_value(parser, cf.AXES, cf.Y_RANGE, [list, "default"])
        if len(y_range) == 2:  # If user provides custom range
            ax.set_ylim(y_range[0], y_range[1])
        gf.graph_labels(ax, parser)
        path_to_save_to = cf.get_key_value(parser, cf.DATA,
                                           cf.PATH_TO_SAVE_TO, [str, "./db_test.png"])
        fig.savefig(path_to_save_to, bbox_inches="tight")
