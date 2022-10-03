import argparse
from performance_pkg import hashing_functions as hf
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hash", default="md5", dest = "hash", choices=hf.Hashes.keys(), help = "Hashing method to use")
    parser.add_argument("-m", "--machine", dest = "machine_name", help="Name of machine", required=True)
    parser.add_argument("--cpu", dest = "cpu",  help="What cpu your machine uses", required=True )
    parser.add_argument("--cores", dest= "cores", help="How many cores in the machine", required=True)
    parser.add_argument("-r", "--ram", dest = "ram",  help="How much ram the cpu had", required=True)
    parser.add_argument("-s", "--storage", dest = "storage_device",  help="What storage device is being used", required=True)
    parser.add_argument("--storage_notes", dest = "storage_notes",  help="Additional storage_device notes")
    parser.add_argument("-n", "--notes", default="None", dest = "notes",  help = "Additional notes")
    parser.add_argument("--database", dest='database', help = "Specify database to write to other than the default")
    args = parser.parse_args()
    return args




#for key, val in zip(d.keys(), d.values()):
#    print(key)
#    print(val)


def main():
    args = parse_command_line_arguments()
    hash_to_use = hf.hash_machine_values(args)
    print(f'Resulting hash: {hash_to_use}')
    hf.add_to_machine_table(hash_to_use, args)

if __name__ == "__main__":
    main()
