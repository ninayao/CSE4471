import sys
import time
from CSE4471.keylogger import Keylogger
import string

class Game:
    text_dict = []

    def __init__(self, filename):
        f = open(filename, "r")
        text = f.read()
        text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
        self.text_dict = text_no_punct.split(" ")
        self.score = 0

    def process_user_input(self, user_input, guess_number):
        index = int(user_input[0])
        word_guess = user_input[2:]
        if word_guess == self.text_dict[index]:
            return len(word_guess)
        else:
            return 0

class Player:
    name = ""
    score = 0
    # difficulty could modify how much the words are obscured at the start
    # difficulty  = 1

    def __init__(self, name):
        self.name = name

    def mod_score(self, score_modifier):
        self.score += result * 100

    # def buy_powerup(self, game, powerup):


if __name__ == '__main__':
    guess_number = 0
    username = input("input username: \n")
    p1 = Player(username)
    g1 = Game("sampletext.txt")
    while(1):
        user_input = input("input index(starting at 0) followed by word guess: \n")
        if user_input[0].isnumeric():
            result = g1.process_user_input(user_input, guess_number)
            if result > 0:
                p1.mod_score(result)
            guess_number += 1
            print(str(p1.score))
        # elif user_input == "buy":
        #
        # else:
        #     print("Unacceptable input")