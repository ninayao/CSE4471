import time
import tkinter as tk

root = tk.Tk()
tk.Label(root, text="Text to Type:", bg="light blue").grid(row=0)
tk.Label(root, text="Your text:", bg="light blue").grid(row=2)

tk.Label(root, text="The brown fox jumped over the lazy dog", bg="yellow").grid(row=0, column=1)

root.geometry("420x300")
root.title("typing game")
root.configure(bg="light blue")

textEntry = tk.Text(root, height=3, width=40).grid(row=2, column=1)
submitBtn = tk.Button(root, text="submit").grid(row=10, column=1)


root.mainloop()
