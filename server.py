#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("client: ", client)
        print("client_address: ", client_address)
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        
        
def permision(client, name):
    client.send(bytes('Wait for the permission from host', 'utf8'))
    msg = '%s want to join the chatroom\n {yes} or {no}\n' % name
    name_list = []
    for x in clients:
        name_list.append(x)
    clients[name_list[0]].send(bytes(msg, 'utf8'))
    if clients[name_list[0]].recv(BUFSIZ).decode('utf8') == '{yes}':
        return 
    else:
        client.send(bytes('Sorry, you are rejected to join the chatroom', 'utf8'))
        client.close()
    """for x in clients:
        x.send(bytes(msg, 'utf8'))
        if x.recv(BUFSIZ).decode('utf8') == 'yes':
            return 
        else:
            client.send(bytes('Sorry, you are rejected to join the chatroom', 'utf8'))
            client.close()"""
        
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    if clients != {}:
        permision(client, name)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    list = []
    if len(clients) == 0:
        client.send(bytes('nobody in the chatroom', 'utf8'))
    else:
        for people in clients:
            list.append(people)
        client.send(bytes(list[0] +' is in the chatroom', 'utf8') if len(clients) == 1 else bytes(', '.join(list) + ' are in the chatroom', 'utf8'))
    clients[name] = client

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            if msg == bytes('{yes}', 'utf8') or msg == bytes('{no}', 'utf8'):
                continue
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[name]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for name in clients:
        clients[name].send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
print("HOST: " + gethostbyname(gethostname()))
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
