import sys
import time
from keylogger import Keylogger
import os
import socket, select, string


#def keylog_from_text(text):
    #config.k.change_mode(mode)
    #print(config.key.get_mode())
#    for char in text:
 #       config.k.simulated_key_pressed(char)
  #  return config.k.logged

def produce_text():
    f = open("sampletext.txt", "r")
    text = f.read()
    return text

def print_text(speed, text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    return text
def prompt_connection():
    address = input("Input address to connect to: \n")
    port = input("Input port to connect to:")
    return address, int(port) 

if __name__ == '__main__':

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "random"
    k = Keylogger(mode)
    string_from_file = produce_text()
    speed = 0.2

    host, port = prompt_connection()
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    try:
        s.connect((host, port))
    except:
        print('Connection error')
        sys.exit()
        
    print('Connected to host')

    start = None
    for char in string_from_file:
        socket_list = [s, sys.stdin]
        read_sockets, write, error = select.select(socket_list, [], [])
        sock = read_sockets[0]
        #print(sock)
        if sock is not s:
            c = k.simulated_key_pressed(char)
            print_text(speed, c)
            #print(speed)
            print(k.get_mode())
            #print(k.get_rand())
        else :
            data = sock.recv(4096)
            if data:
                p_up = data.decode()[-1]
                start = time.time()
                if p_up == "A":
                    k.change_mode("none")
                elif p_up == "B":
                    k.change_rand(20)
        end = time.time()
        if start is not None:
            if end - start >= 5:
                k.change_mode(mode)
                k.change_rand(10)
                start = None
