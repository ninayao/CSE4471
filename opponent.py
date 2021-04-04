import sys
import time
import string
import os
import tkinter as tk
from tkinter import *
from keylogger import Keylogger

text_input = ""

def countdown(count):
    global k
    # change text in label        
    clock_time.set(str(count))

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else :
        print(text_input)

def onKeyPress(event):
    global text_input
    text_input += event.char

root = tk.Tk()
root.title("typing game")
root.configure(bg="light blue")
root.geometry("700x500")
instr = tk.Label(root, text="Type here:").grid(row=0, column=1, sticky=W)
t = Text(root, height=20, width=90)
t.grid(row=1, column=1)
clock_time = StringVar()
clock = tk.Label(root, textvariable=clock_time)
clock.grid(row=0, column=1, columnspan=2)
countdown(20)
root.bind('<KeyPress>', onKeyPress)

root.mainloop()