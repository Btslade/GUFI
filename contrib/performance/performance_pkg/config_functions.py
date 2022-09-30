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



'''Collection of methods/functions for reading and storeing data from a config file '''
from configparser import ConfigParser, ExtendedInterpolation
import performance_pkg.graphing_objects as go

EXCEPTION_MESSAGE = 'section of config not found. Using default values'

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

def read_data_section(graph, parser):
    '''
    Extract contents from data section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''
    try:
        graph.data.path_to_save_to = parser.get('data',
                                                'path_to_save_to',
                                                fallback='graph.png')
        graph.data.commit_list = parse_config_list(parser.get('data',
                                                              'commit_list',
                                                              fallback="HEAD~3..HEAD"))
    except AttributeError:  # If the user deletes the entire section
        print(f'data {EXCEPTION_MESSAGE}')
        graph.data.path_to_csv = 'database.db'
        graph.data.path_to_save_to = 'graph.png'
        graph.data.commit_list = "HEAD~3..HEAD"

def read_basic_attributes_section(graph, parser):
    '''
    Extract contents from basic_attributes section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''

    try:
        graph.basic_attributes.columns_to_plot = parse_config_list(parser.get('basic_attributes',
                                                                              'columns_to_plot',
                                                                              fallback="Real time (main)"))
        graph.basic_attributes.graph_title = parser.get('basic_attributes',
                                                        'graph_title',
                                                        fallback='Basic Graph')
        graph.basic_attributes.dimensions = parse_config_list(parser.get('basic_attributes',
                                                                         'dimension',
                                                                         fallback='12,6'))
        graph.basic_attributes.dimensions[0] = int(graph.basic_attributes.dimensions[0])
        graph.basic_attributes.dimensions[1] = int(graph.basic_attributes.dimensions[1])
    except AttributeError:
        print(f'basic_attributes {EXCEPTION_MESSAGE}')
        graph.basic_attributes.columns_to_plot = "Real time (main)"
        graph.basic_attributes.graph_title = 'Basic Graph'
        graph.basic_attributes.dimensions = "12,6"

def read_line_section(graph, parser):
    '''
    Extract contents from line section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''
    try:
        graph.line.line_colors = parse_config_list(parser.get('line',
                                                              'line_colors',
                                                              fallback="blue"))
        graph.line.line_types = parse_config_list(parser.get('line',
                                                             'line_types',
                                                             fallback="solid"))
        graph.line.markers = parse_config_list(parser.get('line',
                                                          'markers',
                                                          fallback="o"))
    except AttributeError:
        print(f'line {EXCEPTION_MESSAGE}')
        graph.line.line_colors = "blue"
        graph.line.line_types = "solid"
        graph.line.markers = "o"

def read_axes_section(graph, parser):
    '''
    Extract contents from axes section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''
    try:
        graph.axes.x_label = parser.get('axes',
                                        'x_label',
                                        fallback="Commit")
        graph.axes.y_label = parser.get('axes',
                                        'y_label',
                                        fallback="Time (seconds)")
        graph.axes.y_range = parse_config_list(parser.get('axes',
                                                          'y_range',
                                                          fallback=''))
        graph.axes.commit_hash_len = parser.getint('axes',
                                                   'commit_hash_len',
                                                   fallback=6)
    except AttributeError:
        print(f'axes {EXCEPTION_MESSAGE}')
        graph.axes.x_label = "Commit"
        graph.axes.y_label = "Time (seconds)"
        graph.axes.y_range = ''
        graph.axes.commit_hash_len = 6

def read_annotations_section(graph, parser):
    '''
    Extract contents from annotations section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''
    try:
        graph.annotations.show_annotations = parser.getboolean('annotations',
                                                               'show_annotations',
                                                               fallback=False)
        graph.annotations.precision_points = parser.getint('annotations',
                                                           'precision_points',
                                                           fallback=2)
        graph.annotations.offset = parser.getint('annotations',
                                                 'offset',
                                                 fallback=5)
        graph.annotations.text_color = parse_config_list(parser.get('annotations',
                                                                    'text_color',
                                                                    fallback="green"))
        graph.annotations.default_text_color = parser.get('annotations',
                                                          'default_text_color',
                                                          fallback='green')
    except AttributeError:
        print(f'annotations {EXCEPTION_MESSAGE}')
        graph.annotations.show_annotations = False
        graph.annotations.precision_points = 2
        graph.annotations.offset = 5
        graph.annotations.text_color = "green"
        graph.annotations.default_text_color = 'green'

def read_error_bar_section(graph, parser):
    '''
    Extract contents from error_bar section of config file

    ...

    Inputs
    ------
    graph : go.Graph
        graph object to store extracted data into
    parser : ConfigParser
        parser contatining data from config file

    Returns
    -------
    None
    '''
    try:
        graph.error_bar.show_error_bar = parser.getboolean('error_bar',
                                                           'show_error_bar',
                                                           fallback=False)
        graph.error_bar.cap_size = parser.getint('error_bar',
                                                 'cap_size',
                                                 fallback=10)
        graph.error_bar.min_max_annotation = parser.getboolean('error_bar',
                                                               'min_max_annotation',
                                                               fallback=False)
        graph.error_bar.precision_points = parser.getint('error_bar',
                                                         'precision_points',
                                                         fallback=2)
        graph.error_bar.min_color = parse_config_list(parser.get('error_bar',
                                                                 'min_color',
                                                                 fallback='["blue"]'))
        graph.error_bar.max_color = parse_config_list(parser.get('error_bar',
                                                                 'max_color',
                                                                 fallback='["red"]'))
    except AttributeError:
        print(f'error_bar {EXCEPTION_MESSAGE}')
        graph.error_bar.show_error_bar = False
        graph.error_bar.cap_size = 10
        graph.error_bar.min_max_annotation = False
        graph.error_bar.precision_points = 2
        graph.error_bar.min_color = "blue"
        graph.error_bar.max_color = "red"

def read_ini(config_file_path):
    '''
    Read configuration file and extract contents

    ...

    Inputs
    ------
    config_file_path : str
        path to configuration file

    Returns
    -------
    graph : go.Graph
        graph attributes extracted from config file
    '''
    graph = go.Graph()  # Graph object in graphing_objects.py
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(config_file_path)  # user will provide this at command line

    read_data_section(graph, parser)
    read_basic_attributes_section(graph, parser)
    read_line_section(graph, parser)
    read_axes_section(graph, parser)
    read_annotations_section(graph, parser)
    read_error_bar_section(graph, parser)

    return graph
