import shlex
import sqlite3
import subprocess
from . import create_table_functions as ct

def check_if_table_exists(table, keys_list, con):
    if table == []:
        create_table_str = ' FLOAT,'.join("'" + str(x) + "'" for x in keys_list)
        create_table_str = create_table_str.replace("'commit' FLOAT", "'commit'")
        create_table_str = create_table_str.replace("'branch' FLOAT", "'branch'")
        create_table_str = create_table_str.replace("'Real time (main)'", "'Real time (main)' FLOAT") 
        con.execute(f"CREATE TABLE t ({create_table_str});")

def run_get_stdout(command):
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    command_result, _= p.communicate()
    command_result = command_result.decode('ascii')
    return command_result

# TODO: move this to somewhere else
# known gufi_query columns, in the order they are expected and their types
GUFI_QUERY_COLUMNS = [
    # other columns
    ['commit', str],
    ['branch', str],

    # gufi_query debug output
    ['set up globals', float],
    ['set up intermediate databases', float],
    ['thread pool', float],
    ['open directories', float],
    ['attach index', float],
    ['xattrprep', float],
    ['addqueryfuncs', float],
    ['get_rollupscore', float],
    ['descend', float],
    ['check args', float],
    ['check level', float],
    ['check level <= max_level branch', float],
    ['while true', float],
    ['readdir', float],
    ['readdir != null branch', float],
    ['strncmp', float],
    ['strncmp != . or ..', float],
    ['snprintf', float],
    ['lstat', float],
    ['isdir', float],
    ['isdir branch', float],
    ['access', float],
    ['set', float],
    ['clone', float],
    ['pushdir', float],
    ['check if treesummary table exists', float],
    ['sqltsum', float],
    ['sqlsum', float],
    ['sqlent', float],
    ['xattrdone', float],
    ['detach index', float],
    ['close directories', float],
    ['restore timestamps', float],
    ['free work', float],
    ['output timestamps', float],
    ['aggregate into final databases', float],
    ['print aggregated results', float],
    ['clean up globals', float],
    ['Threads run', int],
    ['Queries performed', int],
    ['Rows printed to stdout or outfiles', int],
    ['Total Thread Time (not including main)', float],
    ['Real time (main)', float],
]

# TODO: define function to set up gufi_query database


def list_clean(lst): 
    lst = str(lst).replace('[', '')
    return lst.replace(']','')

def data_to_db(con        : sqlite3.Connection,
               data       : dict,
               columns    : list,
               table_name : str):
    '''
    store extracted data into an sqlite .db file
    ...

    Inputs
    ------
    con: sqlite3.Connection
        the database to insert into
    data : dictionary
        dictionary containing the data to insert into the database
    columns: list
        list of known columns to process
    table_name:
         the table to insert into

    Returns
    -------
    None
    '''
    events = []
    values = []
    for col, convert in columns:
        events += [col]
        values += [convert(data[col])]
        
    events = list_clean(events)
    values = list_clean(values)
    con.execute(f"INSERT INTO {table_name} ( {events} ) VALUES ( {values} );")

def process_debug_line(line   : str,
                       sep    : chr = ':',
                       rstrip : chr = None):
    '''
    split a line with sep
    the left hand side is the event/column name
    the right hand side has the debug data
    the trailing characters from the data are removed

    ...

    Inputs
    ------
    line : str
        the line to parse
    sep: chr
        the character to split the event from the data
    rstrip: chr
        the character to remove from the data

    Returns
    -------
    dictionary of event -> value

    '''
    event, value = line.split(sep)
    event = event.strip()
    value = value.strip().rstrip(rstrip)

    return {event : value}

def gufi_query(con             : sqlite3.Connection,
               debug_output, # : iterable object
               table_name      : str):
    '''
    parse the debug output from gufi_query and store it into the database

    ...

    Inputs
    ------
    con: sqlite3.Connection
        the database to insert into
    debug_output : iterable
        debug output (timings, counts, etc.)
    table_name : str
        name of table to insert to

    Returns
    -------
    None
    '''

    data = {
        'commit' : run_get_stdout('git rev-parse HEAD')[:-1],
        'branch' : run_get_stdout('git rev-parse --abbrev-ref HEAD')[:-1],
    }
    for line in debug_output:
        if line == '' or line == '\n':
            continue

        data.update(process_debug_line(line, ':', 's'))

    # write the parsed data to the database
    data_to_db(con, data, GUFI_QUERY_COLUMNS, table_name)
