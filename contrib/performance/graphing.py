from configparser import ConfigParser, ExtendedInterpolation
import json
from performance_pkg import graphing_functions as gf

parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read("configs/graph_config.ini") #user will provide this at command line

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

df = gf.load_and_clean(path_to_csv)
gf.generate_graph(df, columns_to_plot, line_colors, graph_title, dimensions, line_type, marker, x_label, y_label, annotations, offset, text_color, default_text_color, png)