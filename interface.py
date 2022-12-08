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
    # check if color is too close to black or white
    while (red<150 and blue<150 and green<150) or(red>175 and blue>175 and green>175):
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
    # self.descLabel = Label contenant la description de la trame
    # self.filtered_data = Liste des trames filtrées
    # self.backgroundcolor = Couleur utilisée pour le fond des listbox

    # Constructor
    def __init__(self):
        
        self.window=Tk()
        self.window.geometry("1500x600")
        if (platform.system()=="Windows"):
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.window.title("Visualisateur de trames")
        self.window.resizable(False, False)
        self.first=True
        self.openbutton=ttk.Button(self.window, text="Ouvrir un fichier", command=self.openFile)
        self.welcometext=Label(self.window, text="Bienvenue dans le visualisateur de trames !")
        self.welcometext.pack()
        self.openbutton.config(width=20,padding=10,style="TButton")
        self.welcometext.pack(side="top")
        self.welcometext.place(relx=0.5, rely=0.2, anchor=CENTER)
        # first openfile button
        self.openbutton.pack(side=TOP)
        self.openbutton.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.i=0

    # function that open a file and display the frames
    def openFile(self):
        # OS fileopen function

        file = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        try:
            self.frames=input.input(file) # can raise an Exception
        except FileNotFoundError as inst:
            raise inst
        except Exception as inst:
            messagebox.showerror("Erreur", "Erreur lors de l'ouverture du fichier : "+str(inst))
            raise inst
        if (self.first):
            self.createParts()
        self.__showFrames(self.frames)
        self.first=False 
        
    
    # function that create the parts of the interface
    def createParts(self):
        # create a menu that display frames in a listbox and a scrollbar
        self.openbutton.destroy()
        self.welcometext.destroy()
        if (platform.system()=="Windows"):
            self.backgroundcolor="#f0f0f0"
        elif (platform.system()=="Darwin"):
            self.backgroundcolor="#f0f0f0"
        else:
            self.backgroundcolor="#d9d9d9"
        self.filtered_data=list()
        #create a frame to display the listbox and the scrollbar
        self.listboxframe=Frame(self.window,width=1200,height=500)
        self.listboxframe.pack(side=TOP)
        self.listboxframe.rowconfigure(0,weight=1)
        # create listboxes to display the frames
        # listbox1 = source
        self.listbox1 = Listbox(self.listboxframe, width=14, height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox1.grid(row=1,column=0,pady=30)
        ip1label=Label(self.listboxframe,text="Ip1",font=("Helvetica", 14))
        ip1label.grid(row=0,column=0,sticky="s",pady=(30,0))
        self.listboxlabel1=Label(self.listboxframe,text="Ip1",font=("Helvetica", 14))
        # listbox2 = source port
        self.listbox2=Listbox(self.listboxframe,width=7,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox2.grid(row=1,column=1,pady=30)
        port1label=Label(self.listboxframe,text="Port1",font=("Helvetica", 14))
        port1label.grid(row=0,column=1,sticky="s",pady=(30,0))
        # listbox3 = arrow
        self.listbox3=Listbox(self.listboxframe,width=40,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox3.grid(row=1,column=2,pady=30)

        # listbox4 = destination
        self.listbox4=Listbox(self.listboxframe,width=14,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox4.grid(row=1,column=3,pady=30)
        ip2label=Label(self.listboxframe,text="Ip2",font=("Helvetica", 14))
        ip2label.grid(row=0,column=3,sticky="s",pady=(30,0))
        # listbox5 = destination port
        self.listbox5=Listbox(self.listboxframe,width=7,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox5.grid(row=1,column=4,pady=30)
        port2label=Label(self.listboxframe,text="Port2",font=("Helvetica", 14))
        port2label.grid(row=0,column=4,sticky="s",pady=(30,0))
        # listbox6 = protocol
        self.listbox6=Listbox(self.listboxframe,width=9,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox6.grid(row=1,column=5,pady=30)
        protocol=Label(self.listboxframe,text="Protocol",font=("Helvetica", 14))
        protocol.grid(row=0,column=5,sticky="s",pady=(30,0))
        # listbox7 = Description
        self.listbox7=Listbox(self.listboxframe,width=35,height=16,borderwidth=0,highlightthickness=0,font=("Helvetica", 14),exportselection=0,activestyle="none",background=self.backgroundcolor)
        self.listbox7.grid(row=1,column=6,pady=30)
        description=Label(self.listboxframe,text="Description",font=("Helvetica", 14))
        description.grid(row=0,column=6,sticky="s",pady=(30,0))
        # create a scrollbar to scroll all listboxes
        scrollbar = Scrollbar(self.listboxframe, orient="vertical",background="#f0f0f0")
        scrollbar.grid(row=1,column=7,pady=30,sticky="ns")
        scrollbar.config(command=self.__multiple_yview)
        self.listbox1.config(yscrollcommand=scrollbar.set)
        self.listbox2.config(yscrollcommand=scrollbar.set)
        self.listbox3.config(yscrollcommand=scrollbar.set)
        self.listbox4.config(yscrollcommand=scrollbar.set)
        self.listbox5.config(yscrollcommand=scrollbar.set)
        self.listbox6.config(yscrollcommand=scrollbar.set)
        self.listbox7.config(yscrollcommand=scrollbar.set)

        # calls on_select1 to on_select7 when selecting an element
        self.listbox1.bind("<<ListboxSelect>>", self.on_select1)
        self.listbox2.bind("<<ListboxSelect>>", self.on_select2)
        self.listbox3.bind("<<ListboxSelect>>", self.on_select3)
        self.listbox4.bind("<<ListboxSelect>>", self.on_select4)
        self.listbox5.bind("<<ListboxSelect>>", self.on_select5)
        self.listbox6.bind("<<ListboxSelect>>", self.on_select6)
        self.listbox7.bind("<<ListboxSelect>>", self.on_select7)

        if (platform.system() in ["Windows","Darwin"]):
            # Scroll bind defined by <MouseWheel> on Windows and macOS
            mousewheel="<MouseWheel>"
            self.listbox1.bind(mousewheel, self.on_mousewheel)
            self.listbox2.bind(mousewheel, self.on_mousewheel)
            self.listbox3.bind(mousewheel,self.on_mousewheel)
            self.listbox4.bind(mousewheel, self.on_mousewheel)
            self.listbox5.bind(mousewheel, self.on_mousewheel)
            self.listbox6.bind(mousewheel, self.on_mousewheel)
            self.listbox7.bind(mousewheel, self.on_mousewheel)
        else: 
            # Scroll bind defined by <Button-4> and <Button-5> on linux
            self.listbox1.bind("<Button-4>", self.on_mousewheel)
            self.listbox2.bind("<Button-4>", self.on_mousewheel)
            self.listbox3.bind("<Button-4>", self.on_mousewheel)
            self.listbox4.bind("<Button-4>", self.on_mousewheel)
            self.listbox5.bind("<Button-4>", self.on_mousewheel)
            self.listbox6.bind("<Button-4>", self.on_mousewheel)
            self.listbox7.bind("<Button-4>", self.on_mousewheel)
            self.listbox1.bind("<Button-5>", self.on_mousewheel)
            self.listbox2.bind("<Button-5>", self.on_mousewheel)
            self.listbox3.bind("<Button-5>", self.on_mousewheel)
            self.listbox4.bind("<Button-5>", self.on_mousewheel)
            self.listbox5.bind("<Button-5>", self.on_mousewheel)
            self.listbox6.bind("<Button-5>", self.on_mousewheel)
            self.listbox7.bind("<Button-5>", self.on_mousewheel)



        # bottom part of the screen
        self.frame2=Frame(self.window,width=600,height=300)
        self.frame2.pack(side=BOTTOM,fill=X,expand=1)
        button2=ttk.Button(self.frame2,text="Exporter",command=lambda: self.export(),width=20,padding=10,style="TButton")
        button2.grid(row=1,column=5,padx=10,pady=10,sticky="nsew")
        button3=ttk.Button(self.frame2,text="Ouvrir un fichier",command=lambda: self.openFile(),width=20,padding=10,style="TButton")
        button3.grid(row=1,column=4,padx=10,pady=10,sticky="nsew")
        
        # set filter box
        self.filtervalue=StringVar()
        self.filterentry=Entry(self.frame2,width=18,textvariable=self.filtervalue,font=("Helvetica", 12))
        self.filterentry.config()
        filtertext=Label(self.frame2,text="Filtrer",font=("Helvetica", 12))
        filtertext.grid(row=0,column=0,padx=10,pady=0,sticky="nsew")
        self.filterentry.grid(row=1,column=0,padx=10,pady=15,sticky="nsew")
        self.frame2.columnconfigure(1,weight=1)
        self.frame2.columnconfigure(2,weight=1)
        self.frame2.columnconfigure(3,weight=1)
        # enter defined by <Return>
        self.filterentry.bind("<Return>",self.filter_search)
        self.descLabel=Label(self.frame2,text="",font=("Helvetica", 12))
        self.descLabel.grid(row=1,column=3,padx=0,pady=0,sticky="nsew")

    # scroll one listbox scrolls all others
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
        self.descLabel.config(text="")
        for frame in frames:
            source,sourceport,arrow,dest,destport,protocol,desc,color=self.analyse(frame)
            self.itemlist.append((source,sourceport,arrow,dest,destport,protocol,desc,color))

            self.listbox1.insert(END, source)
            self.listbox2.insert(END, sourceport)
            self.listbox3.insert(END, arrow)
            self.listbox4.insert(END, dest)
            self.listbox5.insert(END, destport)
            self.listbox6.insert(END, protocol)
            self.listbox7.insert(END, desc)
            if (color=="#000000"): # if the frame is in black
                self.listbox1.itemconfig(self.i,fg="white",bg=color)
                self.listbox2.itemconfig(self.i,fg="white",bg=color)
                self.listbox3.itemconfig(self.i,{'bg':self.backgroundcolor})
                self.listbox4.itemconfig(self.i,fg="white",bg=color)
                self.listbox5.itemconfig(self.i,fg="white",bg=color)
                self.listbox6.itemconfig(self.i,fg="white",bg=color)
                self.listbox7.itemconfig(self.i,bg=self.backgroundcolor)
            else:
                self.listbox1.itemconfig(self.i,{'bg':color})
                self.listbox2.itemconfig(self.i,{'bg':color})
                self.listbox3.itemconfig(self.i,{'bg':self.backgroundcolor})
                self.listbox4.itemconfig(self.i,{'bg':color})
                self.listbox5.itemconfig(self.i,{'bg':color})
                self.listbox6.itemconfig(self.i,{'bg':color})
                self.listbox7.itemconfig(self.i,{'bg':self.backgroundcolor})
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

    # called by selecting an element from listbox1
    def on_select1(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox1.curselection()[0]
        self.select_others(index,self.listbox2,self.listbox4,self.listbox5,self.listbox6,self.listbox7)

    # called by selecting an element from listbox2
    def on_select2(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox2.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox4,self.listbox5,self.listbox6,self.listbox7)
    
    # called by selecting an element from listbox3
    def on_select3(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox3.curselection()[0]
        self.listbox3.selection_clear(0,END)
        self.select_others(index,self.listbox1,self.listbox2,self.listbox4,self.listbox5,self.listbox6,self.listbox7)
    
    # called by selecting an element from listbox4
    def on_select4(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox4.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox5,self.listbox6,self.listbox7)

    # called by selecting an element from listbox5
    def on_select5(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox5.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox4,self.listbox6,self.listbox7)
    
    # called by selecting an element from listbox6
    def on_select6(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox6.curselection()[0]
        self.select_others(index,self.listbox1,self.listbox2,self.listbox4,self.listbox5,self.listbox7)
    
    # called by selecting an element from listbox7
    def on_select7(self,event):
        if (self.filtered_data==[] and self.filtervalue.get()!=""):
            return
        index=self.listbox7.curselection()[0]
        all_desc=self.listbox7.get(0,END)
        self.descLabel.config(text="Description : "+all_desc[index])
        self.listbox7.selection_clear(0,END)
        self.select_others(index,self.listbox1,self.listbox2,self.listbox4,self.listbox5,self.listbox6)
    
    # select the same element in the others listbox
    def select_others(self,index,*others):
        for other in others:
            if (other==self.listbox7):
                all_desc=other.get(0,END)
                self.descLabel.config(text="Description : "+all_desc[index])
                other.selection_clear(0,other.size()-1)
            else:
                other.selection_clear(0,other.size()-1)
                other.selection_set(index)

    # called by scrolling the mouse wheel
    def on_mousewheel(self,event):
        # depending on the OS, scrolling values are not managed by the same way
        if (platform.system()=="Windows"):
            value=(-1)*int(event.delta/120)
        elif platform.system()=="Darwin":
            value=(-1)*int(event.delta)
        else: 
            if (int(event.num)==5):
                value=1
            else : 
                value=-1
        
        self.listbox1.yview_scroll(value,"units")
        self.listbox2.yview_scroll(value,"units")
        self.listbox3.yview_scroll(value,"units")
        self.listbox4.yview_scroll(value,"units")
        self.listbox5.yview_scroll(value,"units")
        self.listbox6.yview_scroll(value,"units")
        self.listbox7.yview_scroll(value,"units")
        return "break"



    # export the frames in a txt file
    def export(self):
        if (len(self.filtered_data)==0):
            # write the whole itemlist in a txt file
            file = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            f=open(file,"w",encoding="utf-8")
            for item in self.itemlist:
                f.write("Adresse 1 :"+item[0]+":"+item[1]+" "+item[2]+" Adresse 2 : "+item[3]+":"+item[4]+"    Protocol : "+item[5]+"    Description : "+item[6]+"\n")
                f.write("#"*100+"\n"+"#"*100+"\n")
            f.close()
        else:
            # write the filtered itemlist in a txt file
            f=open(file,"w",encoding="utf-8")
            for item in self.filtered_data:
                f.write("Adresse 1 :"+item[0]+":"+item[1]+" "+item[2]+" "+item[3]+":"+item[4]+"    Protocol : "+item[5]+"    Description : "+item[6]+"\n")
                f.write("#"*100+"\n"+"#"*100+"\n")
            f.close()
        pass



    # return a list of couples ip source and ip destination by looking at the list of frames already displayed
    def find_couple(self,ip1,ip2):
        # depending on the OS, the arrow is different
        if (platform.system() not in ["Windows","Darwin"]):
            arrowr="  ------------------------------------------------------------>"
            arrowl="  <------------------------------------------------------------"
        else:
            arrowr="  ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⟶"
            arrowl="  ⟵⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"

        for couple in self.ip_couples:
            if (couple[0]==ip1 and couple[1]==ip2):
                return (arrowr,couple[2])
            if (couple[0]==ip2 and couple[1]==ip1):
                return (arrowl,couple[2])
        return None


    # analyse the frame and return a string containing the frame's content and a color
    def analyse(self,frame):
        ethernet_header=extract.extract_ethernet_header(frame)
        if (platform.system() not in ["Windows","Darwin"]):
            arrowr="  ------------------------------------------------------------>"
            arrowl="  <------------------------------------------------------------"
        else:
            arrowr="  ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⟶"
            arrowl="  ⟵⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"

        infos=""
        if (ethernet_header[1].lower()=="ff:ff:ff:ff:ff:ff"):
            infos=infos+"Broadcast"
        if (not extract.check_if_ip(frame)):
            return (ethernet_header[1],"",arrowr,ethernet_header[0],"","None",infos,"#000000")
        ip_header=extract.extract_ip_header(frame)
        if (int(ip_header[1],16)*4<20):
            return (ethernet_header[1],"",arrowr,ethernet_header[0],"","IP","IP header too short","#000000")
        # find the couple of ip addresses in the list of couples
        couple=self.find_couple(ip_header[7],ip_header[8])


        # if the couple is not in the list of couples, add it
        if (couple==None):
            color=random_color()
            self.ip_couples.append((ip_header[7],ip_header[8],color))
            arrow=arrowr
        else:
            color=couple[1]
            arrow=couple[0]

        

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
            return (extract.str_to_ip(ip_header[7]),"None",arrow,extract.str_to_ip(ip_header[8]),"None","IP","Not a TCP frame"+infos,color)
        tcp_header=extract.extract_tcp(frame)
        if (tcp_header[4]<20):
            return (extract.str_to_ip(ip_header[7]),"None",arrow,extract.str_to_ip(ip_header[8]),"None","IP","TCP header too short",color)
        prot="TCP"

        tcp_flags=tcp_header[5]
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
        if ( tcp_header[0]=='0050' or tcp_header[1]=='0050'): # if the port is not 80 (HTTP)
            http=extract.extract_http(frame)
            infos=infos+" "+http    
            prot=prot+"/HTTP"
            
        return (extract.str_to_ip(ip_header[7]),str(int(tcp_header[0],16)),arrow,extract.str_to_ip(ip_header[8]),str(int(tcp_header[1],16)),prot,infos,color)

    
    # filter the listbox with the filter entry
    def filter_search(self,event):
        # filter syntax : ip1==ip1,ip2,ip3;port1==44,99,447;etc..
        sstr = self.filtervalue.get()
        regex = re.compile(r'([a-zA-Z0-9_]+==[a-zA-Z0-9_,]+)') # pattern to find in StringVar
        match=regex.findall(sstr)
        if (sstr!="" and match==None):
            self.filterentry.config({"background":"#e8c0be"})
            return
        self.filtervalue.set(';'.join(match)) # removes all wrong filters of the entry
        filterdict={}
        for i in match:
            split1=i.split("==")
            filterdict[split1[0]]=split1[1].split(",")
        # Check if the filter is correct
        for i in filterdict:
            if (i.lower()!="ip1" and i.lower()!="ip2" and i.lower()!="port1" and i.lower()!="port2" and i.lower()!="protocol" and i.lower()!="desc"):
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
        if match == []:
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
                self.listbox3.itemconfig(END,{'bg':self.backgroundcolor})
                self.listbox4.itemconfig(END,{'bg':item[7]})
                self.listbox5.itemconfig(END,{'bg':item[7]})
                self.listbox6.itemconfig(END,{'bg':item[7]})
                self.listbox7.itemconfig(END,{'bg':self.backgroundcolor})
            return
        self.filterentry.config({"background":"#b7e6b1"})
        self.filtered_data = list()
        # check every frame
        for item in self.itemlist:
            ok=True
            # check every captured filter
            for i in filterdict:
                if i.lower()=="ip1":
                    found1=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[0].find(j) >= 0:
                            found1=True
                            break
                    ok=ok and found1
                if i.lower()=="ip2":
                    found2=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[3].find(j) >= 0:
                            found2=True
                            break
                    ok=ok and found2
                if i.lower()=="port1":
                    found3=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[1]==j:
                            found3=True
                            break
                    ok=ok and found3
                if i.lower()=="port2":
                    found4=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[4]==j:
                            found4=True
                            break
                    ok=ok and found4
                if i.lower()=="protocol":
                    found5=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[5].find(j) >= 0:
                            found5=True
                            break
                    ok=ok and found5
                if i.lower()=="desc":
                    found6=False
                    # check if entered filter values are in the frame
                    for j in filterdict[i]:
                        if item[6].find(j) >= 0:
                            found6=True
                            break
                    ok=ok and found6
            if ok:
                self.filtered_data.append(item)
        
        for item in self.filtered_data:
            self.listbox1.insert(END, item[0])
            self.listbox2.insert(END, item[1])
            self.listbox3.insert(END, item[2])
            self.listbox4.insert(END, item[3])
            self.listbox5.insert(END, item[4])
            self.listbox6.insert(END, item[5])
            self.listbox7.insert(END, item[6])
            self.listbox1.itemconfig(END,{'bg':item[7]})  
            self.listbox2.itemconfig(END,{'bg':item[7]})
            self.listbox3.itemconfig(END,{'bg':self.backgroundcolor})
            self.listbox4.itemconfig(END,{'bg':item[7]})
            self.listbox5.itemconfig(END,{'bg':item[7]})
            self.listbox6.itemconfig(END,{'bg':item[7]})
            self.listbox7.itemconfig(END,{'bg':self.backgroundcolor})


    def show(self):
        self.window.mainloop()




if __name__ == "__main__":
    newwindow=App()
    newwindow.show()
