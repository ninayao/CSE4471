import sys
import time
from keylogger import Keylogger
import os


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


if __name__ == '__main__':

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "random"
    k = Keylogger(mode)
    string_from_file = produce_text()
    speed = 0.2
    start = None
    p_bool = False
    #text = keylog_from_text(mode, string_from_file)
    for char in string_from_file:
        file = open("powerup.txt", "r")
        p_up = file.read()
        if p_bool == False:
            if p_up == "A" or p_up == "B" or p_up == "C":
                p_bool = True
                start = time.time()
                if p_up == "A":
                    k.change_mode("none")  
                elif p_up == "B":
                    k.change_rand(20)
                elif p_up == "C":
                    speed = 0.5
        end = time.time()    
        if start is not None:
            elapsed = end - start
            if elapsed >= 5:
                open("powerup.txt", "w").close()
                k.change_mode(mode)
                k.change_rand(10)
                speed = 0.2    
                p_bool = False        
        c = k.simulated_key_pressed(char)
        print_text(speed, c)
        #print(speed)
        #print(k.get_mode())
        #print(k.get_rand())
    file = open("powerup.txt", "w")
    file.write("END")    
