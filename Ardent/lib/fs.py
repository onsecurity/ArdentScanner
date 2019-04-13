import os


def create_dir(path):
    path = path.strip()
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(e)
