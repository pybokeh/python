from Tkinter import *
from TkOpenFileDialog import TkOpenFileDialog
import tkFileDialog

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

app = TkOpenFileDialog(root)
button_close = Button(app.frame, text="CLOSE", fg="black", command=root.destroy)
button_close.grid(row=1, column=1)

root.mainloop()
