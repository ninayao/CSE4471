import sys
import time
import string
import os
import tkinter as tk
from tkinter import *
from keylogger import Keylogger
import math
import socket
from Client import Game, Player

guessed_indices = []
name = ""
address = ""
port = 0
wordNum = 1
score = 0
start = None
sock = None
text_input = ""
test_string = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then"
clock1 = None
t = None
instr = None
caesar_input = ""
caesar_shift = ""
text_dict= []

def countdown(count):
    global score
    # change text in label        
    clock_time.set(str(count))

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else :
        output.set("Game Over!\nScore: "+str(score))
      

def get_name(event=None):
    #gets the name entered from the first screen
    global name 
    global address
    global port
    name = name_var.get()
    address = address_var.get()
    port = int(port_var.get())
    game()

def instruction_page():
    global address
    global port
    global SOCKET_CONNECTION
    global test_string
    global text_string
    global text_dict
    global instr
    global clock1
    global t

    t.destroy()
    instr.destroy()
    clock1.destroy()

    address_with_port = address, port
    SOCKET_CONNECTION = socket.socket()
    SOCKET_CONNECTION.connect(address_with_port)
    SOCKET_CONNECTION.sendall(bytes(text_input, 'utf-8'))

    test_string = SOCKET_CONNECTION.recv(1024).decode()
    print(test_string)

    gen_text_dict(test_string)

    #global bc we need to destroy them in another function
    global greeting, instruc, beginButton
    #print instructions
    greeting = tk.Label(root, text="Hi "+name+"!", bg="light blue")
    greeting.grid(row=0)
    greeting.place(relx=0.5, rely=0.10, anchor=CENTER)
    instruc = tk.Label(root, text="Instructions:\n\nOn the next screen, you will see text printing with multiple errors throughout. Your goal is to decipher what the text is supposed to say, and enter it word by word.\n\nThere will be a text entry box where you will enter the indicated word. When you hit submit, you will be told whether your guess was correct or not, and your score will be adjusted accordingly. You also have the option to skip a word and move on to the next.\n\nWhen enough points have been acquired, you may purchase power-up by clicking the buttons labeled \"pwr 1\" and \"pwr 2\". The power-ups will give you an advantage by decreasing the amount of bugs you encounter. \n\n\nGood Luck!", bg="light blue", wraplength=420)
    instruc.grid(row=1)
    instruc.place(relx=0.5, rely=0.50,anchor=CENTER)
    beginButton = tk.Button(root, command=set_up_gui, text="start the game")
    beginButton.grid(row=3)
    beginButton.place(relx=0.5, rely=0.92,anchor=CENTER)
    root.bind('<Return>',set_up_gui)


def set_up_gui(event=None):
    global outputTxt
    global delta
    global test_string
    #get rid of instruction widgets
    greeting.destroy()
    instruc.destroy()
    beginButton.destroy()
    scr.set(name+"'s Score: "+str(score))
    #sets up the game layout
    wordNumText.set("Word #1")

    k = Keylogger("random")

    yourScore = tk.Label(root, textvariable=scr).grid(row=0, column=0, sticky=W)
    opsScore = tk.Label(root, textvariable=o_scr).grid(row=0, column=1, sticky=W)
    pwr1 = tk.Button(root, command= skip, text="skip").grid(row=0, column=2)
    pwr2 = tk.Button(root, command= lambda: choose_pwr_2(k), text="pwr 1").grid(row=0, column=3)
    # CHANGED TO 4 TO TEST CAESAR
    pwr3 = tk.Button(root, command= lambda: choose_pwr_4(k), text="pwr 2").grid(row=0, column=4)
    tk.Label(root, text="Text to Type:", bg="light blue").grid(row=2, sticky=W)
    tk.Label(root, textvariable=wordNumText, bg="light blue").grid(row=4, column=0, sticky=W)
    tk.Label(root, text="Your guess:", bg="light blue").grid(row=4, column=1, sticky=W)

    #tk.Label(root, text="Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then", bg="yellow", wraplength=420, justify=LEFT).grid(row=2, columnspan=6)
    
    
    #print out text by char
    #canvas = tk.Canvas(root, width=650, height=200)
    canvas.grid(row=3, column=0, columnspan = 5, sticky = tk.W+tk.E)
    #canvas_text = canvas.create_text(10, 10, anchor=tk.NW, width=640)
    print_text(k, test_string, "")
    '''
    delta= 200
    delay = 0
    s = ""
    for c in test_string:
        new_c = k.simulated_key_pressed(c)
        s = s + new_c
        update_text = lambda s=s: canvas.itemconfigure(canvas_text, text=s)
        canvas.after(delay, update_text)
        delay += delta 
    '''
    root.geometry("700x500")
    root.configure(bg="light blue")
    textEntry = tk.Entry(root, textvariable=text_var)
    textEntry.grid(row=4, column=2, columnspan=2, sticky=W)
    submitBtn = tk.Button(root, command=word_entered, text="submit").grid(row=4, column=4)
    root.bind('<Return>',word_entered)
    output.set("Enter the word at position "+str(wordNum)+"!")
    clock = tk.Label(root, textvariable=clock_time)
    clock.grid(row=6, column=0)

    #countdown(5)
    countdown(math.ceil(len(test_string)*200/1000))

    outputTxt = tk.Label(root, textvariable=output, bg="light blue")
    outputTxt.grid(row=6, column=1, columnspan=4)
    root.grid_rowconfigure(1, minsize=20) 
    root.grid_rowconfigure(3, minsize=20)  
    root.grid_rowconfigure(5, minsize=20)  

def countdown2(count):
    global text_input
    # change text in label        
    clock_time2.set(str(count))

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown2, count-1)
    else:
        print(text_input)
        '''
        for client in connections:
            client.sendall(bytes(text_input, 'utf-8'))
        '''
        instruction_page()

def onKeyPress(event):
    global text_input
    text_input += event.char

def game():
    global instr
    global clock1
    global t

    #get rid of name entry widgets
    welcome.destroy()
    enterName.destroy()
    nameEntry.destroy()
    nameButton.destroy()
    enterAddress.destroy()
    enterPort.destroy()
    addressEntry.destroy()
    portEntry.destroy()

    instr = tk.Label(root, text="Type here:")
    instr.grid(row=0, column=1, sticky=W)
    t = Text(root, height=20, width=90)
    t.grid(row=1, column=1)
    clock1 = tk.Label(root, textvariable=clock_time2)
    clock1.grid(row=0, column=1, columnspan=2)
    countdown2(30)
    root.bind('<KeyPress>', onKeyPress)

def print_text(k, test_string, s):
    global start
    end = time.time()
    if start is not None:
        elapsed=end - start
        if elapsed >= 5:
            reset(k)
            start = None
    if len(test_string) > 0:
        #print(k.get_rand())
        c = test_string[0]
        new_c = k.simulated_key_pressed(c)
        s += new_c
        canvas.itemconfigure(canvas_text, text=s)
        canvas.after(200, print_text, k, test_string[1:], s)   


def word_entered(event=None):
    #gets the word the user guessed
    input = text_var.get()
    #print(input)
    text_var.set("")
    # SOCKET_CONNECTION.sendall(bytes(input, 'utf-8'))
    # recieved = SOCKET_CONNECTION.recv(1024).decode()
    # output.set(recieved)
    process_user_input(input)

# make this send data over connection???
def process_user_input(user_input):
    #checks if guess is right
    global wordNum
    global text_dict
    word_guess = user_input
    index = wordNum -1
    if word_guess == text_dict[index]:
        guessed_indices.append(index)
        output.set("Correct!")
        outputTxt.config(fg="green3")
        # mod_score(len(word_guess))
        mod_word_num()
        
        SOCKET_CONNECTION.sendall(bytes(str(len(word_guess)), 'utf-8'))
        scores = SOCKET_CONNECTION.recv(1024).decode().split()
        for score in scores:
            if score is None:
                score = "0"

        scr.set("p1's score: " + str((scores[0])))
        o_scr.set("p2's score: " + str(scores[1]))
        
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


def check_powerup(k):
    b = False
    if k.get_mode() == "none" or k.get_rand() == 20:
        b = True
    return b

def reset(k):
    k.change_mode("random")
    k.change_rand(10)

def skip():
    #outputTxt.config(fg="black")
    output.set("Skipped!")
    mod_word_num()
    return

def choose_pwr_2(k):
    global score
    global start
    #outputTxt.config(fg="black")
    if(check_powerup(k)):
        output.set("You can't use more than 1 power up at a time!")
    elif score<600:
        output.set("You don't have enough points!")
    else:
        output.set("Changing mode to NONE for 5 seconds")
        k.change_mode("none")
        start = time.time()
        mod_score(-6)
    return

def choose_pwr_3(k):
    global score
    global start
    #outputTxt.config(fg="black")
    if(check_powerup(k)):
        output.set("You can't use more than 1 power up at a time!")
    elif score<300:
        output.set("You don't have enough points!")
    else:
        output.set("Decreasing probabilty of flipped characters to 1/20 for 5 seconds")
        k.change_rand(20)
        start = time.time()
        mod_score(-3)
    return

def choose_pwr_4(k):
    global score
    global start
    #outputTxt.config(fg="black")
    if(check_powerup(k)):
        output.set("You can't use more than 1 power up at a time!")
    # elif score<100:
    #     output.set("You don't have enough points!")
    else:
        output.set("Caesar cipher decryptor purchased")
        caesarInput = tk.Entry(root, textvariable=caesar_input)
        caesarInput.grid(row=5, column=2, columnspan=2, sticky=W)
        shiftInput = tk.Entry(root, textvariable=caesar_shift)
        shiftInput.grid(row=5, column=4, columnspan=2, sticky=W)
        start = time.time()
        #mod_score(0)
    return

#opens text document
def gen_text_dict(text_str):
    global text_dict
    #f = open("sampletext.txt", "r")
    #text = f.read()
    text_no_punct = text_str.translate(str.maketrans('', '', string.punctuation))
    text_dict = text_no_punct.split(" ")

#set up GUI
root = tk.Tk()
root.title("typing game")
root.configure(bg="light blue")

#GUI stringVars
scr = StringVar()
o_scr = StringVar()
output = StringVar()
wordNumText = StringVar()
text_var = StringVar()
name_var = StringVar()
clock_time = StringVar()
clock_time2 = StringVar()
address_var =StringVar()
port_var =StringVar()

canvas = tk.Canvas(root, width=650, height=200)
canvas_text = canvas.create_text(10, 10, anchor=tk.NW, width=640)


#username enttry widgets
root.geometry("700x500")
welcome = tk.Label(root, text="Welcome to the typing game!", bg="light blue")
welcome.grid(row=0)
welcome.place(relx=0.5, rely=0.15, anchor=CENTER)
enterName = tk.Label(root, text="Enter your name", bg="light blue")
enterName.grid(row=1)
enterName.place(relx=0.5, rely=0.25,anchor=CENTER)
nameEntry = tk.Entry(root, textvariable=name_var)
nameEntry.grid(row=2)
nameEntry.place(relx=0.5, rely=0.35,anchor=CENTER)
nameButton = tk.Button(root, command=get_name, text="submit")
nameButton.grid(row=7)
nameButton.place(relx=0.5, rely=0.85,anchor=CENTER)

enterAddress = tk.Label(root, text="Enter address", bg="light blue")
enterAddress.grid(row=3)
enterAddress.place(relx=0.5, rely=0.45,anchor=CENTER)
addressEntry = tk.Entry(root, textvariable=address_var)
addressEntry.grid(row=4)
addressEntry.place(relx=0.5, rely=0.55,anchor=CENTER)
enterPort = tk.Label(root, text="Enter port number", bg="light blue")
enterPort.grid(row=5)
enterPort.place(relx=0.5, rely=0.65,anchor=CENTER)
portEntry = tk.Entry(root, textvariable=port_var)
portEntry.grid(row=6)
portEntry.place(relx=0.5, rely=0.75,anchor=CENTER)

root.bind('<Return>',get_name)


#start game loop
root.mainloop()
