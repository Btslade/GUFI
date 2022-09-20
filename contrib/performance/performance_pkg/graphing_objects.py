class Data:
    def __init__(self):
        self.path_to_csv = ' '
        self.path_to_save_to = ' '
        self.commit_list = []

class Basic_Attributes:
    def __init__(self):
        self.columns_to_plot = []
        self.graph_title = ' '
        self.dimensions = [12,6]

class Line:
    def __init__(self):
        self.line_colors = []
        self.line_types = []
        self.markers = []

class Axes :
    def __init__(self):
        self.x_label = ' '
        self.y_label = ' '
        self.y_range = []
        self.commit_hash_len = -1

class Annotations:
    def __init__(self):
        self.show_annotations = False
        self.offset = 5
        self.text_color = []
        self.default_text_color = 'green'

class Error_Bar:
    def __init__(self):
        self.show_error_bar = False
        self.cap_size = 0
        self.min_max_annotation = False
        self.min_color = []
        self.max_color = []

class Graph:
    def __init__(self):
        self.data = Data()
        self.basic_attributes = Basic_Attributes()
        self.line = Line()
        self.axes = Axes()
        self.annotations = Annotations()
        self.error_bar = Error_Bar()
    

