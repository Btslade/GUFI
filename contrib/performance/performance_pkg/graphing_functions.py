import matplotlib.pyplot as plt
from matplotlib import axes
import pandas
from cycler import cycler
import sqlite3
from . import graphing_objects as go
from . import config_functions as cf
import shlex
import subprocess
from subprocess import PIPE

def add_annotations(x_vals : list, 
                    y_vals : list, 
                    text_color : list,
                    default_text_color : str, 
                    ax : axes.Axes , 
                    offset: int):
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

def set_hash_len(x_list : list, 
                 xlen : int):
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
    if xlen == 0:
        return x_list
    if xlen < 0:
        return [x[xlen:] for x in x_list] #return the last 'xlen' characters of hash
    return [x[:xlen] for x in x_list] #return the first 'xlen' characters of hash

def gather_commit_information(df : pandas.DataFrame, 
                              col : str, 
                              show_error_bar : bool, 
                              min_max_annotations : bool):
    '''
    Gather statstics of a column with all entires corresponding to a unqie commit 
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        dataframe containg data to organize by commit
    col : str
        column name from pandas dataframe
    show_error_bar : boolean
        True if user plans to plot error bars
    min_max_annotations : boolean
        True if user plans to annotate the min/max annotations
        
    Returns
    -------
    commit_information : list
        list containing 
    '''
    commit_information = []
    x_average = []
    y_average = []
    if show_error_bar:
        low_y_error_range = []
        upper_y_error_range = []
    if min_max_annotations and show_error_bar:
        lower_annotation = []
        upper_annotation = []
    for commit in df.commit.unique():
        commit_section = (df[col]).where(df['commit'] == commit)
        commit_section = commit_section.dropna()
        x = commit
        y = round( sum(commit_section.values.tolist()) / len(commit_section.values.tolist()), 2)
        if show_error_bar:
            low_y_error_range.append(y - commit_section.min())
            upper_y_error_range.append(commit_section.max() - y)
        if min_max_annotations and show_error_bar:
            lower_annotation.append(commit_section.min())
            upper_annotation.append(commit_section.max())
        x_average.append(x)
        y_average.append(y)
    commit_information.append(x_average)
    commit_information.append(y_average)
    if show_error_bar:
        commit_information.append(low_y_error_range)
        commit_information.append(upper_y_error_range)
    if show_error_bar and min_max_annotations:
        commit_information.append(lower_annotation)
        commit_information.append(upper_annotation)
    return commit_information

def create_error_bars(df : pandas.DataFrame,
                      col : str, 
                      ax : axes.Axes, 
                      annotations : go.Annotations,
                      error_bar : go.Error_Bar,
                      axes : go.Axes):
    '''
    Create error bars out of the data provided
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        dataframe containing data to plot
    col : string
        column name to plot
    ax : Matplotlib Axes
        axes to plot on
    annotations : go.Annotations
        annotations section from the graph object
    error_bar : go.Error_Bar
        error_bar attributes from the graph object
        
        
    Returns
    -------
    ax : Axes
        Matplotlib axes with error bars placed on it
    '''
    commit_information= gather_commit_information(df, col, True, error_bar.min_max_annotation)
    
    x_average = set_hash_len(commit_information[0], axes.commit_hash_len)
    y_average = commit_information[1]
    low_y_error_range = commit_information[2]
    upper_y_error_range = commit_information[3]
    lower_annotation = commit_information[4]
    upper_annotation = commit_information[5]
        
    ax.errorbar(x_average, y_average, yerr=(low_y_error_range, upper_y_error_range), capsize=error_bar.cap_size)
    if annotations.show_annotations:
        ax = add_annotations(x_average, y_average, annotations.text_color, annotations.default_text_color, ax, annotations.offset)
    if error_bar.min_max_annotation:
        ax = add_annotations(x_average, lower_annotation, error_bar.min_color, annotations.default_text_color, ax, annotations.offset)
        ax = add_annotations(x_average, upper_annotation, error_bar.max_color, annotations.default_text_color, ax, annotations.offset)
    return ax

def generate_cycler(line_colors : list, 
                    line_types : list, 
                    markers : list):
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

def generate_graph(df : pandas.DataFrame, 
                   graph : go.Graph):
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
                                       graph.error_bar,
                                       graph.axes)
            else:
                commit_information= gather_commit_information(df, col, show_error_bar= False, min_max_annotations = False)
                xs_to_plot = set_hash_len(commit_information[0], graph.axes.commit_hash_len)
                ys_to_plot = commit_information[1]
                ax.plot(xs_to_plot, ys_to_plot)
                if graph.annotations.show_annotations == True:
                    add_annotations(xs_to_plot, ys_to_plot, graph.annotations.text_color, graph.annotations.default_text_color, ax, graph.annotations.offset)
    ax.legend(graph.basic_attributes.columns_to_plot, bbox_to_anchor=(1,1), loc="upper left")
    ax.set_title(graph.basic_attributes.graph_title)
    ax.set_xlabel(graph.axes.x_label)
    ax.set_ylabel(graph.axes.y_label)
    if len(graph.axes.y_range) != 0:
        lower_limit = graph.axes.y_range[0]
        upper_limit = graph.axes.y_range[1]
        ax.set_ylim(lower_limit, upper_limit)
    fig.savefig(graph.data.path_to_save_to, bbox_inches='tight')

def git_rev_parse(commit : str):
    '''
    exectues git rev-parse with the user's commit as an argument. this
    ensures that that user's input will be expanded to the full commit
    hash

    ...

    Inputs
    ------
    commit : str
        single commit to run git rev-parse on


    Returns
    -------
    command_result : str
        result from running the command
    '''
    command = f'git rev-parse {commit}'
    command = shlex.split(command)
    p = subprocess.Popen(command, stdout=PIPE)
    command_result, _= p.communicate()
    command_result = command_result.decode('ascii')
    command_result = command_result.split('\n') #results in extra empty space at end of list
    command_result = command_result[0] # Ignores empty space
    return command_result

def git_rev_list(commit_range : str):
    '''
    executes git_rev_list with the range of commits the user provides
    as an argument.

    ...

    Inputs
    ------
    commit_range : str
        commit range to run git rev-list on
    

    Returns
    -------
    command_result : list
        list containing commits based on user's input
    '''
    command = f'git rev-list {commit_range}'
    command = shlex.split(command)
    p = subprocess.Popen(command, stdout=PIPE)
    command_result, _= p.communicate()
    command_result = command_result.decode('ascii')
    command_result = command_result.split('\n') #results in extra empty space at end of list
    del command_result[-1] #remove empty space at end of list
    return command_result

def commit_parse(commit : str, 
                 df : pandas.DataFrame, 
                 final_dataframe : pandas.DataFrame, 
                 branch : str):
    '''
    parses each commit/commit range the user provides
    
    ...
    
    Inputs
    ------
    commit : str
        commit or commit range provided by user
    df : Pandas Dataframe
        dataframe containing all data in the database
    final_dataframe : Pandas Dataframe
        dataframe to add data from commit to
        
        
    Returns
    -------
    final_dataframe : Pandas Dataframe
        dataframe with data from commit added to it
    '''
    if '..' in commit:
        commit_list = git_rev_list(commit)
        commit_list.reverse()
        if branch !='-1':
            for c in commit_list:
                data = df.loc[(df['commit'] == c) & (df['branch'] == branch)]
                final_dataframe = pandas.concat([final_dataframe,data], ignore_index = True, axis = 0)
        else:
            for c in commit_list:
                data = df.loc[(df['commit'] == c)]
                final_dataframe = pandas.concat([final_dataframe,data], ignore_index = True, axis = 0)
    else:
        clean_commit = git_rev_parse(commit)
        if branch !='-1':
            data = df.loc[(df['commit'] == c) & (df['branch'] == branch)]
        else:
            data = df.loc[(df['commit'] == clean_commit)]
        final_dataframe = pandas.concat([final_dataframe,data], ignore_index = True, axis = 0)
    return final_dataframe

def gather_commits(data : go.Data, 
                   df : pandas.DataFrame):
    '''
    gather all commits provided by user
    
    ...
    
    Inputs
    ------
    data : go.Data
        data section extracted from the ini config file
    df : Pandas Dataframe
        dataframe containing user specifed columns
        
    
    Returns
    -------
    final_dataframe : Pandas Dataframe
        dataframe containing the data relevant to the commits provided by the user
    '''
    final_dataframe = pandas.DataFrame()
    for commit in data.commit_list:
        final_dataframe = commit_parse(commit, df, final_dataframe, data.branch)
    return final_dataframe

def load_and_clean(db : str, 
                   data : go.Data,
                   columns_to_plot : list):
    '''
    read in data from provided database. Ensure that the data being read in is in the correct format
    
    ...
    
    Inputs
    ------
    db : String
        path to database
    data : go.Data
        data section extracted from the ini config file
    columns_to_plot : list
        list of columns user wants to plot
    
    Returns
    -------
    df : Pandas Dataframe
        data loaded into a pandas dataframe
    '''
    con = sqlite3.connect(db)
    values = ', '.join("`" + str(x).replace('/', '_') + "`" for x in columns_to_plot)
    select_statement = f'select {values}, `commit`, `branch` from t'
    df = pandas.read_sql(select_statement, con)
    final_dataframe = gather_commits(data, df)
    selection = final_dataframe.select_dtypes('object')
    for column in selection.columns:
        try:
            final_dataframe[column] = final_dataframe[column].astype(float)
        except:
            pass
    con.close()
    return final_dataframe


def define_graph(config_file_path : str,
                 database_path : str):
    '''
    using a provided config file, will extract the contents and generate a graph
    ...
    
    Inputs
    ------
    config_file_path : str
        path to either a .ini file or to a directory containing .ini files
    database_path : str
        path to database containing data to plot 
    
    Returns
    -------
    None
    '''
    graph = cf.read_ini(config_file_path, database_path)
    
    df = load_and_clean(graph.data.path_to_database, graph.data, graph.basic_attributes.columns_to_plot)
    generate_graph(df, graph)