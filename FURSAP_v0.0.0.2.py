"""
FURSAP version 0.0.0.2
"""

import Tkinter as T #What I use to create the GUI. This may be switched to another GUI module.
import socket #Allows me to create and manipulate sockets.
import asyncore #Makes asynchronus socket setup quick and easy.
import collections #Adds faster lists.  
#import logging #Tells user things and helps debug somethings
#import select #Lets me do lower-level socket programming.
#import time #Basically just for updating the GUI.



"""The following code is for a server socket to receive and send messages to all connected clients."""
#http://stackoverflow.com/questions/3670127/python-socketserver-sending-to-multiple-clients

class EchoHandler(asyncore.dispatcher):
    def __init__(self, host, socket, address):
        asyncore.dispatcher.__init__(self,socket)
        self.host=host
        self.outbox=collections.deque()
        
    def handle_read(self):  #When the client sends stuff to the socket, this triggers.
        data = self.recv(8192)
        if data:
            self.host.broadcast(data)
            
    def say(self, message): #Messages the server needs to send are saved in the outbox.
        self.outbox.append(message)
        
    def handle_write(self):
        if not self.outbox:
            return
        message=self.outbox.popleft()
        #if len(message)>MAX_MESSAGE_LENGTH:
            #raise ValueError("Message too long")
        self.send(message)
        
class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.clients=[]

    def handle_accept(self): #When the client connects to the server, this creates a socket for the client.
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.clients.append(EchoHandler(self, sock, addr)) #This both creates a new unique socket for the client and adds it to a list. I'll likely call these Echohandlers.
            print 'Incoming connection from %s' % repr(addr) 
            
    def broadcast(self, message): #Sends a message to all clients.
        for client in self.clients:
            client.say(message)

#server = EchoServer('localhost', 8080)
#asyncore.loop()



"""This is the GUI which is used to create the server."""
root=T.Tk() #This is the window.
ip1= T.Label(root, text="IP: ").grid(row=0, column=0)
ip2=T.Label(root, text= socket.gethostbyname(socket.gethostname())).grid(row=0, column=1)
port1= T.Label(root, text="Port: ").grid(row=1, column=0)
global port2
port2= T.Entry(root)
port2.grid(row=1, column=1)
usern1=T.Label(root, text="Expected total users: ").grid(row=2, column=0)
global usern2
usern2=T.Entry(root)
usern2.grid(row=2, column=1)
clientlist=[]