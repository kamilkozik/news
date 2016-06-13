import hashlib
import time


def filename64hex(file_name, n):
    now = str(time.time()).replace('.', '')
    return hashlib.sha256(now + file_name).hexdigest()[:n]


def number64hex(number, n):
    str_from_number = str(number)
    return hashlib.sha256(str_from_number).hexdigest()[:n]
