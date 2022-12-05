from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import ctypes   
import random
import input
import extract
import re
import platform




# function retuns random color in hex format except black and white and colors too close to black and white
def random_color():
    red=random.randint(0,255)
    blue=random.randint(0,255)
    green=random.randint(0,255)
    # check if color is too close to black
    while (red<150 and blue<150 and green<150) or(red>200 and blue>200 and green>200):
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
    # self.i = Nombre de trames ouvertes
    # self.frames = Liste des trames
    # self.listboxframe= Groupe contenant la listbox et la scrollbar
    # self.listbox1 = Listbox contenant les trames
    # self.scrollbar = Scrollbar de la listbox
    # self.frame2 = Groupe contenant les boutons
    # self.filtervalue = Chaine de caractères contenant la valeur du filtre
    # self.itemlist= Liste des items de la listbox
    # self.ip_couples = Liste des couples ip source et ip destination
    # self.identificationlist = Liste des identifications ip pour les trames fragmentées
    # self.errorlabel = Texte d'erreur d'ouverture de fichier
    # self.filterentry = Entry du filtre

    # Constructor
    def __init__(self):
        
        self.window=Tk()
        self.window.geometry("1200x600")
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.window.title("Visualisateur de trames")
        self.window.resizable(False, False)
        self.first=True
        self.errorlabel=ttk.Label(self.window,text="")
        self.errorlabel.pack()
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

    # function that open a file and display the frames
    def openFile(self):
        file = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        try:
            self.frames=input.input(file) # can raise an Exception
        except Exception as inst:
            self.errorlabel.config(text="Erreur lors de l'ouverture du fichier : "+str(inst),foreground="red")
            raise inst
        if (self.first):
            self.createParts()
        
        self.__showFrames(self.frames)
        self.first=False
        print(self.frames)
        
    
    # function that create the parts of the interface
    def createParts(self):
        # create a menu that display frames in a listbox and a scrollbar
        self.openbutton.destroy()
        self.welcometext.destroy()
        self.errorlabel.destroy()
        #create a frame to display the listbox and the scrollbar
        self.listboxframe=Frame(self.window,width=1200,height=500)
        self.listboxframe.pack(side=TOP)
        # create listboxes to display the frames
        # listbox1 = source
        self.listbox1 = Listbox(self.listboxframe, width=14, height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox1.pack(side=LEFT,pady=30)
        # listbox2 = source port
        self.listbox2=Listbox(self.listboxframe,width=7,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox2.pack(side=LEFT,pady=30)
        # listbox3 = arrow
        self.listbox3=Listbox(self.listboxframe,width=7,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox3.pack(side=LEFT,pady=30)
        # listbox4 = destination
        self.listbox4=Listbox(self.listboxframe,width=14,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox4.pack(side=LEFT,pady=30)
        # listbox5 = destination port
        self.listbox5=Listbox(self.listboxframe,width=7,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox5.pack(side=LEFT,pady=30)
        # listbox6 = protocol
        self.listbox6=Listbox(self.listboxframe,width=8,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox6.pack(side=LEFT,pady=30)
        # listbox7 = Description
        self.listbox7=Listbox(self.listboxframe,width=17,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 16),exportselection=0)
        self.listbox7.pack(side=LEFT,pady=30)
        # create a scrollbar to scroll all listboxes
        scrollbar = Scrollbar(self.listboxframe, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y,pady=30)
        scrollbar.config(command=self.__multiple_yview)
        self.listbox1.config(yscrollcommand=scrollbar.set)
        self.listbox2.config(yscrollcommand=scrollbar.set)
        self.listbox3.config(yscrollcommand=scrollbar.set)
        self.listbox4.config(yscrollcommand=scrollbar.set)
        self.listbox5.config(yscrollcommand=scrollbar.set)
        self.listbox6.config(yscrollcommand=scrollbar.set)
        self.listbox7.config(yscrollcommand=scrollbar.set)

        self.listbox1.bind("<<ListboxSelect>>", self.on_select1)
        self.listbox2.bind("<<ListboxSelect>>", self.on_select2)
        self.listbox3.bind("<<ListboxSelect>>", self.on_select3)
        self.listbox4.bind("<<ListboxSelect>>", self.on_select4)
        self.listbox5.bind("<<ListboxSelect>>", self.on_select5)
        self.listbox6.bind("<<ListboxSelect>>", self.on_select6)
        self.listbox7.bind("<<ListboxSelect>>", self.on_select7)

        self.listbox1.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox2.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox3.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox4.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox5.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox6.bind("<MouseWheel>", self.on_mousewheel)
        self.listbox7.bind("<MouseWheel>", self.on_mousewheel)

        self.frame2=Frame(self.window,width=600,height=300)
        self.frame2.pack(side=BOTTOM,fill=X,expand=1)
        button2=ttk.Button(self.frame2,text="Exporter",command=lambda: self.export(),width=20,padding=10,style="TButton")
        button2.grid(row=1,column=5,padx=10,pady=10,sticky="nsew")
        button3=ttk.Button(self.frame2,text="Ouvrir un fichier",command=lambda: self.openFile(),width=20,padding=10,style="TButton")
        button3.grid(row=1,column=4,padx=10,pady=10,sticky="nsew")
        
        self.filtervalue=StringVar()
        self.filterentry=Entry(self.frame2,width=18,textvariable=self.filtervalue,font=("Helvetica", 12))
        self.filterentry.config()
        filtertext=Label(self.frame2,text="Filtrer",font=("Helvetica", 12))
        filtertext.grid(row=0,column=0,padx=10,pady=0,sticky="nsew")
        self.filterentry.grid(row=1,column=0,padx=10,pady=15,sticky="nsew")
        self.frame2.columnconfigure(1,weight=1)
        self.frame2.columnconfigure(2,weight=1)
        self.frame2.columnconfigure(3,weight=1)
        self.filterentry.bind("<Return>",self.filter_search)

    def __multiple_yview(self,*args):
        self.listbox1.yview(*args)
        self.listbox2.yview(*args)
        self.listbox3.yview(*args)
        self.listbox4.yview(*args)
        self.listbox5.yview(*args)
        self.listbox6.yview(*args)
        self.listbox7.yview(*args)

    # function that display the frames in the listbox
    def __showFrames(self,frames):

        self.resetlistbox()
        for frame in frames:
            source,sourceport,arrow,dest,destport,protocol,desc,color=self.analyse(frame)
            print(color)
            self.itemlist.append((source,sourceport,arrow,dest,destport,protocol,desc,color))

            self.listbox1.insert(END, source)
            self.listbox2.insert(END, sourceport)
            self.listbox3.insert(END, arrow)
            self.listbox4.insert(END, dest)
            self.listbox5.insert(END, destport)
            self.listbox6.insert(END, protocol)
            self.listbox7.insert(END, desc)
            if (color=="#000000"):
                self.listbox1.itemconfig(self.i,fg="white",bg=color)
                self.listbox2.itemconfig(self.i,fg="white",bg=color)
                self.listbox3.itemconfig(self.i,fg="white",bg=color)
                self.listbox4.itemconfig(self.i,fg="white",bg=color)
                self.listbox5.itemconfig(self.i,fg="white",bg=color)
                self.listbox6.itemconfig(self.i,fg="white",bg=color)
                self.listbox7.itemconfig(self.i,fg="white",bg=color)
            else:
                self.listbox1.itemconfig(self.i,{'bg':color})
                self.listbox2.itemconfig(self.i,{'bg':color})
                self.listbox3.itemconfig(self.i,{'bg':color})
                self.listbox4.itemconfig(self.i,{'bg':color})
                self.listbox5.itemconfig(self.i,{'bg':color})
                self.listbox6.itemconfig(self.i,{'bg':color})
                self.listbox7.itemconfig(self.i,{'bg':color})
            self.i=self.i+1
    
    # reset the listbox and the itemlist
    def resetlistbox(self):
        self.listbox1.delete(0,END)
        self.listbox2.delete(0,END)
        self.listbox3.delete(0,END)
        self.listbox4.delete(0,END)
        self.listbox5.delete(0,END)
        self.listbox6.delete(0,END)
        self.listbox7.delete(0,END)
        self.ip_couples=[]
        self.itemlist=[]
        self.identificationlist={}
        self.i=0

    def on_select1(self,event):
        index=self.listbox1.curselection()[0]
        self.select_others(index,self.listbox2,self.listbox3,self.listbox4,self.listbox5,self.listbox6,self.listbox7)

    def on_select2(self,event):
        index=self.listbox2.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox3,self.listbox4,self.listbox5,self.listbox6,self.listbox7)
    
    def on_select3(self,event):
        index=self.listbox3.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox4,self.listbox5,self.listbox6,self.listbox7)
    
    def on_select4(self,event):
        index=self.listbox4.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox3,self.listbox5,self.listbox6,self.listbox7)

    def on_select5(self,event):
        index=self.listbox5.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox3,self.listbox4,self.listbox6,self.listbox7)
    
    def on_select6(self,event):
        index=self.listbox6.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox3,self.listbox4,self.listbox5,self.listbox7)
    
    def on_select7(self,event):
        index=self.listbox7.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox3,self.listbox4,self.listbox5,self.listbox6)
    
    def select_others(self,index,*others):
        for other in others:
            other.selection_clear(0,other.size()-1)
            other.selection_set(index)


    def on_mousewheel(self,event):
        if (platform.system()=="Windows"):
            value=int(event.delta/120)
        else:
            value=int(event.delta)
        self.listbox1.yview_scroll((-1)*event.delta,"units")
        self.listbox2.yview_scroll((-1)*event.delta,"units")
        self.listbox3.yview_scroll((-1)*event.delta,"units")
        self.listbox4.yview_scroll((-1)*event.delta,"units")
        self.listbox5.yview_scroll((-1)*event.delta,"units")
        self.listbox6.yview_scroll((-1)*event.delta,"units")
        self.listbox7.yview_scroll((-1)*event.delta,"units")
        return "break"
    # export the frames in a file
    def export():
        # reste a faire : exporter l'affichage de la listbox dans un fichier
        pass



    # return a list of couples ip source and ip destination by looking at the list of frames already displayed
    def find_couple(self,ip1,ip2):
        for couple in self.ip_couples:
            if (couple[0]==ip1 and couple[1]==ip2):
                return ("⎯⎯⎯⎯⎯⟶",couple[2])
            if (couple[0]==ip2 and couple[1]==ip1):
                return ("⟵⎯⎯⎯⎯⎯",couple[2])
        return None


    # analyse the frame and return a string containing the frame's content and a color
    def analyse(self,frame):
        ethernet_header=extract.extract_ethernet_header(frame)

        if (not extract.check_if_ip(frame)):
            return (ethernet_header[1],"","⎯⎯⎯⎯⎯⟶",ethernet_header[0],"","None","Not an IP frame","#000000")
        ip_header=extract.extract_ip_header(frame)
        if (int(ip_header[1],16)*4<20):
            return (ethernet_header[1],"","⎯⎯⎯⎯⎯⟶",ethernet_header[0],"","IP","IP header too short","#000000")
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

        # Check IP Fragmentation
        if (ip_header[4]=="001"):
            infos=infos+"Fragmented"
            if (ip_header[3] not in self.identificationlist):
                self.identificationlist[ip_header[3]]=0
                infos=infos+" Fragment 1"
            else:
                self.identificationlist[ip_header[3]]=self.identificationlist[ip_header[3]]+1
                infos=infos+" Fragment "+str(self.identificationlist[ip_header[3]])
        if (ip_header[4]=="010" and (ip_header[3] in self.identificationlist)):
            infos=infos+"Last fragment"
            del self.identificationlist[ip_header[3]]
        
        if (not extract.check_if_tcp(frame)):
            return (extract.str_to_ip(ip_header[7]),"",arrow,extract.str_to_ip(ip_header[8]),"","IP","Not a TCP frame"+infos,color)
        tcp_header=extract.extract_tcp(frame)
        if (tcp_header[4]<20):
            return (extract.str_to_ip(ip_header[7]),"",arrow,extract.str_to_ip(ip_header[8]),"","IP","TCP header too short",color)
        prot="TCP"
        if (not tcp_header[0]=='50' or tcp_header[1]=='50'): # if the port is not 80 (HTTP)
            http=extract.extract_http(frame)
            infos=infos+" "+http
            prot=prot+"/HTTP"
        else :
            tcp_flags=extract.extract_tcp_flags(frame)
            if (tcp_flags[0]=='1'):
                infos=infos+" [URG]"
            if (tcp_flags[1]=='1'):
                infos=infos+" [ACK]"
            if (tcp_flags[2]=='1'):
                infos=infos+" [PSH]"
            if (tcp_flags[3]=='1'):
                infos=infos+" [RST]"
            if (tcp_flags[4]=='1'):
                infos=infos+" [SYN]"
            if (tcp_flags[5]=='1'):
                infos=infos+" [FIN]"
        return (extract.str_to_ip(ip_header[7]),str(int(tcp_header[0],16)),arrow,extract.str_to_ip(ip_header[8]),str(int(tcp_header[1],16)),prot,infos,color)

    
    # filter the listbox with the filter entry
    def filter_search(self,event):
      
        sstr = self.filtervalue.get()
        match=re.search(r"^(.*)==(.*)$",sstr)
        if (sstr!="" and match==None):
            self.filterentry.config({"background":"#e8c0be"})
            return
        if (match!=None and match.group(1).lower()!="ip1" and match.group(1).lower()!="ip2" and match.group(1).lower()!="port1" and match.group(1).lower()!="port2" and match.group(1).lower()!="protocol" and match.group(1).lower()!="description"):
            self.filterentry.config({"background":"#e8c0be"})
            return
        self.listbox1.delete(0,END)
        self.listbox2.delete(0,END)
        self.listbox3.delete(0,END)
        self.listbox4.delete(0,END)
        self.listbox5.delete(0,END)
        self.listbox6.delete(0,END)
        self.listbox7.delete(0,END)
        # If filter removed show all data
        if sstr == "":
            self.filterentry.config({"background":"#ffffff"})
            for item in self.itemlist:
                self.listbox1.insert(END, item[0])
                self.listbox2.insert(END, item[1])
                self.listbox3.insert(END, item[2])
                self.listbox4.insert(END, item[3])
                self.listbox5.insert(END, item[4])
                self.listbox6.insert(END, item[5])
                self.listbox7.insert(END, item[6])
                self.listbox1.itemconfig(END,{'bg':item[7]}) 
                self.listbox2.itemconfig(END,{'bg':item[7]})
                self.listbox3.itemconfig(END,{'bg':item[7]})
                self.listbox4.itemconfig(END,{'bg':item[7]})
                self.listbox5.itemconfig(END,{'bg':item[7]})
                self.listbox6.itemconfig(END,{'bg':item[7]})
                self.listbox7.itemconfig(END,{'bg':item[7]})
            return
        self.filterentry.config({"background":"#b7e6b1"})
        filtered_data = list()
        for item in self.itemlist:

            match match.group(1):
                case "ip1":
                    if item[0].find(match.group(2)) >= 0:
                        filtered_data.append(item)
                case "port1":
                    if item[1].find(match.group(2)) >= 0:
                        filtered_data.append(item)
                case "ip2":
                    if item[3].find(match.group(2)) >= 0:
                        filtered_data.append(item)
                case "port2":
                    if item[4].find(match.group(2)) >= 0:
                        filtered_data.append(item)
                case "protocol":
                    if item[5].find(match.group(2)) >= 0:
                        filtered_data.append(item)
                case "description":
                    if item[6].find(match.group(2)) >= 0:
                        filtered_data.append(item)
    
        for item in filtered_data:
            self.listbox1.insert(END, item[0])
            self.listbox2.insert(END, item[1])
            self.listbox3.insert(END, item[2])
            self.listbox4.insert(END, item[3])
            self.listbox5.insert(END, item[4])
            self.listbox6.insert(END, item[5])
            self.listbox7.insert(END, item[6])
            self.listbox1.itemconfig(END,{'bg':item[7]})  
            self.listbox2.itemconfig(END,{'bg':item[7]})
            self.listbox3.itemconfig(END,{'bg':item[7]})
            self.listbox4.itemconfig(END,{'bg':item[7]})
            self.listbox5.itemconfig(END,{'bg':item[7]})
            self.listbox6.itemconfig(END,{'bg':item[7]})
            self.listbox7.itemconfig(END,{'bg':item[7]})


    def show(self):
        self.window.mainloop()




if __name__ == "__main__":
    newwindow=App()
    newwindow.show()
