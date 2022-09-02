from ast import operator
import csv
import sys
import argparse
import re

def check_operators(user_input_string):
    user_input_string = user_input_string.split()
    #print(user_input_string)
    string_to_return = ' '
    unite_column_name = ' '
    unite_column_list = []
    final_string_list = []
    operator_list = ['=', '==', '<', '<=', '>', '>=']
    while len(user_input_string) != 0:
        if user_input_string[0] == 'WHERE':
            user_input_string.pop(0)
            continue
        
        
        
        if len(user_input_string) > 1:
            if user_input_string[1] in operator_list:
                unite_column_list.append(user_input_string[0])
                final_string_list.append( unite_column_name.join(unite_column_list) )
                final_string_list.append( user_input_string[1] )
                user_input_string.pop(0)
                user_input_string.pop(0)
                unite_column_list.clear()
                continue
            else:
                unite_column_list.append(user_input_string[0])
                user_input_string.pop(0)
                continue
        else:
            unite_column_list.append(user_input_string[0])
            #print(user_input_string[0])
            user_input_string.pop(0)
    
    
    final_string_list.append( unite_column_name.join(unite_column_list) )
    try: #Check to see if float, this will ensure the logic in the if statement will work well 
        final_string_list[2] = float(final_string_list[2])
        final_string_list[2] = str(final_string_list[2])
    except(ValueError):
        final_string_list[2] = f'float(row[\'{final_string_list[2]}\'])'
    final_string_list[0] = f'float(row[\'{final_string_list[0]}\'])'
    string_to_return = string_to_return.join(final_string_list)
    return string_to_return


def clean_where(user_input):
    clean_string = ''
    user_input_list = re.split(r'and|AND|And|&&', user_input)
    total_ands = len(user_input_list) - 1
    for i in user_input_list:
        operation_string = check_operators(i)
        if operation_string == -1:
            print("FAILED parsing the Where string")
            return -1
        clean_string += operation_string
        if total_ands > 0:
            clean_string = clean_string + ' and '
            total_ands = total_ands - 1
    return clean_string




parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-w", "--where", dest = "where_str", default = "None", help="Where clause goes here")
parser.add_argument("-s", "--set", dest = "set_str", default = "None", help="Set clause goes here")
parser.add_argument('-p', "--print", action='store_true')
args = parser.parse_args()

#print(args.where_str)

#path_to_csv = sys.argv[1]

#user_input = sys.argv[1]

where_input = args.where_str
where_string = clean_where(where_input)
#print(where_string)


with open('fake_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if eval(where_string):
            if args.print:
                print(f"------------------\nRow: {row['']}\n------------------")
                for key, val in row.items():
                    if key == '':
                        continue
                    print(f"{key} : {val}")
                print("-----------------------------------\n")
            else:
                print(f"Row:{row['']}")
        # If we set something...