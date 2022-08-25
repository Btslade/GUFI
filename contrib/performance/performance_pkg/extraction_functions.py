import subprocess
from subprocess import PIPE
import shlex
import csv
from pathlib import Path
def remove_escape_chars (s):
    escape_chars = ['\n', '\r', '\t', '\b', '\f']
    for escape_char in escape_chars:
        s = s.replace(escape_char, "")
    return s

def read_keys_in_csv(csv_file_name):
    command = shlex.split(f'sed -n 1p {csv_file_name}')
    p = subprocess.Popen(command, stdout=PIPE)
    first_line, _ = p.communicate() 
    first_line = first_line.decode('ascii')
    first_line=remove_escape_chars(first_line)
    csv_keys = first_line.split(',')
    return csv_keys

def split_colon(command_result):
    
    command_result = command_result.split(':')
    command_result[0] = command_result[0].lstrip()
    command_result[1] = command_result[1].lstrip() 
    update_dict={command_result[0]:command_result[1]}
    
    return update_dict

def run_line(command):
    command = shlex.split(command)
    p = subprocess.Popen(command, stderr=PIPE)
    _, command_result= p.communicate()
    command_result = command_result.decode('ascii')
    return command_result

def run_and_extract(file_lines):
    result_list = []
    result = ""
    for line in file_lines:
        result = run_line(line)
        result_list.append(result)
    return result_list

def open_file(list_of_commands):
    f = open(list_of_commands,"r")
    lines = f.readlines()
    return lines

def data_to_csv(csv_file_name, list_of_rows, keysList):
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
def clean_gufi_trace2index(command_result):
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
    
    
    #remove unnecessary strings
    
    return update_dict
    
    #print(res)
def gufi_trace2index(command_result):
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
    
def gufi_query(command_result):
    command_result = command_result.split('\n')
    command_dictionary = {}
    for i in command_result:
        if i == '': #there are some blank values extracted, this skips them
            continue
        command_dictionary.update(split_colon(i))
    keysList = [key for key in command_dictionary]
    #csv_keys = read_keys_in_csv('gufi_query.csv') will go here later
    #check if columns in csv match total columns in data method goes here
    data_to_csv('gufi_query.csv', command_dictionary, keysList)