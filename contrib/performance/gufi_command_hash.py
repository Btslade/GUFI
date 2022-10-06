import argparse
from performance_pkg import hashing_functions as hf
from performance_pkg import database_functions as df
import sqlite3
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    #store_true MAke changes in for loop
    #parser.add_argument('-H', action= 'store_true', help= "show assigned input values")
    #MAKE THIS LOOK LIKE GUFI FIND
    parser.add_argument('--hash', "--print", default='md5', dest = "hash", choices=hf.Hashes.keys(), help = "Hashing mehtods available to use")
    parser.add_argument("--gufi", dest = "gufi_command",  help="What gufi command you used", required= True )
    #parser.add_argument('-H', action= 'store_const', const=1, default='', dest='H', help= "show assigned input values")
    #parser.add_argument('-x', action= 'store_const', const=1, default='', dest='x',help='enable xattr processing')
    #parser.add_argument('-p', action= 'store_const', const=1, default='', dest = 'p', help='print file-names')
    #parser.add_argument('-P', action= 'store_const', const=1, default='', dest = 'P', help='print directories as they are encountered')
    #parser.add_argument('-N', action= 'store_const', const=1, default='', dest = 'N', help= 'print column-names (header) for DB results')
    #parser.add_argument('-V', action= 'store_const', const=1, default='', dest='V', help= 'print column-values (rows) for DB results')  
    #parser.add_argument('-s', action= 'store_const', const=1, default='', dest='s',help='generate tree-summary table (in top-level DB) ')
    #parser.add_argument('-b', action= 'store_const', const=1, default='', dest = 'b', help='build GUFI index tree')
    parser.add_argument('-a', action= 'store_const', const=1, default='', dest = 'a', help='AND/OR (SQL query combination)')
    parser.add_argument('-n', default='', dest = 'n', metavar='<threads>', help= 'number of threads')
    #parser.add_argument('-d', default='', dest = 'd', metavar='<delim>', help= 'delimiter (one char)  [use \'x\' for \\x1E]') #using % before 02X breaks code
    #parser.add_argument('-i', default='', dest = 'i', metavar='<input_dir>', help= 'input directory path')
    #parser.add_argument('-t', default='', dest = 't', metavar='<to_dir>', help= 'build GUFI index (under) here')
    #parser.add_argument('-o', default='', dest = 'o', metavar='<out_fname', help= 'output file (one-per-thread, with thread-id suffix)')
    #parser.add_argument('-O', default='', dest = 'O', metavar='<out_DB>', help= 'output DB')
    parser.add_argument('-I', default='', dest = 'I', metavar='<SQL_init>', help= 'SQL init')
    #parser.add_argument('-T', default='', dest = 'T', metavar='<SQL_tsum>', help= 'SQL for tree-summary table')
    parser.add_argument('-S', default='', dest = 'S', metavar='<SQL_sum>', help= 'SQL for summary table')
    parser.add_argument('-E', default='', dest = 'E', metavar='<SQL_ent>', help= 'SQL for entries table')
    #parser.add_argument('-F', default='', dest = 'F', metavar='<SQL_fin>', help= 'SQL cleanup') # What does this do? Sees like there should be no argument
    #parser.add_argument('-r', action= 'store_const', const=1, default='', dest = 'r', help='insert files and links into db (for bfwreaddirplus2db)') #gufi_dir2index?
    #parser.add_argument('-R', action= 'store_const', const=1, default='', dest = 'R', help='insert dires into db (for bfwreaddirplus2db")') #gufi_dir2index?
    #parser.add_argument('-D', action= 'store_const', const=1, default='', dest = 'D', help='dont descend the tree')
    #parser.add_argument('-Y', action= 'store_const', const=1, default='', dest = 'Y', help='default to all directories suspect')
    #parser.add_argument('-Z', action= 'store_const', const=1, default='', dest = 'Z', help='default to all files/links suspect")')
    #parser.add_argument('-W', default='', dest = 'W', metavar='<INSUSPECT>', help= 'suspect input file')
    #parser.add_argument('-A', default='', dest = 'A', metavar='<suspectmethod>', help= 'suspect method (0 no suspects, 1 suspect file_dfl, 2 suspect stat d and file_fl, 3 suspect stat_dfl')
    #parser.add_argument('-g', default='', dest = 'g', metavar='<stridesize>', help= 'stride size for striping inodes')
    #parser.add_argument('-c', default='', dest = 'c', metavar='<suspecttime>', help= 'number of threads')
    #parser.add_argument('-u', action= 'store_const', const=1, default='', dest = 'u', help='input mode is from a file so input is a file not a dir') #gufi_dir2index?
    #parser.add_argument('-y)
    
    #parser.add_argument("-s", "-S", "--summary", dest = "S", default = "", help="Summary command", required = True)
    #parser.add_argument("-e", "-E", "--entires", dest = "E", default = "", help="Name of machine")
    parser.add_argument("--tree", dest = "tree",  help="What tree you are running on", required= True)
    parser.add_argument("--notes", default="", dest = "notes",  help = "Additional notes")
    parser.add_argument("--database", dest='database', default = hf.HASH_DATABASE_FILE, help = "Specify database to write to other than the default")
    parser.add_argument("--table",
                    dest='table',
                    default=hf.GUFI_COMMAND_TABLE)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_command_line_arguments()
    df.check_if_database_exists(args.database, df.HASH_DB)
    try:
        hash_to_use = hf.hash_gufi_command(args)
        print(f'Resulting hash: {hash_to_use}')
        con = sqlite3.connect(args.database)
        hf.add_to_gufi_command_table(con, hash_to_use, args)
        con.commit()
    finally:
        con.close()