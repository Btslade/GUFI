from configparser import ConfigParser, ExtendedInterpolation
from . import graphing_objects as go


def parse_config_list(line):
    return [item.strip() for item in line.split(',')]

def read_ini(config_file_path, database_path):
    graph = go.Graph() #Graph object in graphing_objects.py
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(config_file_path) #user will provide this at command line
    
    #[data]
    graph.data.path_to_database = database_path
        
    try:
        graph.data.path_to_save_to = parser.get('data', 'path_to_save_to', fallback='graph.png')
        graph.data.commit_list = parse_config_list(parser.get('data', 'commit_list', fallback= "HEAD~3..HEAD"))
    except: #If the user deletes the entire section
        graph.data.path_to_csv = 'database.db'
        graph.data.path_to_save_to = 'graph.png'
        graph.data.commit_list = "HEAD~3..HEAD"

    #[basic_attributes]
    try:
        graph.basic_attributes.columns_to_plot = json.loads(parser.get('basic_attributes', 'columns_to_plot', fallback='["Real time (main)"]'))
        graph.basic_attributes.graph_title = parser.get('basic_attributes', 'graph_title', fallback='Basic Graph')
        graph.basic_attributes.dimensions = json.loads(parser.get('basic_attributes', 'dimension', fallback='[12,6]'))
    except:
        graph.basic_attributes.columns_to_plot = ["Real time (main)"]
        graph.basic_attributes.graph_title = 'Basic Graph'
        graph.basic_attributes.dimensions = [12,6]

    #[line]
    try:
        graph.line.line_colors = json.loads(parser.get('line', 'line_colors', fallback='["blue"]'))
        graph.line.line_types = json.loads(parser.get('line', 'line_types', fallback='["solid"]'))
        graph.line.markers = json.loads(parser.get('line', 'markers', fallback='["o"]'))
    except:
        graph.line.line_colors = ["blue"]
        graph.line.line_types = ["solid"]
        graph.line.markers = ["o"]

    #[axes]
    try:
        graph.axes.x_label = parser.get('axes', 'x_label', fallback="Commit")
        graph.axes.y_label = parser.get('axes', 'y_label', fallback="Time (seconds)")
        graph.axes.y_range = json.loads(parser.get('axes', 'y_range', fallback='[]'))
        graph.axes.commit_hash_len = parser.getint('axes', 'commit_hash_len', fallback=6)
    except:
        graph.axes.x_label = "Commit"
        graph.axes.y_label = "Time (seconds)"
        graph.axes.y_range = []
        graph.axes.commit_hash_len = 6

    #[annotations]
    try:
        graph.annotations.show_annotations = parser.getboolean('annotations', 'show_annotations', fallback=False)
        graph.annotations.precision_points = parser.getint('annotations', 'precision_points', fallback=2)
        graph.annotations.offset = parser.getint('annotations', 'offset', fallback=5)
        graph.annotations.text_color = json.loads(parser.get('annotations', 'text_color', fallback='["green"]'))
        graph.annotations.default_text_color = parser.get('annotations', 'default_text_color', fallback='green')
    except:
        graph.annotations.show_annotations = False
        graph.annotations.precision_points = 2
        graph.annotations.offset = 5
        graph.annotations.text_color = ["green"]
        graph.annotations.default_text_color = 'green'
    
    #[error_bar]
    try:
        graph.error_bar.show_error_bar = parser.getboolean('error_bar', 'show_error_bar', fallback=False )
        graph.error_bar.cap_size = parser.getint('error_bar', 'cap_size', fallback=10)
        graph.error_bar.min_max_annotation = parser.getboolean('error_bar', 'min_max_annotation', fallback=False)
        graph.error_bar.precision_points = parser.getint('error_bar', 'precision_points', fallback= 2)
        graph.error_bar.min_color = json.loads(parser.get('error_bar', 'min_color', fallback='["blue"]'))
        graph.error_bar.max_color = json.loads(parser.get('error_bar', 'max_color', fallback='["red"]'))
    except:
        graph.error_bar.show_error_bar = False
        graph.error_bar.cap_size = 10
        graph.error_bar.min_max_annotation = False
        graph.error_bar.precision_points = 2
        graph.error_bar.min_color = ["blue"]
        graph.error_bar.max_color = ["red"]
    
    return graph
