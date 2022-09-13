class Paths:
    path_to_csv = ' '
    path_to_save_to = ' '

class Basic_Attributes:
    columns_to_plot = []
    graph_title = ' '
    dimensions = [12,6]

class Line:
    line_colors = []
    line_types = []
    markers = []

class Axes :
    x_label = ' '
    y_label = ' '

class Annotations:
    show_annotations = False
    offset = 5
    text_color = []
    default_text_color = 'green'

class Error_Bar:
    show_error_bar = False
    cap_size = 0
    min_max_annotation = False
    min_color = []
    max_color = []

class Graph:
    paths = Paths
    basic_attributes = Basic_Attributes
    line = Line
    axes = Axes
    annotations = Annotations
    error_bar = Error_Bar
    

