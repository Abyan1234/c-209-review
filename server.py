# ------- Bolierplate Code Start -----


import socket
from  threading import Thread
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}

def handleClient(client,client_name):
    global clients
    global SERVER
    msg="Welcome, You Are Connected To The Server\n Click on refresh to see all available users"
    client.send(msg.encode('utf-8'))
    while True:
        try:
            chunk=client.recv(4096)
            msg=chunk.decode().strip().lower()
            if msg:
                handleMessages(client,msg,client_name)
            else:
                #removeClient(client_name)
                pass
        except:
            pass

def handleMessages(client,msg,client_name):
    if msg=='Show List':
        handleShowList(client)

def handleShowList(client):
    global clients
    counter=0
    for i in clients:
        counter+=1
        client_address=clients[i]["address"][0]
        connected_with=clients[i]["connected_with"]
        msg=""
        if connected_with:
            msg=f"{counter},{i},{client_address},connected with {connected_with},tiul"
        else:
            msg=f"{counter},{i},{client_address},available"
        client.send(msg.encode('utf-8'))



def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client, addr)
        client_name=client.recv(4096).decode().lower()
        clients[client_name]={
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096,
        }
        thread=Thread(target=handleClient,args=(client,client_name))
        thread.start()

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()

# ------ Bolierplate Code End -----------
