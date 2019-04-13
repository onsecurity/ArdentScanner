from Ardent.lib.template import Task
from Ardent.settings import RESOURCES_DIR

"""
class BruteSMTPUsers(Task):
    services = ["smtp"]
    aggressive = True

    def __init__(self, target, port=None):
        super(BruteSMTPUsers, self).__init__(target)
        self.name = "SMTP User Enum"

    def worker(self):
        import threading
        import Queue
        import socket

        def user_check(user, s, of):
            s.send("VRFY %s\r\n" % user.strip())
            result = s.recv(1024)
            if result.split(" ")[0] == "250":
                of.write(user + "\n")
            elif result.split(" ")[0] == "502":
                of.write(result + "\n")

        def thread(ip, q, of):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = s.connect((ip, 25))
            banner = s.recv(1024)
            while True:
                item = q.get()
                user_check(item, s, of)
                q.task_done()

        print self.start_msg()

        q = Queue.Queue()
        of = open(self.path + "/smtp_users.txt", 'w+r')
        threads = []
        for i in range(50):
            t = threading.Thread(target=thread, kwargs={'ip': self.target, 'q': q, 'of': of})
            t.daemon = True
            t.start()

        names_path = RESOURCES_DIR + "/names.txt"
        with open(names_path, 'r') as users:
            for user in users:
                q.put(user)
        q.join()
        of.seek(0)
        if "502" in of.readline():
            self.err = "VRFY not supported"
            of.truncate()
        print self.end_msg()
"""