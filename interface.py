from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import ctypes   


# Characters : ⟵⎯⟶
window=Tk()
window.geometry("1200x600")
window.title("Visualisateur de trames")
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)
window.rowconfigure(1,weight=1)

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

filemenu = Menu(menubar, tearoff=0,font=("Helvetica", 12))
filemenu.add_command(label="Open", command=lambda: open_file())
filemenu.add_command(label="Save as", command=lambda: save_file())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)




helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: about())
menubar.add_cascade(label="Help", menu=helpmenu)


#create a frame to display the listbox and the scrollbar
frame=Frame(window)
frame.grid(row=0,column=0,sticky="nsew")
frame.rowconfigure(0,weight=1)
frame.columnconfigure(0,weight=1)

# create a listbox to display the frames
listbox = Listbox(frame, width=100, height=20,borderwidth=0,highlightthickness=0,font=("Helvetica", 18))
listbox.grid(row=0, column=0,padx=5,pady=5,sticky="nsew")

# create a scrollbar to scroll the listbox
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.grid(row=0, column=1,padx=0,pady=0,sticky="ns")
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

#create a horizontal scrollbar to scroll the listbox
scrollbar2 = Scrollbar(frame, orient="horizontal")
scrollbar2.grid(row=1, column=0,padx=0,pady=0,sticky="ew")
scrollbar2.config(command=listbox.xview)
listbox.config(xscrollcommand=scrollbar2.set)


frame2=Frame(window,width=100,height=70,borderwidth=0,highlightthickness=0,relief=SUNKEN)
frame2.grid(row=1,column=0,sticky="nsew")
frame2.rowconfigure(0,weight=1)
frame2.columnconfigure(0,weight=1)
frame2.pack_propagate(0)

# create an element into the listbox
# element label in the center
listbox.insert(END, "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⟶")

listbox.itemconfig(0,{'bg':'#e63030'})

ctypes.windll.shcore.SetProcessDpiAwareness(1)
photo=PhotoImage(file="icon.png")
window.iconphoto(False, photo)
window.mainloop()