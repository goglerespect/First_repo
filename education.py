from contextlib import contextmanager
from datetime import datetime


@contextmanager
def managed_resource(*args, **kwargs):
    log = ''
    timestamp = datetime.now().timestamp()
    msg = f'{timestamp:<20}|{args[0]:^15}| open \n'
    log += msg
    file_handler = open(*args, **kwargs)
    try:
        yield file_handler
    finally:
        diff = datetime.now().timestamp() - timestamp
        msg = f'{timestamp:<20}|{args[0]:^15}| closed {round(diff, 6):>15}s \n'
        log += msg
        file_handler.close()
        print(log)


with managed_resource('new_file.txt', 'r') as f:
    print(f.read())