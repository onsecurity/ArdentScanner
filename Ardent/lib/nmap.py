from libnmap.parser import NmapParser
from libnmap.process import NmapProcess


def scan_services(target):
    nm = NmapProcess(target, options="-sV")
    rc = nm.run()
    services = []
    parsed = NmapParser.parse(nm.stdout)
    for host in parsed.hosts:
        for serv in host.services:
            services.append(serv.get_dict())
    return services
