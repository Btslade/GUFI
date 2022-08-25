import os 
import subprocess
from performance_pkg import extraction_functions as ef

command_file_lines = ef.open_file("./list_of_commands.txt")
command_outputs = ef.run_and_extract(command_file_lines)
iterator = 0
for i in command_file_lines:
    if 'gufi_query' in i:
        ef.gufi_query(command_outputs[iterator])
    #if 'gufi_trace2index' in i:
    #    gufi_trace2index(command_outputs[iterator])
    #if 'gufi_trace2index' in i:
        
    iterator = iterator + 1