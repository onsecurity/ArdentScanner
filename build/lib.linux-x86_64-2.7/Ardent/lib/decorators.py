from Ardent import settings


def stdout(func):
    def wrapper(*args, **kwargs):
        if settings.OUTPUT_MODE == "none":
            return
        buffer = func(*args, **kwargs)
        if settings.OUTPUT_MODE == "print":
            print "\033[H\033[J"
            print buffer
    return wrapper
