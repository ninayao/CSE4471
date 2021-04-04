import sys
import time
import string
import os
import tkinter as tk
from tkinter import *
from keylogger import Keylogger
import socket

text_input = ""
name = ""
address = ""
port = 0
sock = None
connections = []

def countdown(count):
    global text_input
    global connections
    # change text in label        
    clock_time.set(str(count))

    if count > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, count-1)
    else :
        print(text_input)
        file = open("test.txt", "w")
        file.write(text_input)
        for client in connections:
            client.sendall(bytes(text_input, 'utf-8'))

def onKeyPress(event):
    global text_input
    text_input += event.char

def game():
    global name 
    global address
    global port
    global sock
    global connections

    sock = socket.socket()
    sock.bind(('', port))
    print("Socket bound to ", port)
    sock.listen(5)

    while len(connections) < 1:
        c, addr = sock.accept()   
        connections.append(c)
        print("Got connection from " + str(addr))

    instr = tk.Label(root, text="Type here:").grid(row=0, column=1, sticky=W)
    t = Text(root, height=20, width=90)
    t.grid(row=1, column=1)
    clock = tk.Label(root, textvariable=clock_time)
    clock.grid(row=0, column=1, columnspan=2)
    countdown(20)
    root.bind('<KeyPress>', onKeyPress)

def get_name(event=None):
    #gets the name entered from the first screen
    global name 
    global address
    global port
    name = name_var.get()
    address = address_var.get()
    port = int(port_var.get())
    game()


root = tk.Tk()
root.title("typing game")
root.configure(bg="light blue")
root.geometry("700x500")

clock_time = StringVar()
address_var =StringVar()
port_var =StringVar()
name_var =StringVar()

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

root.mainloop()