from Tkinter import *
import tkFileDialog

class TkOpenFileDialogExample(Frame):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.pack()

        self.label_open = Label(self.frame, text="Choose input file:")
        self.label_open.grid(row=0, columnspan=2)
        
        self.button_open = Button(self.frame, text="OPEN", fg="red", command=self.openFile)
        self.button_open.grid(row=1)

        self.button_close = Button(self.frame, text="CLOSE", fg="black", command=root.destroy)
        self.button_close.grid(row=1, column=1)

        self.strView = StringVar()  # this is used to update the label in real time
        self.label_filename = Label(self.frame, textvariable=self.strView, fg="black")
        self.label_filename.grid(row=2, columnspan=2)

    def openFile(self):
        file_opt = {}
        file_opt['filetypes']=[('all files','.*'), ('text files', '.txt'), ('csv files','.csv')]
        file_opt['parent'] = root

        filename = tkFileDialog.askopenfilename(**file_opt)
        if filename:
            print filename
            self.strView.set(filename)

root = Tk()
root.title("Tk")

root.update()

# Begin code to center the window
w = root.winfo_width()
h = root.winfo_height()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw/2) - (w/2)
y = (sh/2) - (h/2)
# root.geometry('%dx%d+%d+%d' % (w,h,x,y,)) use this if you made window with specific width and height
root.geometry('+%d+%d' % (x,y))

app = TkOpenFileDialogExample(root)

root.mainloop()
