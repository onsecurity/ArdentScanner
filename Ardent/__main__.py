from lib import fs
from modules import http
from scan import TaskEngine, Scanner
from colorama import Fore
from argparse import ArgumentParser
import settings
import sys
from Ardent.lib.banner import get_banner

import sys, os


def banner():
    print "Welcome to..." + Fore.LIGHTBLACK_EX
    banner_path = os.path.join(os.path.dirname(__file__), 'resources/banner.txt')
    banner_file = open(banner_path, "r")
    for line in banner_file:
        sys.stdout.write(line)
    print Fore.RESET + "\n"
    banner_file.close()



def parse_args():
    parser = ArgumentParser(description="Ardent Scanner is a lightweight, easily extendable, automated enumeration framework.")
    parser.add_argument('targets', type=str,
                        help="Specify a target to scan. Specify multiple targets using a coma separated string",
                       nargs="*", default="")
    parser.add_argument('-iL', '--input-file',  type=str,
                        help="Specify a file containing a list of targets (IP's or Domain names)")
    parser.add_argument('-l', "--list", action="store_true",
                        help="Lists the class names of currently installed modules")
    parser.add_argument('-A', "--aggressive", action="store_true",
                        help="Enable more intrusive enumeration tools such as dirbuster. Use --list to see all modules marked aggressive.")
    return parser.parse_args()


def init(targets):

    parse_args()








def main():
    print get_banner()
    args = parse_args()

    if args.list:
        task_engine = TaskEngine()
        task_engine.print_module_list()
        exit(0)
    targets = args.targets
    if args.input_file:
        with open(args.input_file, 'r') as f:
            targets = []
            for line in f:
                targets.append(line.strip())

    if not targets:
        print Fore.RED + "[-] No targets specified, please specify some targets or use -iL to supply a targets file. " \
                         "See --help for more information."
        exit()
    scanner = Scanner(targets, args)
    scanner.scan()




if __name__ == "__main__":
    main()





