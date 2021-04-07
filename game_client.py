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
p1score = 0
start = None
sock = None
text_input = ""
test_string = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then"
clock1 = None
t = None
instr = None
caesar_count = 0
player_number= ""
text_dict= []
usedCaesar = 0

def countdown(count):
    global score
    # change text in label        
    clock_time.set(str(count))

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else :
        SOCKET_CONNECTION.sendall(bytes("end", 'utf-8'))
        end_string = SOCKET_CONNECTION.recv(1024).decode()
        if(end_string=="end"):
            end_game()

def end_game():
    global word_guess
    global p1score
    global scores
    global player_score
    global yourScore, opsScore, clock, pwr1, pwr2, pwr3, textToType, wordCount, guessBox, textEntry, canvas, submitBtn, outputTxt 
    global caesarText, caesarInput, shiftText, shiftInput, caesarButton

    #get score when timer runs out
    SOCKET_CONNECTION.sendall(bytes("0", 'utf-8'))
    scores = SOCKET_CONNECTION.recv(1024).decode().split()

    #destroy all widgets for game-play
    yourScore.destroy()
    opsScore.destroy()
    clock.destroy()
    pwr1.destroy()
    pwr2.destroy()
    pwr3.destroy()
    pwr4.destroy()
    pwr5.destroy()
    pwr6.destroy()
    textToType.destroy()
    wordCount.destroy()
    guessBox.destroy()
    textEntry.destroy()
    canvas.destroy()
    submitBtn.destroy()
    outputTxt.destroy()
    
    #destroy caesar widgets only if caesar power up was bought
    if(usedCaesar==1):
        caesarText.destroy()
        caesarInput.destroy()
        shiftText.destroy()
        shiftInput.destroy()
        caesarButton.destroy()
    
    #print game over message
    gameOverMessage = tk.Label(root, textvariable=gameover, bg="light blue")
    gameOverMessage.place(relx=0.5, rely=0.3,anchor=CENTER)
    scoreMessage = tk.Label(root, textvariable=scrmsg, bg="light blue")
    scoreMessage.place(relx=0.5, rely=0.5,anchor=CENTER)

    opscr = 0
    #set a score for the player and the opponent
    if(int(player_score)==int(scores[0])):
        scrmsg.set("Your score: "+str(player_score) +"\nOpponent's score: "+str(scores[1]))
        opscr=scores[1]
    else:
        scrmsg.set("Your score: "+str(player_score) +"\nOpponent's score: "+str(scores[0]))
        opscr=scores[0]

    #determine who won the game

    if(int(player_score)>int(opscr)):
        gameover.set("GameOver! You Win!")
    elif(int(player_score)<int(opscr)):
        gameover.set("GameOver! You Lose :(")
    else:
        gameover.set("GameOver! It's a Tie!")      
      

def get_name(event=None):
   
    global name 
    global address
    global port
    # gets the name entered from the first screen
    name = name_var.get()
    # gets the address from the first screen
    address = address_var.get()
    # gets the port from the first screen
    port = int(port_var.get())
    # Initiates the next screen
    game()

def instruction_page():
    global address
    global port
    global SOCKET_CONNECTION
    global test_string
    global player_score
    player_score = 0
    global text_string
    global text_dict
    global instr
    global clock1
    
    global t

    t.destroy()
    instr.destroy()
    clock1.destroy()

    # Establish connection with host server
    address_with_port = address, port
    SOCKET_CONNECTION = socket.socket()
    SOCKET_CONNECTION.connect(address_with_port)
    # Send the recorded text from client to server
    SOCKET_CONNECTION.sendall(bytes(text_input, 'utf-8'))

    # recieve the other players text
    test_string = SOCKET_CONNECTION.recv(1024).decode()
    #seperate words into dict for easy checking of guesses
    gen_text_dict(test_string)

    #global bc we need to destroy them in another function
    global greeting, instruc, beginButton
    #print instructions
    greeting = tk.Label(root, text="Hi "+name+"!", bg="light blue")
    greeting.grid(row=0)
    greeting.place(relx=0.5, rely=0.10, anchor=CENTER)
    instruc = tk.Label(root, text="Instructions:\n\nOn the next screen, you will see text printing with multiple errors throughout. Your goal is to decipher what the text is supposed to say, and enter it word by word.\n\nThere will be a text entry box where you will enter the indicated word. When you hit submit, you will be told whether your guess was correct or not, and your score will be adjusted accordingly. You also have the option to skip a word and move on to the next.\n\nWhen enough points have been acquired, you may purchase power-up by clicking the buttons at the top right of the screen. The power-ups will give you an advantage by decreasing the amount of bugs you encounter, attacking your opponent, or assisting you against their attacks. \n\n\nGood Luck!", bg="light blue", wraplength=420)
    instruc.grid(row=1)
    instruc.place(relx=0.5, rely=0.50,anchor=CENTER)
    # pressing begin initiates the next screen
    beginButton = tk.Button(root, command=set_up_gui, text="start the game")
    beginButton.grid(row=3)
    beginButton.place(relx=0.5, rely=0.92,anchor=CENTER)
    root.bind('<Return>',set_up_gui)


def set_up_gui(event=None):
    global outputTxt
    global delta
    global test_string
    player_score = None
    global yourScore, opsScore, clock, pwr1, pwr2, pwr3, pwr4, pwr5, pwr6, textToType, wordCount, guessBox, textEntry, canvas, submitBtn, outputTxt 

    #get rid of instruction widgets
    greeting.destroy()
    instruc.destroy()
    beginButton.destroy()
    scr.set("P1's Score: 0")
    o_scr.set("P2's Score: 0")
    #sets up the game layout
    wordNumText.set("Word #1")

    # Sets the keylogger with mode random
    k = Keylogger("random")

    # score widgets
    yourScore = tk.Label(root, textvariable=scr)
    yourScore.grid(row=0, column=0, sticky=W)
    opsScore = tk.Label(root, textvariable=o_scr)
    opsScore.grid(row=0, column=1, sticky=W)

    tk.Label(root, text="", bg="light blue").grid(row=1)
    # Skip button widget
    pwr1 = tk.Button(root, command= skip, text="skip", height=2, width=7)
    pwr1.place(relx=0.5, rely=0.015)
    # powerup buttons
    pwr2 = tk.Button(root, command= lambda: choose_pwr_2(k), text="Perfect\n Output ", height=2, width=7)
    pwr2.place(relx=0.65, rely=0.015)
    pwr3 = tk.Button(root, command= lambda: choose_pwr_3(k), text="Less\n  Random  ", height=2, width=7)
    pwr3.place(relx=0.8, rely=0.015)

    pwr4 = tk.Button(root, command= lambda: choose_pwr_4(k), text="Caesar\nDecryptor", height=2, width=7)
    pwr4.place(relx=0.5, rely=0.115)

    pwr5 = tk.Button(root, command= lambda: show_hint(k), text="Shift\n Hint ", height=2, width=7)
    pwr5.place(relx=0.65, rely=0.115)

    pwr6 = tk.Button(root, command= lambda: send_attack(k), text="Caesar\n Attack ", height=2, width=7)
    pwr6.place(relx=0.8, rely=0.115)

    # Text Widgets
    textToType = tk.Label(root, text="Text to Type:", bg="light blue")
    textToType.grid(row=2, sticky=W)
    wordCount = tk.Label(root, textvariable=wordNumText, bg="light blue")
    wordCount.grid(row=4, column=0, sticky=W)
    guessBox = tk.Label(root, text="Your guess:", bg="light blue") 
    guessBox.grid(row=4, column=1, sticky=W)

    
    
    #print out text by char
    canvas.grid(row=3, column=0, columnspan = 5, sticky = tk.W+tk.E)


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
    # Widget for word guess entry
    textEntry = tk.Entry(root, textvariable=text_var)
    textEntry.grid(row=4, column=2, columnspan=2, sticky=W)
    # Widget for submit button
    submitBtn = tk.Button(root, command= lambda: word_entered(k), text="submit")
    submitBtn.grid(row=4, column=4)

    root.bind('<Return>',lambda event: word_entered(k))
    # Index will be changed in word_entered when guess is correct
    output.set("Enter the word at position "+str(wordNum)+"!")
    clock = tk.Label(root, textvariable=clock_time)
    clock.grid(row=8, column=0)

    
    # timer is based on length of text
    countdown(math.ceil(len(test_string)*400/1000))

    # Output text widget displays messages to the player
    outputTxt = tk.Label(root, textvariable=output, bg="light blue")
    outputTxt.grid(row=8, column=1, columnspan=4)
    root.grid_rowconfigure(1, minsize=70) 
    root.grid_rowconfigure(3, minsize=20)  
    root.grid_rowconfigure(5, minsize=30)  
    root.grid_rowconfigure(7, minsize=20)

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

#keylogging
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

    # label for user input box
    instr = tk.Label(root, text="Type here:")
    instr.grid(row=0, column=1, sticky=W)
    t = Text(root, height=20, width=90)
    t.grid(row=1, column=1)
    # timer widget
    clock1 = tk.Label(root, textvariable=clock_time2)
    clock1.grid(row=0, column=1, columnspan=2)
    countdown2(45)
    # calls onKeyPress when key is pressed
    root.bind('<KeyPress>', onKeyPress)

def print_text(k, test_string, s):
    global start
    global caesar_count
    end = time.time()
    if start is not None:
        elapsed = end - start
        if elapsed >= 5:
            reset(k)
            start = None
    if len(test_string) > 0:
        c = test_string[0]
        # Obscure character based on rules in keylogger
        k.caesar = caesar_count
        new_c = k.simulated_key_pressed(c)
        caesar_count = k.caesar 
        s += new_c
        canvas.itemconfigure(canvas_text, text=s)
        canvas.after(400, print_text, k, test_string[1:], s)  

def caesar_decrypt(event=None):
    return_string = ""
    # gets the cipher text
    cipher_text = caesar_input.get()
    # gets the shift size
    shift_size = int(caesar_shift.get())
    # Decryption
    for i in range(len(cipher_text)):
        a = ord(cipher_text[i])
        if a > 96:
            return_string += chr((ord(cipher_text[i]) + (-1 * shift_size) - 65) % 26 + 65)
        else:
            return_string += chr((ord(cipher_text[i]) + (-1 * shift_size) - 97) % 26 + 97)
        # if((a - shift_size) < 33):
        #     return_string += chr((a - shift_size) + 94)
        # else:
        #     return_string += chr(a - shift_size)

    # Print the decrypted string to the output widget        
    output.set(return_string)

def word_entered(k):
    #gets the word the user guessed
    input = text_var.get()
    #print(input)
    text_var.set("")
    process_user_input(k, input)

# make this send data over connection???
def process_user_input(k, user_input):
    #checks if guess is right
    global wordNum
    global text_dict
    global caesar_count
    global outputTxt
    # get guess form user_inpot field
    word_guess = user_input
    # front end indexing starts at 1 but of course it starts at 0 in the code
    index = wordNum -1
    # If guess is correct
    if word_guess == text_dict[index]:
        # Add this index to list of words gessed correctly
        guessed_indices.append(index)
        output.set("Correct!")
        outputTxt.config(fg="green3")
        caesar_count += mod_score(len(word_guess))
        # change index
        mod_word_num()

        return len(word_guess)
    
    # Incorrect guesses do not need to communicate with server
    else:
        output.set("Incorrect :(")
        return 0

def show_hint(k):
    global caesar_count
    global player_score
    if int(player_score) < 200:
        output.set("You don't have enough points! Need 200!")
    else:
        key = next(iter(k.shifted))
        output.set("Word at index " + str(key) + " is shifted by " + str(k.shifted[key]))
        k.shifted.pop(key)
        caesar_count += mod_score(-2)
def send_attack(k):
    global caesar_count
    global player_score
    if int(player_score) < 800:
        output.set("You don't have enough points! Need 800!")
    else:
        caesar_count += mod_score("-800 cca")

def mod_score(score_modifier):
    #modifies score if guess is right
    global p1score
    global score
    global player_score
    #send length of word guess to server to modify score
    SOCKET_CONNECTION.sendall(bytes(str(score_modifier), 'utf-8'))
    # recieve scores from server so we can update the ui
    # Splits on space and creates a list of scores
    # Note that this means the player will not see themself listed as player1 in the ui, the first player to connect is p1 and second is p2
    scores = SOCKET_CONNECTION.recv(1024).decode().split()
    for score in scores:
            if score is None:
                score = "0"
        
    # Set scoreboard 
    scr.set("P1's score: " + str(scores[0]))
    o_scr.set("P2's score: " + str(scores[1]))
    player_number = scores[2]
    player_score = scores[int(player_number) - 1]
    if len(scores) > 3:
        return 3
    else:
        return 0
    

# Change indexing
def mod_word_num():
    global wordNum
    wordNum +=1
    # Print new index to screen
    wordNumText.set("Word #"+str(wordNum))

# Checks if there is currently a powerup enabled
def check_powerup(k):
    b = False
    if k.get_mode() == "none" or k.get_rand() == 20:
        b = True
    return b

# Reset mode after powerup time
def reset(k):
    k.change_mode("random")
    k.change_rand(10)

# Skip button increases index
def skip():
    global player_score
    global caesar_count
    #outputTxt.config(fg="black")
    
    if int(player_score) < 100:

        output.set("You don't have enough points! Need 100!")
    else:
        # Increase index by one
        mod_word_num()
        output.set("Skipped!")
        caesar_count += mod_score(-1)
        return

# Powerup for perfect text printing with no errors
def choose_pwr_2(k):
    global score
    global start
    global caesar_count
    global player_score
    #outputTxt.config(fg="black")
    if(check_powerup(k)):
        output.set("You can't use more than 1 power up at a time!")
    # Powerup cost 600
    elif int(player_score) < 600:

        output.set("You don't have enough points! Need 600!")
    # If you don't already have a powerup and you have enough points
    else:
        output.set("Changing mode to NONE for 5 seconds")
        k.change_mode("none")
        start = time.time()
        caesar_count += mod_score(-6)
    return

# Powerup for Reduced randomization
def choose_pwr_3(k):
    global score
    global start
    global caesar_count
    global player_score
    #outputTxt.config(fg="black")
    if(check_powerup(k)):
        output.set("You can't use more than 1 power up at a time!")
    # Powerup cost 300
    elif int(player_score) < 400:
        output.set("You don't have enough points! Need 400!")
    # If you don't already have a powerup and you have enough points
    else:
        output.set("Decreasing probabilty of flipped characters to 1/20 for 5 seconds")
        k.change_rand(20)
        start = time.time()
        caesar_count += mod_score(-4)
    return

# Powerup for Caesar cipher decryption
def choose_pwr_4(k):
    global score
    global start
    global caesar_count
    global usedCaesar
    global player_score
    global caesarText, caesarInput, shiftText, shiftInput, caesarButton
    #outputTxt.config(fg="black")
    if int(player_score) < 1000:
         output.set("You don't have enough points! Need 1000!")
    else:
        usedCaesar+=1
        print("bought cipher "+str(usedCaesar))
        output.set("Caesar cipher decryptor purchased")
        # TODO: MAKE WORTH MORE POINTS
        caesar_count += mod_score(-10)
        # New text field widgets
        caesarText = tk.Label(root, text="cipher-text:")
        caesarText.grid(row=6, column=0)
        caesarInput = tk.Entry(root, textvariable=caesar_input)
        caesarInput.grid(row=6, column=1, sticky=W)
        shiftText = tk.Label(root, text="shift size:")
        shiftText.grid(row=6, column=2)
        shiftInput = tk.Entry(root, textvariable=caesar_shift)
        shiftInput.grid(row=6, column=3, sticky=W)
        # Submission button for caesar cipher
        caesarButton = tk.Button(root, command=caesar_decrypt, text="submit")
        caesarButton.grid(row=6, column=4)
        start = time.time()
        #mod_score(0)
    return

# opens text document and creates dict
def gen_text_dict(text_str):
    global text_dict
    # code for set text with no keylogging
    #f = open("sampletext.txt", "r")
    #text = f.read()
    
    # gets rid of punctuation as we don't want the player to have to enter anything other than letters
    text_no_punct = text_str.translate(str.maketrans('', '', string.punctuation))
    text_dict = text_no_punct.split(" ")

#set up GUI
root = tk.Tk()
root.title("typing game")
root.configure(bg="light blue")

#GUI stringVars
gameover = StringVar()
scrmsg = StringVar()
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
caesar_input = StringVar()
caesar_shift = StringVar()

# window size declaration
canvas = tk.Canvas(root, width=650, height=200)
canvas_text = canvas.create_text(10, 10, anchor=tk.NW, width=640)


#username entry widgets
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
