import pyodbc as pyodbc
from Tkinter import *

class DBmetadata (Frame):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.pack()

        self.lblUserID = Label(self.frame, text="User ID: ")
        self.lblUserID.grid(row=0, column=0)

        self.strUserID = StringVar()
        self.UserID = Entry(self.frame, textvariable=self.strUserID, width=8, borderwidth=2)
        self.UserID.grid(row=0, column=1)

        self.lblPassword = Label(self.frame, text="Password: ")
        self.lblPassword.grid(row=1, column=0)

        self.strPassword = StringVar()
        self.Password    = Entry(self.frame, width=15, textvariable=self.strPassword, show="*")
        self.Password.grid(row=1, column=1)


if __name__ == "__main__":
    root = Tk()
    root.title("DB Browser")
    root.update()
    app = DBmetadata(root)
    root.mainloop()



"""
userid = raw_input("Enter your user id: ")
pw     = raw_input("Enter your password: ")
cnxn_string = 'DSN=CMQ_PROD;UID=' + userid + ';PWD=' + pw


cnxn = pyodbc.connect(cnxn_string)
cursor = cnxn.cursor()
cursor.execute("SELECT MDL_YR, FCTRY_CD, MDL_NM FROM CMQ.V_DIM_MTO_FEATURE_PIVOT WHERE MDL_YR = 2012")
row = cursor.fetchone()
if row:
   print row
"""
