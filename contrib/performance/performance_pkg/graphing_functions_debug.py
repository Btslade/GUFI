import random
import matplotlib.pyplot as plt
import pandas
import sqlite3

def include_commit_debug(df):
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

def commit_parse_debug(commit, df, final_dataframe):
    '''
    parses each commit/commit range the user provides
    
    ...
    
    Inputs
    ------
    commit: str
        commit or commit range provided by user
    df : dataframe
        dataframe containing all data in the database
    final_dataframe
        dataframe to add data from commit to
        
        
    Returns
    -------
    final_dataframe
        dataframe with data from commit added to it
    '''
    if '..' in commit:
        commit_range = commit.split('..')
        if len(commit_range) != 2:
            print(f'{commit} is an invalid input')
        else:
            oldest_commit_first_row = df[df['Commit'].str.contains(commit_range[0], na=False)].index[0]
            newest_commit_last_row = df[df['Commit'].str.contains(commit_range[1], na=False)].index
            newest_commit_last_row = newest_commit_last_row[len(newest_commit_last_row) - 1]
            data = df.iloc[oldest_commit_first_row:newest_commit_last_row + 1] # CHECK IF PLUS ONE IS NEEDED
            final_dataframe = pandas.concat([final_dataframe,data], ignore_index = True, axis = 0)
    else:
        data = df[df['Commit'].str.contains(commit, na=False)]
        data = data.dropna()
        final_dataframe = pandas.concat([final_dataframe,data], ignore_index = True, axis = 0)
    return final_dataframe


def generate_fake_data_debug(df, commit_rand_int):
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
            rand_float = round(random.uniform(0.05, 0.1),2)
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


def load_and_clean_debug(db):
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
    for column in selection.columns:
        if column == 'Commit':
            #df[i] = df[i].astype(str)
            continue
        df[column] = df[column].astype(float)
    i = 0
    while i < 10: #user will provide commit number to go back to here right now its fake data
        commit_rand_int = random.randint(10000, 70000)
        for j in range(9): #for this fake data, we will have 10 entries per commit
            df = generate_fake_data_debug(df, commit_rand_int)
        i = i + 1
    con.close()
    return df


def plot_one_debug(df, col):
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


def plot_all_debug(col, df, path_to_save):
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