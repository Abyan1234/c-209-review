#-----------Bolierplate Code Start -----
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None


def connectToServer():
    global SERVER
    global name
    cname=name.get()
    SERVER.send(cname.encode('utf-8'))


def showClientList():
    global SERVER
    global listbox

    SERVER.send("Show List".encode('utf-8'))

def openChatWindow():

   
    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('File Sharing App')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10))
    namelabel.place(x=10, y=8)

    name = Entry(window,width =30,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

    connectserver = Button(window,text="Connect to Chat Server",bd=1, font = ("Calibri",10))
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10), command=connectToServer)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10))
    disconnectButton.place(x=350,y=160)

    refresh=Button(window,text="Refresh",bd=1, font = ("Calibri",10),command=showClientList)
    refresh.place(x=435,y=160)

    chat = Label(window, text= "Chat Window", font = ("Calibri",10))
    chat.place(x=10, y=180)

    textarea=Text(window,width=67,height=6,font=("Calibri",10))
    textarea.place(x=10,y=200)

    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = textarea.yview)

    attach=Button(window,text="Attach & Send",bd=1, font = ("Calibri",10))
    attach.place(x=10,y=305)
  
    attachBox=Entry(window,width =47,font = ("Calibri",10))
    attachBox.place(x=100,y=305)
    
    send=Button(window,text="Send",bd=1, font = ("Calibri",10))
    send.place(x=450,y=305)
  
  
  
  
    window.mainloop()


def receiveMessage():
    global SERVER
    while True:
        chunk=SERVER.recv(4096)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list=chunk.decode().split(",")
                listbox.insert(letter_list[0]+": "+letter_list[1]+": "+letter_list[3])
            else:
                textarea.insert(chunk.decode('utf-8'))
        except:
            pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    
    thread=Thread(target=receiveMessage)
    thread.start()
   
    openChatWindow()

setup()
