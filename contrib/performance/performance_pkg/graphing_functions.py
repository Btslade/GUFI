import matplotlib.pyplot as plt
import pandas
import random
from cycler import cycler
def include_commit(df):
    #f['Commit'] = [1000]
    df.insert(loc=1, column='Commit', value=1000)
    return df

def load_and_clean(csv):
    df = pandas.read_csv(csv)
    #remove s after values
    selection = df.select_dtypes('object')
    for i in selection.columns:
        df[i] = df[i].str.replace('s', '')
        df[i] = df[i].astype(float)
    df = include_commit(df)
    i = 0
    while i < 10: #user will provide commit number to go back to here
        new_row = []
        for j in df.columns:
            if df[j].dtype == 'float64':
                rand_float = round(random.uniform(0.05, 10),2)
                new_row.append(rand_float)
            elif df[j].name == 'Threads run':
                rand_int = random.randint(100, 251)
                new_row.append(rand_int)
            elif df[j].name == 'Queries performed':
                rand_int = random.randint(500, 1000)
                new_row.append(rand_int)
            elif df[j].name == 'Rows printed to stdout or outfiles':
                rand_int = random.randint(1500, 2100)
                new_row.append(rand_int)
            elif df[j].name == 'Commit':
                rand_int = random.randint(10000, 70000)
                new_row.append(rand_int)
        df.loc[len(df)] = new_row
        df['Threads run'] = df['Threads run'].astype(int)
        df['Queries performed'] = df['Queries performed'].astype(int)
        df['Rows printed to stdout or outfiles'] = df['Rows printed to stdout or outfiles'].astype(int)
        df['Commit'] = df['Commit'].astype(int)
        df['Commit'] = df['Commit'].astype(str)
        i = i + 1
    return df

def plot_all(df, col):
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

def generate_graph(df, columns_to_plot, line_colors, graph_title, dimensions, line_types, markers, x_label, y_label, annotations, offset, text_color, default_text_color, png):
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
            ax.plot(df['Commit'].values.tolist(), df[col].values.tolist())
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