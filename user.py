#!/usr/bin/env python3
"""Script for tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print('\n'+msg)
        except OSError:  # Possibly client has left the chat.
            break
        if msg == 'Sorry, you are rejected to join the chatroom':
            client_socket.close()
            break


def send():  # event is passed by binders.
    """Handles sending of messages."""
    while True:
        
        msg = input()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            break
        """if msg == "{yes}" or msg == "{no}":
            client_socket.send(bytes(msg, "utf8"))"""




#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()

