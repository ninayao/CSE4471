import sys
import time
from keylogger import Keylogger


def keylog_from_text(mode, text):
    k = Keylogger(mode)
    for char in text:
        k.simulated_key_pressed(char)
    return k.logged

def produce_text():
    f = open("sampletext.txt", "r")
    text = f.read()
    return text

def print_text(speed, text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.2)
    return text


if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "random"
    string_from_file = produce_text()
    text = keylog_from_text(mode, string_from_file)
    print_text(0, text)
