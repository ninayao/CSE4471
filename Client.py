import sys
import time
import string
import os
import socket, select

class Game:
    text_dict = []
    guessed_indices = []

    def __init__(self, filename):
        f = open(filename, "r")
        text = f.read()
        text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
        self.text_dict = text_no_punct.split(" ")
        self.score = 0

    def process_user_input(self, user_input, guess_number):
        arr = user_input.split()
        index = int(arr[0])
        #index = int(user_input[0])
        #word_guess = user_input[2:]
        word_guess = arr[1]
        if index in self.guessed_indices:
            print("Already guessed")
            return 0
        elif word_guess == self.text_dict[index]:
            self.guessed_indices.append(index)
            return len(word_guess)
        else:
            return 0

class Player:
    name = ""
    score = 0
    powerup = ""
    # difficulty could modify how much the words are obscured at the start
    # difficulty  = 1

    def __init__(self, name):
        self.name = name

    def mod_score(self, score_modifier):
        self.score += score_modifier * 100

    def buy_powerup(self, power):
        #and self.score >= 100\
        if power == "A":
            print("Changing mode to NONE for 5 seconds")
            #file = open("powerup.txt", "w")
            #file.write("A")
            #file.close()
            self.powerup = "A"
            self.score = self.score - 100
        elif power == "B":
            print("Decreasing probabilty of flipped characters to 1/20 for 5 seconds")
            #file = open("powerup.txt", "w")
            #file.write("B") 
            #file.close()
            self.powerup = "B"
            self.score = self.score - 100
        print(self.score)
    def clear_powerup(self):
        #open("powerup.txt", "w").close()
        self.powerup = ""

    '''
    def check_powerup(self):
        file = open("powerup.txt", "r")
        b = True
        if file.read() == "":
            b = False
        return b
    '''


if __name__ == '__main__':

    host = 'localhost'
    port = 8000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    try:
        s.connect((host, port))
    except:
        print('Connection error')
        sys.exit()
        
    print('Connected to host')
    #prompt()

    #socket_list = [sys.stdin, s]

    #read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    
    guess_number = 0
    username = input("Input username: \n")
    p1 = Player(username)
    print(p1.score)
    g1 = Game("sampletext.txt")
    #end_bool = open("powerup.txt", "r").read() == "END"
    while True:
        user_input = input("Input index (starting at 0) followed by word guess or buy a powerup [A (900), B (300), C (600)]: \n")
        if user_input[0].isnumeric():
            result = g1.process_user_input(user_input, guess_number)
            if result > 0:
                p1.mod_score(result)
            guess_number += 1
            print(str(p1.score))
        else:
            
            if p1.score < 100:
                print("Not enough points to buy a powerup\n")
            else:
                s.send(user_input.encode())
                p1.buy_powerup(user_input)
        #end_bool = open("powerup.txt", "r").read() == "END"
        # else:
        #     print("Unacceptable input")
    print("Game over \nScore: ", p1.score)
    open("powerup.txt", "w").close()