import subprocess
from subprocess import PIPE
import shlex
import csv
from pathlib import Path
import sqlite3

def remove_escape_chars (s):
    '''
    Remove escape chars from a provided string
    
    ...
    
    Inputs
    ------
    s : str
        String to remove the escape charactrers from
    
    
    Returns
    -------
    s : str
        the string with escape characters removed
    '''
    escape_chars = ['\n', '\r', '\t', '\b', '\f']
    for escape_char in escape_chars:
        s = s.replace(escape_char, "")
    return s


def data_to_csv(csv_file_name, list_of_rows, keysList):
    '''
    convert the data extracted into a csv file
    
    ...
    
    Inputs
    ------
    csv_file_name : str
        file name of the csv to save the data to
    
    
    Returns
    -------
    None
    '''
    path = Path(csv_file_name)
    file_exists = path.is_file()
    #https://pythonguides.com/python-dictionary-to-csv/
    with open(csv_file_name, 'a') as csvfile:
        i = csv.DictWriter(csvfile, fieldnames = keysList)
        if not file_exists:
            i.writeheader()
            quick_fix = []
            quick_fix.append(list_of_rows)
            i.writerows(quick_fix)
            return
        #if keys dont match is the next step here
        quick_fix = []
        quick_fix.append(list_of_rows)
        i.writerows(quick_fix)


# https://stackoverflow.com/questions/53050969/python-capture-next-word-after-specific-string-in-a-text
# FIRST WORD AND FIRST FLOAT WILL BE ADDED TOGETHER AS KEY PAIR AT SOMEPOINT
def clean_gufi_trace2index(command_result : str):
    #define dict
    #get Scout value
    update_dict = {}
    if "Scouts took total of" in command_result:
        scout = command_result.split("Scouts took total of ", 2)
        scout = scout[1].split(" ")
        scout = scout[0]
        scout = scout + 's'
        update_dict={'Scouts':scout}
    
    if "main completed in" in command_result:
        main = command_result.split("main completed in ", 2)
        main = main[1].split(" ")
        main = main[0]
        main = main + 's'
        update_dict = {'Main':main}
    return update_dict


def gufi_trace2index(command_result : str):
    command_result = command_result.split('\n')
    command_dictionary = {}
    for i in command_result:
        if "Scouts took total of" in i or "main completed" in i:
            command_dictionary.update(clean_gufi_trace2index(i))
        elif i == '':
            continue
        else:
            command_dictionary.update(split_colon(i))
    keysList = [key for key in command_dictionary]
    data_to_csv('gufi_trace2index.csv', command_dictionary, keysList)
    print(command_dictionary)


def data_to_db(db_file_name : str, 
               dictionary_of_columns : dict):
    '''
    store extracted data into an sqlite .db file
    
    ...
    
    Inputs
    ------
    db_file_name : str
        what to name the database file
    dictionary_of_rows : dictionary
        dictionary containing column headers and column values
    
    
    Returns
    -------
    None
    '''
    keysList = [key for key in dictionary_of_columns]
    #database_file = generate_third_hash(machine_hash, gufi_command_hash)    
    
    
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    table = cur.execute("PRAGMA table_info(t);").fetchall()
    if table == []:
        create_table_str = ''
        for key in keysList:
            if key == 'commit' or key == 'branch':
                create_table_str = create_table_str + str(f"\'{key}\' ")
            if key == keysList[-1]:
                create_table_str = create_table_str + str(f"\'{key}\' FLOAT")
            else:
                create_table_str = create_table_str + str(f"\'{key}\'FLOAT,")
        cur.execute(f"CREATE TABLE t ({create_table_str});")
    #https://softhints.com/python-3-convert-dictionary-to-sql-insert/
    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dictionary_of_columns.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dictionary_of_columns.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('t', columns, values)
    #cur.execute(sql)
    try:
        cur.execute(sql)
    except(sqlite3.OperationalError):
        for column in dictionary_of_columns.keys():
            try:
                sql_statement = f'select [{column}] from t'
                cur.execute(sql_statement)
            except:
                sql_statement = f'alter table t add column {column}'
                cur.execute(sql_statement)
    finally:
        con.execute(sql)
        con.commit()
        cur.close()
        con.close()

def extract_branch():
    '''
    gets the current branch the user is on
    
    ...
    
    Inputs
    ------
    None
    
    Returns
    -------
    branch_dictionary : dictionary
        'branch' -> result of 'git rev-parse'
    
    '''
    command = 'git rev-parse --abbrev-ref HEAD'
    command = shlex.split(command)
    p = subprocess.Popen(command, stdout=PIPE)
    command_result, _= p.communicate()
    command_result = command_result.decode('ascii')
    command_result = command_result.split('\n')
    command_result = command_result[0]
    branch_dictionary = {'branch':command_result}
    return branch_dictionary

def extract_commit():
    '''
    gets the current commit the user is on
    
    ...
    
    Inputs
    ------
    None
    
    Returns
    -------
    commit_dictionary : dictionary
        'commit' -> result of 'git rev-parse'
    '''
    command = 'git rev-parse HEAD'
    command = shlex.split(command)
    p = subprocess.Popen(command, stdout=PIPE)
    command_result, _= p.communicate()
    command_result = command_result.decode('ascii')
    command_result = command_result.split('\n')
    command_result = command_result[0]
    commit_dictionary = {'commit':command_result}
    return commit_dictionary


def split_colon(command_result : str):
    '''
    take the data from the cumulative time debug output and split by colon 
    to get the event and its corresponding time
    
    ...
    
    Inputs
    ------
    command_result : str
        result from the cumulative time output
    
    
    Returns
    -------
    update_dict: Dictionary
        event name as key and time as value
    '''
    command_result = command_result.split(':')
    command_result[0] = command_result[0].lstrip()
    command_result[1] = command_result[1].lstrip()
    command_result[1] = command_result[1].replace('s', '') 
    update_dict={command_result[0]:command_result[1]}
    return update_dict


def gufi_query(command_result : str, 
               hash_to_use : str):
    '''
    convert the results of a gufi_query command and store them into the appropriate csv
    
    ...
    
    Inputs
    ------
    command_result : str
        result of the command the user ran
    hash_to_use : str
        hash to name databasefile
    
    
    Returns
    -------
    None
    '''
    command_result = command_result.split('\n')
    command_dictionary = {}
    for i in command_result:
        if i == '': #there are some blank values extracted, this skips them
            continue
        command_dictionary.update(split_colon(i))
        #add commit here
        command_dictionary.update(extract_commit())
        command_dictionary.update(extract_branch())
    #check if columns in csv match total columns in data method goes here
    data_to_db(f'{hash_to_use}.db', command_dictionary)


def run_line(command : str):
    '''
    Runs the command line extracted from the command line file
    
    ...
    
    Inputs
    ------
    command : str
        command to execute 
    
    
    Returns
    -------
    command_result: str
        results from the command being run
    '''
    command = shlex.split(command)
    p = subprocess.Popen(command, stderr=PIPE)
    _, command_result= p.communicate()
    command_result = command_result.decode('ascii')
    return command_result


def run_and_extract(file_lines : list):
    '''
    Run the command lines from the command line file and 
    store their output
    
    ...
    
    Inputs
    ------
    file_lines : list
        lines to run from the command line file
    
    
    Returns
    -------
    result_list: list
        results of each command run stored in their own string
    '''
    result_list = []
    result = ""
    for line in file_lines:
        result = run_line(line)
        result_list.append(result)
    return result_list

def open_file(file_of_commands : str):
    '''
    Open the command line file and extract the contents
    
    ...
    
    Inputs
    ------
    file_of_commands : str
        file containing the list of commands to run
    
    
    Returns
    -------
    lines: str
        lines from the file
    '''
    f = open(file_of_commands,"r")
    lines = f.readlines()
    return lines