import os
import subprocess
from subprocess import PIPE
import sys
import shlex
import csv
from pathlib import Path
import string
import argparse



def split_whitespace(lines):
    lines = [item.strip() for item in result.split('\n')]
    lines = [item.strip() for item in lines[line].split(' ')]
    return lines
    
def data_to_csv(csv_file_name, keysList):
    path = Path(csv_file_name)
    file_exists = path.is_file()
    with open(csv_file_name, 'a') as csvfile:
        i = csv.DictWriter(csvfile, fieldnames = keysList)
        if not file_exists:
            i.writeheader()
            i.writerows(list_of_rows)
            return
        #if keys dont match is the next step here
        i.writerows(list_of_rows)
    #https://pythonguides.com/python-dictionary-to-csv/

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
    
def split_colon(command_results):
    i = 0
    list_of_rows = []
    for result in command_results:
        test = result.split('\n')
        dictionary = {}
        for item in test:
            if item == '':
                test.remove(item)
                continue
            item = item.split(':')
            item[0] = item[0].lstrip()
            item[1] = item[1].lstrip() 
            update_dict={item[0]:item[1]}
            dictionary.update(update_dict)
        list_of_rows.append(dictionary)
    return list_of_rows

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


#command_file_lines = open_file("./list_of_commands.txt")
#command_outputs = run_and_extract(command_file_lines)
#list_of_rows = split_colon(command_outputs)
#keysList = [key for key in list_of_rows[0]]
#csv_keys = read_keys_in_csv('my_csv.csv')
#data_to_csv('my_csv.csv', keysList)
