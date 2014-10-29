# -*- coding: utf-8 -*-
"""
REFERENCE to make this app non-blocking:
http://docs.python.org/release/3.2/faq/gui.html#can-i-have-tk-events-handled-while-waiting-for-i-o
http://python.6.n6.nabble.com/Fw-Tkinter-s-createfilehandler-attempt-to-run-parallel-threads-td1974704.html
http://codeidol.com/python/python3/GUI-Coding-Techniques/More-Ways-to-Add-GUIs-to-Non-GUI-Code/
Created on Sun Feb 12 17:22:25 2012

@author: pybokeh
"""

from Tkinter import *
import socket

class TCP_Server_GUI(Frame):
    def __init__(self, master):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_data = 512
        self.host = '127.0.0.1'
        self.port = 1060
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen(5)
        
        self.frame = Frame(master)
        self.frame.pack()

        self.lblServer = Label(self.frame, text="Server IP:")
        self.lblServer.grid(row=0, column=0)
        
        self.strServer = StringVar()
        self.Server = Entry(self.frame, textvariable=self.strServer, width=16, borderwidth=2)
        self.Server.grid(row=0, column=1)
        
        self.lblPort = Label(self.frame, text="Server Port:")
        self.lblPort.grid(row=1, column=0)
        
        self.strPort = StringVar()
        self.Port = Entry(self.frame, textvariable=self.strPort, width=6, borderwidth=2)
        self.Port.grid(row=1, column=1)
        
        self.lblHistory = Label(self.frame, text="Message History:")
        self.lblHistory.grid(row=2, column=0)
        
        self.History = Listbox(self.frame, height=5, width=50)
        self.History.grid(row=3, columnspan=2)

        self.sbar = Scrollbar(self.frame, orient=VERTICAL, command=self.History.yview)
        self.sbar.grid(row=3, column=2)
        self.History['yscrollcommand']=self.sbar.set
        
        self.lblMessage = Label(self.frame, text="Outgoing Message:")
        self.lblMessage.grid(row=4, column=0)
        
        self.strMessage = StringVar()
        self.Message = Entry(self.frame, textvariable=self.strMessage, borderwidth=2, width=50)
        self.Message.grid(row=5, columnspan=2)
        """
        self.btnSend = Button(self.frame,text="Send", command=self.SendBtn)
        self.btnSend.grid(row=6, column=0)"""
        
        self.strServer.set(self.host)
        self.strPort.set(self.port)
        
        self.client_socket, self.client_address = self.server_socket.accept()
    """
    def SendBtn(self):
        self.History.insert(END, self.host+':'+str(self.port)+'--->'+self.strMessage.get())
        self.History.yview_scroll(1, "units")
        self.client_socket.send(self.strMessage.get())
        self.strMessage.set('')"""
        
if __name__ == "__main__":        
    def SendBtn():
        app.History.insert(END, app.host+':'+str(app.port)+'--->'+app.strMessage.get())
        app.History.yview_scroll(1, "units")
        app.client_socket.send(app.strMessage.get())
        app.strMessage.set('')    
        
    root = Tk()
    root.title("TCP Chat Server GUI")
    app = TCP_Server_GUI(root) 
    app.btnSend = Button(app.frame,text="Send", command=SendBtn)
    app.btnSend.grid(row=6, column=0)    
    root.update()
    while True:
        print "I am in the while loop"
        data = app.client_socket.recv(app.max_data)
        client_ip, client_port = app.client_address
        app.History.insert(END, client_ip+':'+str(client_port)+'--->'+str(data))
        root.update()
        print "Performed screen refresh\n"
        root.mainloop()
            
    """
    while True:
        root.update()
        root.mainloop()
        client_socket, client_ip = app.server_socket.accept()
        root.mainloop()
        while True:
            data = client_socket.recv(app.max_data)
            if (data == 'Q' or data == 'q'):
                client_socket.close()
                break
            else:
                app.History.insert(END, "FromClient:")
            root.mainloop()"""
