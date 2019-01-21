# What is this?

Ardent scanner is a fully automated, extensible, dynamic command line enumeration tool.
It is in many ways very similar to sparta, except it logs everything to flat files.

## Installation

Run `python setup.py` to install Ardent Scan.

Please note: Due to the tools used by this project, compatibility can only be ensured when using Kali Linux.

## Usage 

For a list of options, run `ardent --help`.

To see a list of installed modules, run `ardent --list` 

Typical usage for scanning multiple hosts is as follows: `ardent host1 host2 host3`

Supplying a file containing targets is also supported via `ardent -iL targets.txt`

Some Modules such as Dirbuster and Nikto are marked as aggressive. To enable aggressive modules, use the `-A` flag.


All output will be saved in `~/.ardent/`. This can be changed in `settings.py`

## Writing your own tests 
Ardent Scanner utilities reflective programming techniques to dynamically execute user defined modules depending on open ports discovered by the port scanning tool 'nmap'. For the most part, currently implemented modules simply handle the execution of enumeration scripts, however, writing entirely custom modules is also possible. 

To avoid overloading hosts with a high volume of network traffic Ardent Scanner utilizes thread pools to achieve concurrent enumeration whilst limiting the number of active modules. Via the settings.py file, it is possible to configure how many hosts may be scanned at one time, as well as how many modules may be executed against each host in parallel. Currently Ardent Scanner outputs all enumeration results in the form text files in a well organized directory structure. I have tried to make extending Ardent Scan as painless as possible. In the following sections we shall go through some examples of possible Ardent Modules.

Below you see an example module which triggers when the initial nmap scan detects the service "netbios-ssn". As you can see, this is defined by the services property. The class then defines it's constructor, which begins the instantiation by called the parent class Task's constructor. The Modules human readable name is then defined, as well as the command which is executed by the module. All you have to do for your Module to be executed by Ardent is place it in the Modules directory and the framework will take care of the rest.
```
class Enum4Linux(Task):
    
    # Defines the service whose detection should trigger this module
    services = ["netbios-ssn"]

    def __init__(self, target):
        super(Enum4Linux, self).__init__(target)
        self.name = "Enum4Linux"
        self.cmd = "enum4linux %s 2>/dev/null >%s/enum4linux.txt" % (self.target, self.path)
```
Furthermore, you can specify modules which should be run once against each host regardless of which services are identified. Below you see the FullNamp Module which runs once the basic nmap scan has been completed. The FullNmap module also specifies port as a required argument. As a result, Ardent will iterate through services from the initial nmap result, extracting the port field from each one and passing it to the FullNmap module as a list. You may supply any number of args, and they will be retrieved from the initial nmap scan and passed as key word arguments to the modules constructor. For more information on the available args I reccomend you consult the python-libnmap docs.

Additionally you use the self.use_subdir(dirname) method to create a new subdirectory to store the modules results, and update the Modules path attribute, which can be used to refer to the Modules output directory.
```
class FullNmap(Task):
    # Run once regardless of service detected
    services = ["any"]
    
    # args defines the values which should be retrieved from the Nmap results and passed to the module.
    # In this instance, all ports will be extacted and passed to the module. All ports are retrieved as
    # 'services' is defined as "any"
    args = ["port"]

    def __init__(self, target, port):
        super(FullNmap, self).__init__(target)
        self.name = "Full TCP Scan"
        
        # Here we tell Ardent to store the output in a subdirectory of the targets directory.
        self.use_subdir("nmap")
        
        port_list = ",".join(port)
        self.cmd = "nmap -p %s -sS -sV -sC -A -O %s -oA %s/full_tcp" % (port_list, self.target, self.path)
 ```

In instances where you wish to specify the same Module attributes for multiple Modules, you may create a descriptor class such as theHTTPModules class seen below, and then utilize multiple inheritance to provide these attributes to a Module.
```
class HTTPModules(object):
    args = ["port", "service"]
    services = ["http", "ssl", "https"]
    multi = True


class Dirb(Task, HTTPModules):
    # Specifies this module should only execute if Ardent is run in Aggressive mode (-A)
    aggressive = True

    def __init__(self, target, port, service):
        super(Dirb, self).__init__(target)
        self.name = "Dirb on port %s" % port
        self.proto = "http://"
        if "ssl" in service or "https" in service:
            self.proto = "https://"
        self.cmd = "dirb %s%s:%s -o %s/dirb_%s.txt" % (self.proto, self.target, port, self.path, port)
```
Modules are executed by the framework by calling a Modules run method, which prints the start message, invokes self.action(), and then finally prints the end message. Below you can see the default action method inherited by Modules from the Task class. To write Modules which perform completely bespoke actions, simply override the action Method within your own module classes.
```
class Task(object):

  ---- Snipped ----
  
     def action(self):
        FNULL = open(devnull, 'w')
        p = subprocess.Popen(self.cmd, shell=True, stdout=FNULL, stderr=FNULL)
        p.wait()
  
  ---- Snipped ---`

