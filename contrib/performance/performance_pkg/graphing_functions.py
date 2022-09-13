import matplotlib.pyplot as plt
import pandas
import random
from cycler import cycler
from configparser import ConfigParser, ExtendedInterpolation
import json
import sqlite3
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

def create_error_bars(df, col, ax, annotations, text_color, default_text_color, offset):
    #We need to get the y values to be the last session run in a commit
    x_final = []
    y_final = []
    if annotations:
        lower_annotation = []
        upper_annotation = []
    low_y_error_range = []
    upper_y_error_range = []
    for commit in df.Commit.unique():

        commit_section = (df[col]).where(df['Commit'] == commit)
        commit_section = commit_section.dropna()
        x = commit
        y = commit_section.values.tolist()[len(commit_section)-1]
        if annotations:
            lower_annotation.append(commit_section.min())
            upper_annotation.append(commit_section.max())
        low_y_error_range.append(y - commit_section.min())
        upper_y_error_range.append(commit_section.max() - y)
        x_final.append(x)
        y_final.append(y)
    
    ax.errorbar(x_final, y_final, yerr=(low_y_error_range, upper_y_error_range), capsize=10)
    if annotations:
        ax = add_annotations(x_final, y_final, text_color, default_text_color, ax, offset)
        ax = add_annotations(x_final, lower_annotation, text_color, default_text_color, ax, offset)
        ax = add_annotations(x_final, upper_annotation, text_color, default_text_color, ax, offset)
        #ax = add_annotations(x_final, upper_y_error_range, text_color, default_text_color, ax, offset)
        #for x, y, in zip (x_final, y_final, low_y_error_range, upper_y_error_range):
        #    if len(text_color) == 0:
        #        text_color.append(default_text_color)
        #    ax.annotate(f'{y}', (x,y), color=text_color[0], textcoords ='offset points',  xytext =(offset, offset))
            #if low_y != upper_y:
            #    ax.annotate(f'Fastest: {low_y}', (x,low_y), color = text_color[0], textcoords='offset points', xytext=(offset, offset))
            #    ax.annotate(f'Slowest: {upper_y}', (x,upper_y), color = text_color[0], textcoords='offset points', xytext=(offset, offset))
        #text_color.pop(0)
    return ax


def add_annotations(x_vals, y_vals, text_color, default_text_color, ax, offset):
    for x, y in zip(x_vals, y_vals): #This is a for loop for the marker and linestyle
        if len(text_color) == 0:
            text_color.append(default_text_color)
        ax.annotate(f'{y}', (x,y), color=text_color[0], textcoords ='offset points',  xytext =(offset, offset))
    text_color.pop(0)
    return ax

def generate_graph(df, columns_to_plot, line_colors, 
                   graph_title, dimensions, line_types, 
                   markers, x_label, y_label, annotations, 
                   offset, text_color, default_text_color, 
                   png, error_bar):
    '''
    used to generate graph based off of all of the users inputs
    
    ...
    
    Inputs
    ------
    df : Pandas Dataframe
        Dataframe containg the data to plot
    columns_to_plot : list
        list of columns to plot on the graph
    line_colors : list
        list of line colors (corresponding to columns to plot)
    graph_title : String
        title of the graph
    dimensions : list
        dimensions of the graph [width, height]
    line_types : list
        list of line styles (corresponding to columns to plot)
    markers : list
        list of markers (corresponding to columns to plot)
    x_label : String
        name of the x_label to be displayed on the graph
    y_label : String
        name of the y_label to be displayed on the graph
    annotations : boolean
        whether or not to include the annotated text on the graph
    offset : int
        offset scalar describing how far the text will be from its original point
    text_color : list
        list of text color (corresponding to columns to plot)
    default_text_color : String
        text color for all columns not accounted for in the text_color list
    png : String
        filename to save graph to
    error_bar : bool
    
    
    
    Returns
    -------
    None
    '''
    fig, ax = plt.subplots(figsize=(dimensions[0], dimensions[1]), facecolor='white')
    #default_style = ax._get_lines.color_cycle
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    #print(colors)
    #ax = plot_points(ax, columns_to_plot, marker, line_type, line_colors, df, annotations, text_color)
    for col in columns_to_plot:
        if len(line_colors) == 0:
            line_colors.extend(colors)
        if len(line_types) == 0:
            line_types.append('solid')
        if len(markers) == 0:
            markers.append('o')
        if len(line_colors) != 0 or len(line_types) != 0 or len(markers) != 0:
            custom_cycler, line_colors, line_types, markers = generate_cycler(line_colors, line_types, markers)
            ax.set_prop_cycle(custom_cycler)
            if error_bar:
                ax = create_error_bars(df, col, ax, annotations, text_color, default_text_color, offset)
            else:
                ax.plot(df['Commit'].values.tolist(), df[col].values.tolist())
                if annotations == True:
                    for x, y in zip(df['Commit'].values.tolist(), df[col].values.tolist()): #This is a for loop for the marker and linestyle
                        if len(text_color) == 0:
                            text_color.append(default_text_color)
                        ax.annotate(f'{y}', (x,y), color=text_color[0], textcoords ='offset points',  xytext =(offset, offset))
                    text_color.pop(0)
    ax.legend(columns_to_plot, bbox_to_anchor=(1,1), loc="upper left")
    ax.set_title(graph_title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.savefig(png, bbox_inches='tight')
    
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
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(config_file_path) #user will provide this at command line

    path_to_csv = parser.get('data', 'path_to_csv')
    png = parser.get('data', 'save_to')

    columns_to_plot = json.loads(parser.get('general', 'columns_to_plot'))
    line_colors = json.loads(parser.get('general', 'line_colors'))
    graph_title = parser.get('general', 'graph_title')
    dimensions = json.loads(parser.get('general', 'dimension'))

    line_type = json.loads(parser.get('line', 'line_type'))
    marker = json.loads(parser.get('line', 'marker'))

    x_label = parser.get('axes', 'x_label')
    y_label = parser.get('axes', 'y_label')

    annotations = parser.getboolean('annotations', 'annotations')
    offset = parser.getint('annotations', 'offset')
    text_color = json.loads(parser.get('annotations', 'text_color'))
    default_text_color = parser.get('annotations', 'default_text_color')

    error_bar = parser.getboolean('error_bar', 'error_bar' )

    df = load_and_clean(path_to_csv)
    
    
    generate_graph(df, columns_to_plot, line_colors, graph_title, dimensions, line_type, marker, x_label, y_label, annotations, offset, text_color, default_text_color, png, error_bar)
    #if error_bar:
    #    generate_error_bar(df, columns_to_plot, line_colors, graph_title, dimensions, line_type, marker, x_label, y_label, annotations, offset, text_color, default_text_color, png)
    #else:
    #    generate_graph(df, columns_to_plot, line_colors, graph_title, dimensions, line_type, marker, x_label, y_label, annotations, offset, text_color, default_text_color, png)
    
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
    
def generate_error_bar(df, columns_to_plot, line_colors, 
                       graph_title, dimensions, line_types, 
                       markers, x_label, y_label, annotations,
                       offset, text_color, default_text_color, png):
    fig, ax = plt.subplots(figsize=(dimensions[0], dimensions[1]), facecolor='white')
    #default_style = ax._get_lines.color_cycle
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    #print(colors)
    #ax = plot_points(ax, columns_to_plot, marker, line_type, line_colors, df, annotations, text_color)
    for col in columns_to_plot:
        if len(line_colors) == 0:
            line_colors.extend(colors)
        if len(line_types) == 0:
            line_types.append('solid')
        if len(markers) == 0:
            markers.append('o')
        if len(line_colors) != 0 or len(line_types) != 0 or len(markers) != 0:
            custom_cycler, line_colors, line_types, markers = generate_cycler(line_colors, line_types, markers)
            ax.set_prop_cycle(custom_cycler)
            ax.errorbar(df['Commit'].values.tolist(), df[col].values.tolist(), yerr='std')
        if annotations == True:
            for x, y in zip(df['Commit'].values.tolist(), df[col].values.tolist()): #This is a for loop for the marker and linestyle
                if len(text_color) == 0:
                    text_color.append(default_text_color)
                ax.annotate(f'{y}', (x,y), color=text_color[0], textcoords ='offset points',  xytext =(offset, offset))
            text_color.pop(0)
    if len(columns_to_plot) >= 2:
        ax.legend(columns_to_plot, bbox_to_anchor=(1,1), loc="upper left")
    ax.set_title(graph_title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.savefig(png, bbox_inches='tight')