from Ardent.lib.template import Task


class HTTPModules(object):
    args = ["port", "service"]
    services = ["http", "ssl", "https"]
    multi = True


class Dirb(HTTPModules, Task):
    aggressive = True

    def __init__(self, target, port, service):
        super(Dirb, self).__init__(target)
        self.port = port
        self.name = "Dirb"
        self.proto = "http://"
        if "ssl" in service or "https" in service:
            self.proto = "https://"
        self.cmd = "dirb %s%s:%s -o %s/dirb_%s.txt" % (self.proto, self.target, self.port, self.path, self.port)


class TestSSL(HTTPModules, Task):

    def __init__(self, target, port, service):
        super(TestSSL, self).__init__(target)
        self.port = port
        self.name = "TestSSL"
        self.port = port
        self.cmd = "/opt/testssl.sh/testssl.sh -oJ %s/testssl_%s.json --append https://%s:%s" % (self.path, self.port, self.target, self.port)


class Nikto(HTTPModules, Task):
    aggressive = True

    def __init__(self, target, port, service):
        super(Nikto, self).__init__(target)
        self.name = "Nikto"
        self.port = port
        self.proto = "http://"
        if "ssl" in service or "https" in service:
            self.proto = "https://"
        self.cmd = "nikto -h %s%s:%s > %s/nikto_%s.txt" % (self.proto, target, self.port, self.path, self.port)


class Screenshot(HTTPModules, Task):

    def __init__(self, target, port, service):
        super(Screenshot, self).__init__(target)
        self.name = "Screenshot"
        self.port = port
        self.use_subdir("screenshots")
        self.proto = "http://"
        if "ssl" in service or "https" in service:
            self.proto = "https://"
        self.cmd = "cutycapt --insecure --url=%s%s --out=%s/%s.png" % (self.proto, self.target, self.path, self.port)

