import sys
import time
import string
import os
import tkinter as tk
from tkinter import *

guessed_indices = []
name = ""
wordNum = 1
score = 0

def countdown(count):
    # change text in label        
    clock_time.set(str(count))

    if count >= 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count+1)

def get_name(event=None):
    #gets the name entered from the first screen
    global name 
    name = name_var.get()
    instruction_page()

def instruction_page():
    #get rid of name entry widgets
    enterName.destroy()
    nameEntry.destroy()
    nameButton.destroy()
    #global bc we need to destroy them in another function
    global greeting, instruc, beginButton
    #print instructions
    greeting = tk.Label(root, text="Hi "+name+"!", bg="light blue")
    greeting.grid(row=0)
    greeting.place(relx=0.5, rely=0.10, anchor=CENTER)
    instruc = tk.Label(root, text="Instructions:\n\nOn the next screen, you will see text printing with multiple errors throughout. Your goal is to decipher what the text is supposed to say, and enter it word by word.\n\nThere will be a text entry box where you will enter the indicated word. When you hit submit, you will be told whether your guess was correct or not, and your score will be adjusted accordingly.\n\nWhen enough points have been acquired, you may purchase a power-up by clicking the buttons labeled \"pwr 1\", \"pwr 2\", and \"pwr 3\". The power-ups will give you an advantage by decreasing the amount of bugs you encounter or by slowing down your opponents text speed.\n\n\nGood Luck!", bg="light blue", wraplength=420)
    instruc.grid(row=1)
    instruc.place(relx=0.5, rely=0.50,anchor=CENTER)
    beginButton = tk.Button(root, command=set_up_gui, text="start the game")
    beginButton.grid(row=3)
    beginButton.place(relx=0.5, rely=0.92,anchor=CENTER)
    root.bind('<Return>',set_up_gui)


def set_up_gui(event=None):
    global outputTxt
    #get rid of instruction widgets
    greeting.destroy()
    instruc.destroy()
    beginButton.destroy()
    scr.set(name+"'s Score: "+str(score))
    #sets up the game layout
    wordNumText.set("Word #1")
    yourScore = tk.Label(root, textvariable=scr).grid(row=0, column=0, sticky=W)
    opsScore = tk.Label(root, text="Op Score: 0").grid(row=0, column=1, sticky=W)
    pwr1 = tk.Button(root, command=choose_pwr_1, text="pwr 1").grid(row=0, column=2)
    pwr2 = tk.Button(root, command=choose_pwr_2, text="pwr 2").grid(row=0, column=3)
    pwr3 = tk.Button(root, command=choose_pwr_3, text="pwr 3").grid(row=0, column=4)
    tk.Label(root, text="Text to Type:", bg="light blue").grid(row=2, sticky=W)
    tk.Label(root, textvariable=wordNumText, bg="light blue").grid(row=4, column=0, sticky=W)
    tk.Label(root, text="Your guess:", bg="light blue").grid(row=4, column=1, sticky=W)
    tk.Label(root, text="Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then", bg="yellow", wraplength=420, justify=LEFT).grid(row=2, columnspan=6)
    root.geometry("420x380")
    root.configure(bg="light blue")
    textEntry = tk.Entry(root, textvariable=text_var)
    textEntry.grid(row=4, column=2, columnspan=2, sticky=W)
    submitBtn = tk.Button(root, command=word_entered, text="submit").grid(row=4, column=4)
    root.bind('<Return>',word_entered)
    output.set("Enter the word at position "+str(wordNum)+"!")
    clock = tk.Label(root, textvariable=clock_time)
    clock.grid(row=6, column=0)
    countdown(0)
    outputTxt = tk.Label(root, textvariable=output, bg="light blue")
    outputTxt.grid(row=6, column=1, columnspan=4)
    root.grid_rowconfigure(1, minsize=20) 
    root.grid_rowconfigure(3, minsize=20)  
    root.grid_rowconfigure(5, minsize=20)  

def word_entered(event=None):
    #gets the word the user guessed
    input = text_var.get()
    print(input)
    text_var.set("")
    process_user_input(input)

def process_user_input(user_input):
    #checks if guess is right
    global wordNum
    word_guess = user_input
    index= wordNum -1
    if word_guess == text_dict[index]:
        guessed_indices.append(index)
        output.set("Correct!")
        outputTxt.config(fg="green3")
        mod_score(len(word_guess))
        mod_word_num()
        return len(word_guess)
    else:
        output.set("Incorrect :(")
        outputTxt.config(fg="red2")
        return 0

def mod_score(score_modifier):
    #modifies score if guess is right
    global score
    score += score_modifier * 100
    scr.set(name+"'s Score: "+str(score))

def mod_word_num():
    global wordNum
    wordNum +=1
    wordNumText.set("Word #"+str(wordNum))

def check_powerup():
    file = open("powerup.txt", "r")
    b = True
    if file.read() == "":
        b = False
    return b

def clear_powerup():
    open("powerup.txt", "w").close()

def choose_pwr_1():
    global score
    outputTxt.config(fg="black")
    if(check_powerup()):
        output.set("You can't use more than 1 power up at a time!")
    elif score<900:
        output.set("You don't have enough points!")
    else:
        output.set("Changing mode to NONE for 5 seconds")
        file = open("powerup.txt", "w")
        file.write("1")
        file.close()
        mod_score(-9)
    return

def choose_pwr_2():
    global score
    outputTxt.config(fg="black")
    if(check_powerup()):
        output.set("You can't use more than 1 power up at a time!")
    elif score<300:
        output.set("You don't have enough points!")
    else:
        output.set("Decreasing probabilty of flipped characters to 1/20 for 5 seconds")
        file = open("powerup.txt", "w")
        file.write("2") 
        file.close()
        mod_score(-3)
    return

def choose_pwr_3():
    global score
    outputTxt.config(fg="black")
    if(check_powerup()):
        output.set("You can't use more than 1 power up at a time!")
    elif score<600:
        output.set("You don't have enough points!")
    else:
        output.set("Slowing down text for 5 seconds")
        file = open("powerup.txt", "w")
        file.write("3")
        file.close()
        mod_score(-6)
    return

#opens text document
f = open("sampletext.txt", "r")
text = f.read()
text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
text_dict = text_no_punct.split(" ")

#set up GUI
root = tk.Tk()
root.title("typing game")
root.configure(bg="light blue")

#GUI stringVars
scr = StringVar()
output = StringVar()
wordNumText = StringVar()
text_var = StringVar()
name_var = StringVar()
clock_time = StringVar()

#username enttry widgets
root.geometry("420x380")
welcome = tk.Label(root, text="Welcome to the typing game!", bg="light blue")
welcome.grid(row=0)
welcome.place(relx=0.5, rely=0.25, anchor=CENTER)
enterName = tk.Label(root, text="Enter your name", bg="light blue")
enterName.grid(row=1)
enterName.place(relx=0.5, rely=0.35,anchor=CENTER)
nameEntry = tk.Entry(root, textvariable=name_var)
nameEntry.grid(row=2)
nameEntry.place(relx=0.5, rely=0.45,anchor=CENTER)
nameButton = tk.Button(root, command=get_name, text="submit")
nameButton.grid(row=3)
nameButton.place(relx=0.5, rely=0.55,anchor=CENTER)
root.bind('<Return>',get_name)


#start game loop
root.mainloop()
