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


# pylint: disable=too-many-arguments
'''Collection of functions to generate graph'''
from matplotlib import axes
import matplotlib.pyplot as plt

import performance_pkg.graphing_objects as go

def add_annotations(x_vals: list,
                    y_vals: list,
                    text_color: list,
                    default_text_color: str,
                    ax: axes.Axes,
                    offset: int,
                    precision_points: int,
                    error_bar: bool = False):
    '''
    adds annotations to the appropriate position on the graph

    ...

    Inputs
    ------
    x_vals : list
        list containing all x coordinates
    y_vals : list
        list containing all y coordinates
    text_color : list
        list of text colors to cycle through
    default_text_color : str
        color to default to when text_color is cycled through
    ax : Axes
        Matplotlib Axes to add annotations to
    offset : int
        offset distance from annotaion point
    precision_points : int
        how many precision points/decimal places to print annotations
    error_bar : bool
        whether the error bar is implemented or not

    Returns
    -------
    None
    '''
    for x, y in zip(x_vals, y_vals):  # for loop for the marker and linestyle
        if len(text_color) == 0:
            text_color.append(default_text_color)
        ax.annotate(f"{y:.{precision_points}f}",
                    (x, y),
                    color=text_color[0],
                    textcoords="offset points",
                    xytext=(offset, offset))
    if not error_bar:
        text_color.pop(0)

def set_hash_len(hash: list,
                 hash_len: int):
    '''
    sets the length of the hash label on the x axis of the graph

    ...

    Inputs
    ------
    x_list : list
        list of hashes to go through and shorten
    x_len : int
        how many characters long to plot the hash on the graph

    Returns
    -------
    x_list : list
        list of hashes shortned to length (xlen) provided by user
    '''
    if hash_len == 0:
        return hash
    if hash_len < 0:
        return hash[hash_len:]  # return the last 'xlen' characters of hash
    return hash[:hash_len]  # return the first 'xlen' characters of hash

def graph_labels(ax: axes.Axes,
                 basic_attributes: go.BasicAttributes,
                 axes: go.Axes):
    '''
    add labels to the graph

    ...

    Inputs
    ------
    ax : axes.Axes
        matplotlib axes to plot on
    basic_attributes : go.BasicAttributes
        basic attributes of graph
    axes : go.Axes
        attributes of axes of graph

    Returns
    -------
    None
    '''
    ax.legend(basic_attributes.columns_to_plot,
              bbox_to_anchor=(1, 1),
              loc="upper left")
    ax.set_title(basic_attributes.graph_title)
    ax.set_xlabel(axes.x_label)
    ax.set_ylabel(axes.y_label)

def line_integrety_check(graph_line: go.Line):
    '''
    ensure line will always have a color, type, and marker by adding default
    values when empty

    ...

    Inputs
    ------
    graph_line : go.Line
        line attributes to validate

    Returns
    -------
    None
    '''
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    if len(graph_line.line_colors) == 0:
        graph_line.line_colors.extend(colors)
    if len(graph_line.line_types) == 0:
        graph_line.line_types.append("solid")
    if len(graph_line.markers) == 0:
        graph_line.markers.append("o")

def add_annotations_to_graph(graph: go.Graph,
                             xs_to_plot: list,
                             ys_to_plot: list,
                             ax: axes.Axes,
                             lower_annotation: list,
                             upper_annotation: list):
    '''
    adds annotations based on user's input

    ...

    Inputs
    ------
    graph : go.Graph
        graph object containing all user input from config
    xs_to_plot : list
        list of x_locations of data used as reference for adding annotations
    ys_to_plot : list
        list of y_locations of data used as reference for adding annotaitons
    ax : axes.Axes,
        matplotlib axes to plot on
    lower_annotation : list
        list of y locations of lower whisker of error bars for adding
        annotations
    upper_annotation : list
        list of y locations of upper whisker of error bars for adding
        annotations

    Returns
    -------
    None
    '''
    if graph.annotations.show_annotations:
        add_annotations(xs_to_plot,
                        ys_to_plot,
                        graph.annotations.text_color,
                        graph.annotations.default_text_color,
                        ax,
                        graph.annotations.offset,
                        graph.annotations.precision_points)
    if graph.error_bar.min_max_annotation and graph.error_bar.show_error_bar:
        add_annotations(xs_to_plot, lower_annotation,
                        graph.error_bar.min_color,
                        graph.error_bar.min_color[0],
                        ax,
                        graph.annotations.offset,
                        graph.error_bar.precision_points,
                        True)
        add_annotations(xs_to_plot, upper_annotation,
                        graph.error_bar.max_color,
                        graph.error_bar.max_color[0],
                        ax,
                        graph.annotations.offset,
                        graph.error_bar.precision_points,
                        True)
