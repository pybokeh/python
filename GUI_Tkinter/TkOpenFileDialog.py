from Tkinter import *
import tkFileDialog

class TkOpenFileDialog(Frame):
    """ A GUI class that sets up a basic open file dialog window with an open file button.
        You'll have to implement the close button outside this class-couldn't figure out
        how to do it within this class"""
    
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        self.label_open = Label(self.frame, text="Choose input file:")
        self.label_open.grid(row=0, columnspan=2)
        
        self.button_open = Button(self.frame, text="OPEN", fg="red", command=self.openFile)
        self.button_open.grid(row=1)

        # self.button_close = Button(self.frame, text="CLOSE", fg="black", command=root.destroy)
        #self.button_close = Button(self.frame, text="CLOSE", fg="black", command=self.frame.quit)
        #self.button_close.grid(row=1, column=1)

        self.strView = StringVar()  # this is used to update the label in real time
        self.label_filename = Label(self.frame, textvariable=self.strView, fg="black")
        self.label_filename.grid(row=2, columnspan=2)

    def openFile(self):
        file_opt = {}
        file_opt['filetypes']=[('all files','.*'), ('text files', '.txt'), ('csv files','.csv')]
        #file_opt['parent'] = root

        filename = tkFileDialog.askopenfilename(**file_opt)
        if filename:
            print filename
            self.strView.set(filename)

if __name__ == "__main__":
    root = Tk()
    root.title("Tk")
    root.update()
    app = TkOpenFileDialog(root)
    root.mainloop()
