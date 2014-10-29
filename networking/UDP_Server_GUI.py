# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 17:22:25 2012

@author: pybokeh
"""

from Tkinter import *
import socket

class UDP_Server_GUI(Frame):
    def __init__(self, master):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.max_data = 65535
        host = '127.0.0.1'
        port = 1060
        self.s.bind((host,port))
        
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
        
        self.btnSend = Button(self.frame,text="Send", command=self.SendBtn)
        self.btnSend.grid(row=6, column=0)
        
        self.strServer.set(host)
        self.strPort.set(port)

    def SendBtn(self):
        server = self.strServer.get()
        self.History.insert(END, server+':'+self.strMessage.get())
        self.History.yview_scroll(1, "units")

"""        
    def SendBtn(self):
        history_old = self.strHistory.get()
        #self.strMessage.set(str(len(history_old)))
        if len(history_old) > 0:
            self.strHistory.set(history_old+'\n'+self.strMessage.get())
        else:
            self.strHistory.set(self.strMessage.get())"""
        
if __name__ == "__main__":
    root = Tk()
    root.title("UDP Chat Server GUI")
    app = UDP_Server_GUI(root)
    
    while True:
        root.update()
        data, address = app.s.recvfrom(app.max_data)
        client_ip, client_port = address
        app.History.insert(END, client_ip+':'+str(data))
        app.s.sendto(app.strMessage.get(), (client_ip, client_port))
        root.mainloop()
