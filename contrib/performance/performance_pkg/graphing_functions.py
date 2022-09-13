import matplotlib.pyplot as plt
import pandas
import random
from cycler import cycler
from configparser import ConfigParser, ExtendedInterpolation
import json
import sqlite3
from . import graphing_objects as go
def include_commit(df):
    '''
    create a commit column (USED ONLY FOR MOCK DATA)
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        pandas data frame to add a commit column to
        
        
    Returns
    -------
    df : Pandas Dataframe
        data from csv loaded into a pandas dataframe
    '''
    #f['Commit'] = [1000]
    df.insert(loc=1, column='Commit', value=1000)
    return df


def generate_fake_data(df, commit_rand_int):
    '''
    generates fake data to fill a csv with to mimic the information 
    one might get when running the commands. This is used strictly for
    testing purposes and will most likely becom obselete.
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        pandas dataframe to add fake data to
    entries_per_commit : int
        How many entires to have per commit (testing error bars)

        
    Returns
    -------
    df : Pandas Dataframe
        pandas dataframe with fake data added to it
    '''
    
    #adding commit 
    new_row = []
    for column in df.columns:
        if df[column].dtype == 'float64':
            rand_float = round(random.uniform(0.05, 10),2)
            new_row.append(rand_float)
        elif df[column].name == 'Threads run':
            rand_int = random.randint(100, 251)
            new_row.append(rand_int)
        elif df[column].name == 'Queries performed':
            rand_int = random.randint(500, 1000)
            new_row.append(rand_int)
        elif df[column].name == 'Rows printed to stdout or outfiles':
            rand_int = random.randint(1500, 2100)
            new_row.append(rand_int)
        elif df[column].name == 'Commit':
            new_row.append(commit_rand_int)
    #print(len(df.columns))
    #print(new_row)
    df.loc[len(df)] = new_row
    df['Threads run'] = df['Threads run'].astype(int)
    df['Queries performed'] = df['Queries performed'].astype(int)
    df['Rows printed to stdout or outfiles'] = df['Rows printed to stdout or outfiles'].astype(int)
    #df['Commit'] = df['Commit'].astype(int)
    df['Commit'] = df['Commit'].astype(str).str[:6]
    return df


def plot_one(df, col):
    '''
    plot one column from the dataframe
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        pandas dataframe containing the data and their columns
    col: String
        name of column inside of the dataframe to plot
        
        
    Returns
    -------
    None
    '''
    if col.name == 'Commit':
        return
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(df['Commit'].values.tolist(), col.values.tolist(), marker='o', linestyle='dashed')
    ax.set_title(f'{col.name}')
    if col.dtype == 'float64':
        ax.set_ylabel('Time(seconds)')
    elif col.name == 'Threads run':
        ax.set_ylabel('Threads')
    elif col.name == 'Queries performed':
        ax.set_ylabel('Queries')
    elif col.name == 'Rows printed to stdout or outfiles':
        ax.set_ylabel('Rows printed')
    ax.set_xlabel('Commit Hash')
    #annotate
    offset = 2
    for x,y in zip(df['Commit'].values.tolist(), col.values.tolist()):
        ax.annotate(f'{y}', (x,y), color='green', textcoords ='offset points',  xytext =(offset, offset))
    plt.show()


def plot_all(col, df, path_to_save):
    '''
    This function generate's a single graph from a column inside of a provided dataframe
    ...
    
    Inputs
    ------
    col : str
        column from the dataframe to graph
    df : Pandas Dataframe
        pandas dataframe containing the column to graph
    path_to_save : str
        path to save all the graphs
    
    
    Returns
    -------
    None
    '''
    if col.name == 'Commit':
        return
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['Commit'].values.tolist(), col.values.tolist(), marker='o', linestyle='dashed')
    ax.set_title(f'{col.name}')
    if col.dtype == 'float64':
        ax.set_ylabel('Time(seconds)')
    elif col.name == 'Threads run':
        ax.set_ylabel('Threads')
    elif col.name == 'Queries performed':
        ax.set_ylabel('Queries')
    elif col.name == 'Rows printed to stdout or outfiles':
        ax.set_ylabel('Rows printed')
    ax.set_xlabel('Commit Hash')
    #annotate
    offset = 2
    for x,y in zip(df['Commit'].values.tolist(), col.values.tolist()):
        ax.annotate(f'{y}', (x,y), color='green', textcoords ='offset points',  xytext =(offset, offset))
    full_path = path_to_save + '/' f'{col.name}.png'
    #print(full_path)
    plt.savefig(full_path)
    plt.close()


def add_annotations(x_vals, y_vals, text_color, default_text_color, ax, offset):
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
        
        
    Returns
    -------
    ax : Axes
        Matplotlib axes with the annotations added to it
    '''
    for x, y in zip(x_vals, y_vals): #This is a for loop for the marker and linestyle
        if len(text_color) == 0:
            text_color.append(default_text_color)
        ax.annotate(f'{y}', (x,y), color=text_color[0], textcoords ='offset points',  xytext =(offset, offset))
    text_color.pop(0)
    return ax


def gather_commit_information(df, col, show_error_bar, min_max_annotations):
    '''
    Gather statstics of a column with all entires corresponding to a unqie commit 
    
    ...
    
    df : Pandas Dataframe
        dataframe containg data to organize by Commit
    col : list (Pandas Dataframe Column)
        column from pandas dataframe 
    show_error_bar : boolean
        True if user plans to plot error bars
    min_max_annotations : boolean
        True if user plans to annotate the min/max annotations
    '''
    #We need to get the y values to be the last session run in a commit
    to_return = []
    x_final = []
    y_final = []
    if show_error_bar:
        low_y_error_range = []
        upper_y_error_range = []
    if min_max_annotations and show_error_bar:
        lower_annotation = []
        upper_annotation = []
    for commit in df.Commit.unique():
        commit_section = (df[col]).where(df['Commit'] == commit)
        commit_section = commit_section.dropna()
        x = commit
        y = round( sum(commit_section.values.tolist()) / len(commit_section.values.tolist()), 2)
        if show_error_bar:
            low_y_error_range.append(y - commit_section.min())
            upper_y_error_range.append(commit_section.max() - y)
        if min_max_annotations and show_error_bar:
            lower_annotation.append(commit_section.min())
            upper_annotation.append(commit_section.max())
        x_final.append(x)
        y_final.append(y)
    to_return.append(x_final)
    to_return.append(y_final)
    if show_error_bar:
        to_return.append(low_y_error_range)
        to_return.append(upper_y_error_range)
    if show_error_bar and min_max_annotations:
        to_return.append(lower_annotation)
        to_return.append(upper_annotation)
    return to_return


def create_error_bars(df, col, ax, 
                      annotations : go.Annotations,
                      error_bar : go.Error_Bar):
    '''
    Create error bars out of the data provided
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        dataframe containing data to plot
    annotations : go.Annotations
        annotations section from the graph object
    error_bar : go.Error_Bar
        error_bar attributes from the graph object
        
        
    Returns
    -------
    ax : Axes
        Matplotlib axes with error bars placed on it
    '''
    #We need to get the y values to be the last session run in a commit
    commit_information= gather_commit_information(df, col, True, error_bar.min_max_annotation)
    
    x_final = commit_information[0]
    y_final = commit_information[1]
    low_y_error_range = commit_information[2]
    upper_y_error_range = commit_information[3]
    lower_annotation = commit_information[4]
    upper_annotation = commit_information[5]
    
    ax.errorbar(x_final, y_final, yerr=(low_y_error_range, upper_y_error_range), capsize=error_bar.cap_size)
    if annotations.show_annotations:
        ax = add_annotations(x_final, y_final, annotations.text_color, annotations.default_text_color, ax, annotations.offset)
    if error_bar.min_max_annotation:
        ax = add_annotations(x_final, lower_annotation, error_bar.min_color, annotations.default_text_color, ax, annotations.offset)
        ax = add_annotations(x_final, upper_annotation, error_bar.max_color, annotations.default_text_color, ax, annotations.offset)
    return ax


def generate_cycler(line_colors, line_types, markers):
    '''
    used to generate a matplotlib cycler object with the users input from the config
    using a cycler allows for user input without overwritting the original cycler
    
    ...
    
    Inputs
    ------
    line_colors : list
        list of line_colors inputed by user in config file
    line_types : list
        list of line styles (dashed, bold, etc) provided by user in config file
    markers : list
        list of point markers defined by user in the config file
    
    
    Returns
    -------
    custom_cycler : Cycler
        cycler to use in plot
    line_colors : list
        original line_colors list with the first position popped off
    line_types : list
        original line_types list with the first position popped off
    markers : list
        original markers list with the first position popped off
    '''
    cycler_executer = '('
    if len(line_colors) != 0:
        cycler_executer = cycler_executer + "cycler(color=[line_colors[0]])"
        if len(line_types) !=0 or len(markers) !=0:
            cycler_executer = cycler_executer + " + "
    if len(line_types) != 0:
        cycler_executer = cycler_executer + "cycler(linestyle=[line_types[0]])"
        if len(markers) != 0:
            cycler_executer = cycler_executer + " + "
    if len(markers) != 0:
        cycler_executer = cycler_executer + "cycler(marker=[markers[0]])"
    cycler_executer = cycler_executer + ")"
    custom_cycler = eval(cycler_executer)
    if len(line_colors) != 0:
        line_colors.pop(0)
    if len(line_types) != 0:
        line_types.pop(0)
    if len(markers) != 0:
        markers.pop(0)
    return custom_cycler, line_colors, line_types, markers


def generate_graph(df, graph : go.Graph):
    '''
    used to generate graph based off of all of the users inputs
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        Dataframe containg the data to plot
    graph : go.Graph
        Graph object containing all of the attributes
    
    
    Returns
    -------
    None
    '''
    fig, ax = plt.subplots(figsize=(graph.basic_attributes.dimensions[0], graph.basic_attributes.dimensions[1]), facecolor='white')
    #default_style = ax._get_lines.color_cycle
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    #print(colors)
    #ax = plot_points(ax, columns_to_plot, marker, line_type, line_colors, df, annotations, text_color)
    for col in graph.basic_attributes.columns_to_plot:
        if len(graph.line.line_colors) == 0:
            graph.line.line_colors.extend(colors)
        if len(graph.line.line_types) == 0:
            graph.line.line_types.append('solid')
        if len(graph.line.markers) == 0:
            graph.line.markers.append('o')
        if len(graph.line.line_colors) != 0 or len(graph.line.line_types) != 0 or len(graph.line.markers) != 0:
            custom_cycler, graph.line.line_colors, graph.line.line_types, graph.line.markers = generate_cycler(graph.line.line_colors, graph.line.line_types, graph.line.markers)
            ax.set_prop_cycle(custom_cycler)
            if graph.error_bar.show_error_bar:
                ax = create_error_bars(df, col, ax,
                                       graph.annotations,
                                       graph.error_bar)
            else:
                commit_information= gather_commit_information(df, col, False, False)
                xs_to_plot = commit_information[0]
                ys_to_plot = commit_information[1]
                ax.plot(xs_to_plot, ys_to_plot)
                if graph.annotations.show_annotations == True:
                    add_annotations(xs_to_plot, ys_to_plot, graph.annotations.text_color, graph.annotations.default_text_color, ax, graph.annotations.offset)
    ax.legend(graph.basic_attributes.columns_to_plot, bbox_to_anchor=(1,1), loc="upper left")
    ax.set_title(graph.basic_attributes.graph_title)
    ax.set_xlabel(graph.axes.x_label)
    ax.set_ylabel(graph.axes.y_label)
    fig.savefig(graph.paths.path_to_save_to, bbox_inches='tight')


def load_and_clean(db):
    '''
    read in data from provided csv. Ensure that the data being read in is in the correct format
    
    ...
    
    Inputs
    ------
    csv : String
        path to csv
        
        
    Returns
    -------
    df : Pandas Dataframe
        data in csv loaded into a pandas dataframe
    '''
    con = sqlite3.connect(db)
    df = pandas.read_sql('select * from t', con)
    selection = df.select_dtypes('object')
    for i in selection.columns:
        if i == 'Commit':
            #df[i] = df[i].astype(str)
            continue
        df[i] = df[i].astype(float)
    i = 0
    while i < 10: #user will provide commit number to go back to here right now its fake data
        commit_rand_int = random.randint(10000, 70000)
        for j in range(9): #for this fake data, we will have 10 entries per commit
            df = generate_fake_data(df, commit_rand_int)
        i = i + 1
    con.close()
    return df


def define_and_generate_graph(config_file_path):
    '''
    using a provided config file, will extract the contents and generate a graph
    ...
    
    Inputs
    ------
    config_file_path : str
        path to either a .ini file or to a directory containing .ini files
    
    Returns
    -------
    None
    '''
    
    graph = go.Graph #Graph object in graphing_objects.py
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(config_file_path) #user will provide this at command line

    #[paths]
    graph.paths.path_to_csv = parser.get('paths', 'path_to_csv')
    graph.paths.path_to_save_to = parser.get('paths', 'path_to_save_to')

    #[basic_attributes]
    graph.basic_attributes.columns_to_plot = json.loads(parser.get('basic_attributes', 'columns_to_plot'))
    graph.basic_attributes.graph_title = parser.get('basic_attributes', 'graph_title')
    graph.basic_attributes.dimensions = json.loads(parser.get('basic_attributes', 'dimension'))

    #[line]
    graph.line.line_colors = json.loads(parser.get('line', 'line_colors'))
    graph.line.line_types = json.loads(parser.get('line', 'line_types'))
    graph.line.markers = json.loads(parser.get('line', 'markers'))

    #[axes]
    graph.axes.x_label = parser.get('axes', 'x_label')
    graph.axes.y_label = parser.get('axes', 'y_label')

    #[annotations]
    graph.annotations.show_annotations = parser.getboolean('annotations', 'show_annotations')
    graph.annotations.offset = parser.getint('annotations', 'offset')
    graph.annotations.text_color = json.loads(parser.get('annotations', 'text_color'))
    graph.annotations.default_text_color = parser.get('annotations', 'default_text_color')

    #[error_bar]
    graph.error_bar.show_error_bar = parser.getboolean('error_bar', 'show_error_bar' )
    graph.error_bar.cap_size = parser.getint('error_bar', 'cap_size')
    graph.error_bar.min_max_annotation = parser.getboolean('error_bar', 'min_max_annotation')
    graph.error_bar.min_color = json.loads(parser.get('error_bar', 'min_color'))
    graph.error_bar.max_color = json.loads(parser.get('error_bar', 'max_color'))

    df = load_and_clean(graph.paths.path_to_csv)
    generate_graph(df, graph)