from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import ctypes   

window=Tk()
window.geometry("720x440")
window.title("Visualisateur de trames")


# create a menu that display frames in a listbox and a scrollbar
menubar = Menu(window)
window.config(menu=menubar)


def open_file():
    file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    return file


def save_file():
    file = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    return file    

def about():
    messagebox.showinfo("About", "This is a simple tool to visualize network frames")

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=lambda: open_file())
filemenu.add_command(label="Save as", command=lambda: save_file())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)




helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: about())
menubar.add_cascade(label="Help", menu=helpmenu)




ctypes.windll.shcore.SetProcessDpiAwareness(1)
photo=PhotoImage(file="icon.png")
window.iconphoto(False, photo)
window.mainloop()