from Ardent.lib.template import Task


class FullNmap(Task):
    services = ["any"]
    args = ["port"]

    def __init__(self, target, port):
        super(FullNmap, self).__init__(target)
        self.name = "Full TCP Scan"
        self.use_subdir("nmap")
        port_list = ",".join(port)
        self.cmd = "nmap -p %s -sS -sV -sC -A -O %s -oA %s/full_tcp" % (port_list, self.target, self.path)
        # self.cmd = "nmap -sS -sV -sC -A -O %s -oA %s/full_tcp" % (self.target, self.path)


class UDPNmap(Task):
    services = ["any"]

    def __init__(self, target):
        super(UDPNmap, self).__init__(target)
        self.name = "UDP Scan"
        self.use_subdir("nmap")
        self.cmd = "nmap -sU -sC %s -oA %s/udp" % (self.target, self.path)
