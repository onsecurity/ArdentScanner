from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from Ardent.lib.template import Task
from Ardent.lib import fs
from Ardent import settings
import pkgutil
import re
import sys
import inspect
import importlib
from time import sleep
from queue import Queue, Empty
from threading import Thread, Event
from tabulate import tabulate


class Scanner(object):

    def __init__(self, targets, args):
        self.q = Queue()
        self.args = args
        self.stopping = Event()
        self.targets = targets

        self.exclude_regexs = self.gen_exclusions()

        fs.create_dir(settings.BASE_DIR)
        for target in self.targets:
            fs.create_dir(settings.BASE_DIR + target + "/")

    def gen_exclusions(self):
        exclude_strings = []
        if self.args.exclude:
            exclude_strings.append(self.args.exclude)
        elif self.args.exclude_file:
            with open(self.args.exlude_file, 'r') as f:
                exclude_strings += [line.strip() for line in f]
        regex_strings = []
        for exclude_string in exclude_strings:
            regex_string = exclude_string.replace(".", "\\.")
            regex_string = regex_string.replace("*", "[\\S]*")
            regex_strings.append(regex_string)
        print(regex_strings)
        return regex_strings

    def is_excluded(self, target):
        for regex in self.exclude_regexs:
            if re.match(regex, target):
                return True
        return False

    def scan(self):
        for target in self.targets:
            if not self.is_excluded(target):
                self.q.put({"target": target, "args": self.args})

        self.start_threads()
        self.q.join()
        self.stopping.set()

    def execute_scan(self, target, args):
        services = []
        nm = NmapProcess(target, options="-sV -sS -p 443")
        nm.run()
        parsed = NmapParser.parse(nm.stdout)
        host = parsed.hosts[0]
        for serv in host.services:
            services.append(serv.get_dict())

        engine = TaskEngine(args)
        engine.process_scan(target, services)
        engine.run_tasks()

    def start_threads(self):
        threads = []
        for i in range(settings.CONCURRENT_HOSTS):
            t = Thread(target=self.worker)
            t.start()
            threads.append(t)

    def worker(self):
        while not self.stopping.is_set():
            try:
                item = self.q.get(True, timeout=1)
                self.execute_scan(**item)
            except Empty:
                continue
            self.q.task_done()


class TaskEngine:

    def __init__(self, args=None):
        self.q = Queue()
        self.stopping = Event()
        self.args = args

    def run_tasks(self):
        self.start_threads()
        self.q.join()
        self.stopping.set()

    def start_threads(self):
        threads = []
        for i in range(settings.CONCURRENT_TASKS):
            t = Thread(target=self.worker)
            t.start()
            threads.append(t)

    def worker(self):
        while not self.stopping.is_set():
            try:
                kwargs = self.q.get(True, timeout=1)
                self.process_module(**kwargs)
            except Empty:
                continue
            self.q.task_done()

    def get_module_list(self):
        import Ardent.modules as modules
        package = modules
        prefix = package.__name__ + "."
        class_list = []
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = importlib.import_module(modname)
            clsmembers = inspect.getmembers(sys.modules[modname], inspect.isclass)
            class_list.append((module, clsmembers))
        module_list = []
        for module in class_list:
            for member in module[1]:
                mname = member[0]
                if issubclass(member[1], Task) and member[1] != Task:
                    m = self.get_module(module[0], mname)
                    module_list.append({
                        "name": mname,
                        "module": m
                    })
        return module_list

    def print_module_list(self):
        module_list = self.get_module_list()
        table = [["Name", "Services", "Aggressive"]]
        for module in module_list:
            table.append([
                module["name"],
                ", ".join(module["module"].services),
                module["module"].aggressive
            ])
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    def process_scan(self, target, nmap_services):
        module_list = self.get_module_list()
        for module in module_list:
            self.q.put({"class_": module["module"], "nmap_services": nmap_services, "target": target})

    def get_module(self, module, mname):
        class_ = getattr(module, mname)
        return class_

    def process_module(self, class_, nmap_services, target):
        kwargs = {}
        if class_.services[0] == "any":
            for arg in class_.args:
                kwargs[arg] = [service[arg] for service in nmap_services if arg in service]
            return self.invoke_module(class_, target, kwargs)
        if class_.multi:
            for service in nmap_services:
                if service['service'] in class_.services and service['state'] == "open":
                    for arg in class_.args:
                        kwargs[arg] = service[arg]
                    self.invoke_module(class_, target, kwargs)
        if not class_.multi:
            services = [service['service'] for service in nmap_services if
                        service['state'] == "open" and service['service'] in class_.services]
            if len(services) > 0:
                self.invoke_module(class_, target, kwargs)

    def invoke_module(self, class_, target, kwargs):
        # Sleep added because some module start messages couldn't print fast enough
        sleep(0.5)
        instance = class_(target, **kwargs)
        if instance.aggressive and not self.args.aggressive:
            return
        instance.run()
