import sys
import time
import string
import os

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
    # difficulty could modify how much the words are obscured at the start
    # difficulty  = 1

    def __init__(self, name):
        self.name = name

    def mod_score(self, score_modifier):
        self.score += score_modifier * 100

    def buy_powerup(self, power):
        #and self.score >= 100\
        self.score = self.score - 100
        if power == "A":
            print("Changing mode to NONE for 5 seconds")
            file = open("powerup.txt", "w")
            file.write("A")
            file.close()
        elif power == "B":
            print("Decreasing probabilty of flipped characters to 1/20 for 5 seconds")
            file = open("powerup.txt", "w")
            file.write("B") 
            file.close()
        elif power == "C":
            print("Slowing down text for 5 seconds")
            file = open("powerup.txt", "w")
            file.write("C")
            file.close()
        print(self.score)
    def clear_powerup(self):
        open("powerup.txt", "w").close()

    def check_powerup(self):
        file = open("powerup.txt", "r")
        b = True
        if file.read() == "":
            b = False
        return b


if __name__ == '__main__':

    guess_number = 0
    username = input("Input username: \n")
    p1 = Player(username)
    print(p1.score)
    g1 = Game("sampletext.txt")
    start_time = None
    end_bool = (open("powerup.txt", "r").read() == "END")
    while(not end_bool):
        user_input = input("Input index(starting at 0) followed by word guess or buy a powerup (A, B, C): \n")
        if user_input[0].isnumeric():
            result = g1.process_user_input(user_input, guess_number)
            if result > 0:
                p1.mod_score(result)
            guess_number += 1
            print(str(p1.score))
        else:
            if p1.check_powerup():
                print("Cannot use more than 1 powerup simultaneously\n")
            elif p1.score < 100:
                print("Not enough points to buy a powerup\n")
            else:
                p1.buy_powerup(user_input)
        end_bool = (open("powerup.txt", "r").read() == "END")
        # else:
        #     print("Unacceptable input")
    print("Game over \nScore: ", p1.score)
    open("powerup.txt", "w").close()