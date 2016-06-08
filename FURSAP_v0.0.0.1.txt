import Tkinter as T #What I use to create the GUI.
import socket #Allows me to create and manipulate sockets.
import asyncore #Makes asynchronus socket setup quick and easy.
#import select #Lets me do lower-level socket programming.
#import time #Basically just for updating the GUI.

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


#http://stackoverflow.com/questions/3670127/python-socketserver-sending-to-multiple-clients

class EchoHandler(asyncore.dispatcher_with_send):
    def __init__(self, host, socket, address):
        asyncore.dispatcher_with_send.__init__(self,socket)
        self.host=host
        self.outbox=[]
        
    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.host.broadcast(data)
            
    def say(self, message):
        self.outbox.append(message)
        
    def handle_write(self):
        if not self.outbox:
            return
        message=self.outbox.popleft()
        #if len(message)>MAX_MESSAGE_LENGTH:
            #raise ValueError("Message too long")
        self.send(message)
        
"""At this point, how can the data I receive be sent to all sockets?"""
class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.clients=[]

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.clients.append(EchoHandler(self, sock, addr))
            print 'Incoming connection from %s' % repr(addr)
            
    def broadcast(self, message):
        for client in self.clients:
            client.say(message)

"""At this point, I want a button in the GUI to create a server"""
#server = EchoServer('localhost', 8080)
#asyncore.loop()