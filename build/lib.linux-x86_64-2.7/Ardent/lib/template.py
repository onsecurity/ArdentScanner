from colorama import Fore
from Ardent import settings
import sys
import inspect
import subprocess
import threading
from os import devnull
from Ardent.lib import fs
from time import sleep
import time
from Ardent.lib.table import output_buffer, table
from Ardent.lib.banner import get_banner
from Ardent.lib.decorators import stdout
import sys

from tabulate import tabulate

blacklist = ["Descriptor", "Runner", "Task"]


class Task(object):
    multi = False
    aggressive = False
    args = {}

    def __init__(self, target):
        self.target = target
        self.cmd = ""
        self.name = ""
        self.path = ""
        self.port = "N/A"
        self.path = settings.BASE_DIR + self.target
        self.create_path()
        self.err = ""
        self.start_time = None


    def use_subdir(self, dirname):
        self.path += "/" + dirname
        self.create_path()

    def create_path(self):
        fs.create_dir(self.path + "/")

    def action(self):
        FNULL = open(devnull, 'w')
        p = subprocess.Popen(self.cmd, shell=True, stdout=FNULL, stderr=FNULL)
        return p.wait()

    def start_msg(self):
        # return Fore.GREEN + "[*] %s:%s Started" % (self.target, self.name) + Fore.RESET
        table.append([
            self.target,
            self.name,
            self.port,
            "Yes",
            "No",
            "N/A"
        ])

    def end_msg(self):
        """
        if self.err:
            return Fore.RED + "[-] %s:%s %s" % (self.target, self.name, self.err) + Fore.RESET
        return Fore.LIGHTGREEN_EX + "[+] %s:%s Complete!" % (self.target, self.name) + Fore.RESET
       """
        search = [
            self.target,
            self.name,
            self.port
        ]

        start_list_index = table.index(filter(lambda x: x[0:3] == search, table)[0])

        table[start_list_index] = [
            self.target,
            self.name,
            self.port,
            "Yes",
            "Yes",
            str(time.time() - self.start_time)
        ]

    @stdout
    def print_table(self):
        print_buffer = get_banner()
        print_buffer += tabulate(table, headers="firstrow", tablefmt="fancy_grid")
        return print_buffer

    def run(self):
        self.start_msg()
        self.start_time = time.time()
        self.print_table()
        try:
            self.action()
        except:
            print Fore.RED + "[-] %s:%s Failed" % (self.target, self.name)
        self.end_msg()
        self.print_table()
