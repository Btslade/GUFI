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
from configparser import ConfigParser
from matplotlib import axes

from performance_pkg import config_functions as cf

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

def add_annotations_to_graph(parser: ConfigParser,
                             min_colors: list,
                             max_colors: list,
                             text_colors: list,
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

    min_max_annotation = cf.get_key_value(parser, cf.ERROR_BAR,
                                          cf.MIN_MAX_ANNOTATION, [bool, True])
    show_error_bar = cf.get_key_value(parser, cf.ERROR_BAR,
                                      cf.SHOW_ERROR_BAR, [bool, True])
    annotation_offset = cf.get_key_value(parser, cf.ANNOTATIONS,
                                         cf.OFFSET, [int, 5])
    annotation_precision_points = cf.get_key_value(parser, cf.ANNOTATIONS,
                                                   cf.PRECISION_POINTS, [int, 2])
    default_text_color = cf.get_key_value(parser, cf.ANNOTATIONS,
                                          cf.DEFAULT_TEXT_COLOR, [str, "orange"])
    error_bar_precision_points = cf.get_key_value(parser, cf.ERROR_BAR,
                                                  cf.PRECISION_POINTS, [int, 2])
    show_error_bar = cf.get_key_value(parser, cf.ANNOTATIONS,
                                      cf.SHOW_ANNOTATIONS, [bool, True])

    if show_error_bar:
        add_annotations(xs_to_plot,
                        ys_to_plot,
                        text_colors,
                        default_text_color,
                        ax,
                        annotation_offset,
                        annotation_precision_points)

    if min_max_annotation and show_error_bar:
        add_annotations(xs_to_plot,
                        lower_annotation,
                        min_colors,
                        min_colors[0],
                        ax,
                        annotation_offset,
                        error_bar_precision_points,
                        True)
        add_annotations(xs_to_plot,
                        upper_annotation,
                        max_colors,
                        max_colors[0],
                        ax,
                        annotation_offset,
                        error_bar_precision_points,
                        True)

def graph_labels(ax: axes.Axes,
                 parser: ConfigParser):
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
    ax.legend(cf.get_key_value(parser, cf.BASIC_ATTRIBUTES,
                               cf.COLUMNS_TO_PLOT, [list, "Real time (main)"]),
              bbox_to_anchor=(1, 1),
              loc="upper left")
    ax.set_title(cf.get_key_value(parser, cf.BASIC_ATTRIBUTES, cf.GRAPH_TITLE, [str, "Graph"]))
    ax.set_xlabel(cf.get_key_value(parser, cf.AXES, cf.X_LABEL, [str, "Commit Hash"]))
    ax.set_ylabel(cf.get_key_value(parser, cf.AXES, cf.Y_LABEL, [str, "Time (seconds)"]))
