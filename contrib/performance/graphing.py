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

from cycler import cycler
from matplotlib import pyplot as plt

from performance_pkg import commit_object as co
from performance_pkg import config_functions as cf
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
    cur = con.execute(f'SELECT "{col}" ' +\
                      f'FROM {table_name} ' +\
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
    commit_data.xs_to_plot.append(gf.set_hash_len(commit, hash_len))
    commit_data.ys_to_plot.append(y_val)
    commit_data.lower_error_bar_range.append(y_val - min(raw_values))
    commit_data.upper_error_bar_range.append(max(raw_values) - y_val)
    commit_data.lower_annotation.append(min(raw_values))
    commit_data.upper_annotation.append(max(raw_values))

if __name__ == "__main__":
    args = parse_args()
    for filename in args.config:
        graph = cf.read_ini(filename)
        graph.data.path_to_database = args.database  # Necessary attribute not in config
        con = sqlite3.connect(graph.data.path_to_database)
        parsed_commits = identifiers_to_hashes(graph.data.commit_list)  # individual commits
        fig, ax = plt.subplots(figsize=tuple(graph.basic_attributes.dimensions),
                               facecolor="white")  # needs subplot to get access to figure and axes
        for col in graph.basic_attributes.columns_to_plot:
            commit_data = co.CommitInformation()
            for commit in parsed_commits:
                raw_values = gather_raw_commit_data(col, args.table,
                                                    commit, con)
                if len(raw_values) == 0:
                    continue
                process_raw_data(commit_data, raw_values,
                                 commit, graph.axes.commit_hash_len)

            gf.line_integrety_check(graph.line)  # line vals must not be empty
            custom_cycler = (cycler(color=[graph.line.line_colors[0]]) +
                             cycler(linestyle=[graph.line.line_types[0]]) +
                             cycler(marker=[graph.line.markers[0]]))

            graph.line.line_colors.pop(0)
            graph.line.line_types.pop(0)
            graph.line.markers.pop(0)

            ax.set_prop_cycle(custom_cycler)

            if graph.error_bar.show_error_bar:
                ax.errorbar(commit_data.xs_to_plot,
                            commit_data.ys_to_plot,
                            yerr=(commit_data.lower_error_bar_range,
                                  commit_data.upper_error_bar_range
                                  ),
                            capsize=graph.error_bar.cap_size)
            else:
                ax.errorbar(commit_data.xs_to_plot, commit_data.ys_to_plot)

            gf.add_annotations_to_graph(graph, commit_data.xs_to_plot,
                                        commit_data.ys_to_plot,
                                        ax,
                                        commit_data.lower_annotation,
                                        commit_data.upper_annotation)
        if len(graph.axes.y_range) == 2:  # If user provides custom range
            ax.set_ylim(graph.axes.y_range[0], graph.axes.y_range[1])
        gf.graph_labels(ax, graph.basic_attributes, graph.axes)
        fig.savefig(graph.data.path_to_save_to, bbox_inches="tight")
