from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import ctypes   
import random
import input
import extract




# function retuns random color in hex format except black and white and colors too close to black and white
def random_color():
    red=random.randint(0,255)
    blue=random.randint(0,255)
    green=random.randint(0,255)
    # check if color is too close to black
    while (red<100 and blue<100 and green<100) or(red>200 and blue>200 and green>200):
        red=random.randint(0,255)
        blue=random.randint(0,255)
        green=random.randint(0,255)
    return '#%02X%02X%02X' % (red,blue,green)


class App:

    # liste des variables d'instances
    # self.window = Fenêtre principale
    # self.first = Booléen indiquant si c'est la première fois que l'on ouvre un fichier
    # self.welcometext = Texte de bienvenue
    # self.openbutton = Bouton d'ouverture de fichier à l'ouverture de l'application
    # self.i = Nombre de trames affichées
    # self.frames = Liste des trames
    # self.listboxframe= Groupe contenant la listbox et la scrollbar
    # self.listbox1 = Listbox contenant les trames
    # self.scrollbar = Scrollbar de la listbox
    # self.frame2 = Groupe contenant les boutons
    # self.filtervalue = Chaine de caractères contenant la valeur du filtre
    # self.itemlist= Liste des items de la listbox
    # self.ip_couples = Liste des couples ip source et ip destination

    
    def __init__(self):
        self.window=Tk()
        self.window.geometry("1200x600")
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.window.title("Visualisateur de trames")
        self.window.resizable(False, False)
        self.first=True
        self.openbutton=ttk.Button(self.window, text="Ouvrir un fichier", command=self.openFile)
        self.welcometext=Label(self.window, text="Bienvenue dans le visualisateur de trames !")
        self.welcometext.pack()
        self.openbutton.config(width=20,padding=10,style="TButton")
        #put the text on top of the button
        self.welcometext.pack(side="top")
        self.welcometext.place(relx=0.5, rely=0.2, anchor=CENTER)
        #put the button at the center of the window
        self.openbutton.pack(side=TOP)
        self.openbutton.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.i=0


    def openFile(self):
        file = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        self.frames=input.input(file)
        if (self.first):
            self.createParts()
        
        self.__showFrames(self.frames)
        self.first=False
        print(self.frames)
        
    
    def createParts(self):
        # create a menu that display frames in a listbox and a scrollbar
        self.openbutton.destroy()
        self.welcometext.destroy()
        #create a frame to display the listbox and the scrollbar
        self.listboxframe=Frame(self.window,width=1200,height=500)
        self.listboxframe.pack(side=TOP)
        # create a listbox to display the frames
        self.listbox1 = Listbox(self.listboxframe, width=90, height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16))
        self.listbox1.pack(side=LEFT)
        # create a scrollbar to scroll the listbox
        scrollbar = Scrollbar(self.listboxframe, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.listbox1.yview)
        self.listbox1.config(yscrollcommand=scrollbar.set)


        self.frame2=Frame(self.window,width=600,height=150)
        self.frame2.pack(side=RIGHT)
        button2=ttk.Button(self.frame2,text="Save file",command=lambda: self.export(),width=20,padding=10,style="TButton")
        button2.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
        button3=ttk.Button(self.frame2,text="Ouvrir un fichier",command=lambda: self.openFile(),width=20,padding=10,style="TButton")
        button3.grid(row=1,column=1,padx=10,pady=10,sticky="nsew")
        
        self.filtervalue=StringVar()
        filterentry=Entry(self.frame2,width=18,textvariable=self.filtervalue,font=("Helvetica", 12))
        filterentry.config()
        filtertext=Label(self.frame2,text="Filtrer",font=("Helvetica", 12))
        filtertext.grid(row=0,column=2,padx=10,pady=0,sticky="nsew")
        filterentry.grid(row=1,column=2,padx=10,pady=15,sticky="nsew")
        filterentry.bind("<Return>",self.filter_search)


    def __showFrames(self,frames):
        # create an element to display the frame's content


        self.resetlistbox()
        for frame in frames:
            res,color=self.analyse(frame)
            self.itemlist.append((res,color))
            self.listbox1.insert(END, res)
            self.listbox1.itemconfig(0,{'bg':color})
            self.i=self.i+1
    
    def resetlistbox(self):
        self.listbox1.delete(0,END)
        self.ip_couples=[]
        self.itemlist=[]
        self.i=0


    def export():
        pass


    def find_couple(self,ip1,ip2):
        for couple in self.ip_couples:
            if (couple[0]==ip1 and couple[1]==ip2):
                return ("⎯⎯⎯⎯⎯⟶",couple[2])
            if (couple[0]==ip2 and couple[1]==ip1):
                return ("⟵⎯⎯⎯⎯⎯",couple[2])
        return None

    def analyse(self,frame):
        ethernet_header=extract.extract_ethernet_header(frame)

        if (not extract.check_if_ip(frame)):
            return (ethernet_header[1]+"⎯⎯⎯⎯⎯⟶"+ethernet_header[0]+"Not an IP frame")
        ip_header=extract.extract_ip_header(frame)
        if (int(ip_header[1],16)*4<20):
            return (ethernet_header[1]+"⎯⎯⎯⎯⎯⟶"+ethernet_header[0]+"IP header too short")
        # find the couple of ip addresses in the list of couples
        couple=self.find_couple(ip_header[7],ip_header[8])
        
        # if the couple is not in the list of couples, add it
        if (couple==None):
            color=random_color()
            self.ip_couples.append((ip_header[7],ip_header[8],color))
            arrow="⎯⎯⎯⎯⎯⟶"
        else:
            color=couple[1]
            arrow=couple[0]

        infos=""
        if (ip_header[4]=="001"):
            infos=infos+"Fragmented"
        
        if (not extract.check_if_tcp(frame)):
            return (extract.str_to_ip(ip_header[7])+arrow+extract.str_to_ip(ip_header[8])+"   Not a TCP frame"+infos,color)
        tcp_header=extract.extract_tcp(frame)
        if (int(tcp_header[4],16)*4<20):
            return (extract.str_to_ip(ip_header[7])+arrow+extract.str_to_ip(ip_header[8])+"   TCP header too short",color)
        if (not tcp_header[0]!='50' or tcp_header[1]!='50'):
            return (extract.str_to_ip(ip_header[7])+":"+str(int(tcp_header[0],16))+arrow+extract.str_to_ip(ip_header[8])+":"+str(int(tcp_header[1],16))+"   Not an HTTP frame",color)
        


        return ("correct",color)

    def filter_search(self,event):
      
        sstr = self.filtervalue.get()
        self.listbox1.delete(0,END)
        # If filter removed show all data
        if sstr == "":
            for item in self.itemlist:
                self.listbox1.insert(END, item[0])
                self.listbox1.itemconfig(0,{'bg':item[1]}) 
            return
    
        filtered_data = list()
        for item in self.itemlist:
            if item[0].find(sstr) >= 0:
                filtered_data.append(item)
    
        for item in filtered_data:
            self.listbox1.insert(END, item[0])
            self.listbox1.itemconfig(0,{'bg':item[1]})  

    def show(self):
        self.window.mainloop()




if __name__ == "__main__":
    newwindow=App()
    newwindow.show()




# # # Characters : ⟵⎯⟶
# window=Tk()
# window.geometry("1200x600")
# window.title("Visualisateur de trames")
# window.columnconfigure(0,weight=1)
# window.rowconfigure(0,weight=1)
# window.rowconfigure(1,weight=1)

# # create a menu that display frames in a listbox and a scrollbar
# menubar = Menu(window)
# window.config(menu=menubar)


# def open_file():
#     file = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
#     return file


# def save_file():
#     file = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
#     return file    

# def about():
#     messagebox.showinfo("About", "This is a simple tool to visualize network frames")

# filemenu = Menu(menubar, tearoff=0,font=("Helvetica", 12))
# filemenu.add_command(label="Open", command=lambda: open_file())
# filemenu.add_command(label="Save as", command=lambda: save_file())
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=window.quit)
# menubar.add_cascade(label="File", menu=filemenu)




# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="About", command=lambda: about())
# menubar.add_cascade(label="Help", menu=helpmenu)


# #create a frame to display the listbox and the scrollbar
# frame=Frame(window,width=1200,height=500)
# frame.pack(side=TOP)
# # frame.place(relx=0.5, rely=0.3, anchor="s")
# frame.config(bg="blue")

# # create a listbox to display the frames
# listbox = Listbox(frame, width=90, height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 18))
# listbox.pack(side=LEFT)
# # create a scrollbar to scroll the listbox
# scrollbar = Scrollbar(frame, orient="vertical")
# scrollbar.pack(side=RIGHT, fill=Y)
# scrollbar.config(command=listbox.yview)
# listbox.config(yscrollcommand=scrollbar.set)

# #create a horizontal scrollbar to scroll the listbox
# scrollbar2 = Scrollbar(frame, orient="horizontal")

# scrollbar2.config(command=listbox.xview)
# listbox.config(xscrollcommand=scrollbar2.set)

# frame2=Frame(window,width=600,height=150)
# frame2.pack(side=RIGHT)
# frame2.config(bg="red")
# button2=ttk.Button(frame2,text="Save file",command=lambda: save_file(),width=20,padding=10,style="TButton")
# button2.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
# button3=ttk.Button(frame2,text="Open file",command=lambda: open_file(),width=20,padding=10,style="TButton")
# button3.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")


# # create an element into the listbox
# # element label in the center




# ctypes.windll.shcore.SetProcessDpiAwareness(1)
# photo=PhotoImage(file="icon.png")
# window.iconphoto(False, photo)


# # function retuns random color in hex format except black and white and colors too close to black and white
# def random_color():
#     red=random.randint(0,255)
#     blue=random.randint(0,255)
#     green=random.randint(0,255)
#     # check if color is too close to black
#     while (red<100 and blue<100 and green<100) or(red>200 and blue>200 and green>200):
#         red=random.randint(0,255)
#         blue=random.randint(0,255)
#         green=random.randint(0,255)
#     return '#%02X%02X%02X' % (red,blue,green)

# listbox.insert(END, "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⟶")
# listbox.itemconfig(0,{'bg':random_color()})

# window.mainloop()