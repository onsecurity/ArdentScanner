from Ardent.lib.template import Task


class NbtScan(Task):

    services = ["netbios-ssn"]

    def __init__(self, target):
        super(NbtScan, self).__init__(target)
        self.name = "NBT_Scan"
        self.cmd = "nbtscan %s > %s/nbtscan.txt" % (self.target, self.path)


class SmbMap_Null(Task):

    services = ["netbios-ssn"]

    def __init__(self, target):
        super(SmbMap_Null, self).__init__(target)
        self.name = "Smbmap null session"
        self.cmd = "smbmap -H %s -u '' -p '' > %s/smbmap_null.txt" % (self.target, self.path)


class SmbMap_Guest(Task):

    services = ["netbios-ssn"]

    def __init__(self, target, user="test", password="test"):
        super(SmbMap_Guest, self).__init__(target)
        self.name = "Smbmap Guest"
        self.cmd = "smbmap -H %s -u '%s' -p '%s5' > %s/smbmap_guest.txt" % (self.target, user, password, self.path)


class Enum4Linux(Task):

    services = ["netbios-ssn"]

    def __init__(self, target):
        super(Enum4Linux, self).__init__(target)
        self.name = "Enum4Linux"
        self.cmd = "enum4linux %s 2>/dev/null > %s/enum4linux.txt" % (self.target, self.path)


class SMBNmap(Task):

    services = ["netbios-ssn"]

    def __init__(self, target):
        super(SMBNmap, self).__init__(target)
        self.name = "SMBNmap scans"
        self.use_subdir("nmap")
        self.cmd = "nmap -sV -Pn -vv -p 139, 445\
         --script=\"(smb*) and not (brute or broadcast or dos or external or fuzzer)\"\
          --script-args=unsafe=1 %s -oA %s/smb_nmap" % (self.target, self.path)
