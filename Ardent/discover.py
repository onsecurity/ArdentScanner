from Ardent.lib import fs
from Ardent.lib.template import Task
from Ardent import settings
import subprocess
import threading


class Discovery(object):

    def __init__(self, wildcard):
        self.wildcard = wildcard
        fs.create_dir(settings.BASE_DIR)

    def discover(self):
        threads = []
        discovery_modules = [
            Subfinder(self.wildcard),
            Amass(self.wildcard)
        ]

        for discovery_module in discovery_modules:
            t = threading.Thread(target=discovery_module.run())
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        raw_domains = [item.lstrip(".") for sublist in [discovery_module.get_results() for discovery_module in discovery_modules] for item in sublist]

        return list(set(raw_domains))


class Subfinder(Task):
    def __init__(self, wildcard):
        self.wildcard = wildcard
        self.output_file = settings.BASE_DIR + "subfinder/" + self.wildcard

    def run(self):
        fs.create_dir(settings.BASE_DIR + "subfinder/")
        cp = subprocess.run(["subfinder", "-d", self.wildcard, "-o", self.output_file], stdout=subprocess.DEVNULL)

    def get_results(self):
        with open(self.output_file, 'r') as f:
            return [line.strip() for line in f]


class Amass(Task):
    def __init__(self, wildcard):

        self.wildcard = wildcard
        self.output_file = settings.BASE_DIR + "amass/" + self.wildcard

    def run(self):
        fs.create_dir(settings.BASE_DIR + "amass/")

        cp = subprocess.run(["amass", "-d", self.wildcard, "-o", self.output_file, "-active"], stdout=subprocess.DEVNULL)

    def get_results(self):
        with open(self.output_file, 'r') as f:
            return [line.strip() for line in f]
