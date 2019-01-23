import os


def create_dir(path):
    path = path.strip()
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError as e:
            pass

