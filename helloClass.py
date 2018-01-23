from Tkinter import *

class App:
    #master is the parent widget
    def __init__(self, master):

        frame = Frame(master)
        frame.pack() #make Frame widget (simple container) visible

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        #fg is foreground, command specify function called when btn clicked
        

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.button.pack(side=LEFT)
        self.hi_there.pack(side=LEFT)

        #btns were stored in instance attribs, then packed , 
        # widgets packed relative to their parent (btns -> frame -> master)

    def say_hi(self):
        print "hi there, everyone!"

root = Tk()

app = App(root)

root.mainloop() #runs till window exited/frame quitted
root.destroy() # optional;only needed under certain dev enviros, explicitly destroys main window

#frame var stored locally, what happens when __init__ returns?
#Tkinter auto keeps widget tree, so wont disappear when last ref disappears, must be explicitly destroyed (.destroy()
# if you want to do something with widget after creation should keep ref
#BEST FORM: separate construction from packing

#Tcl command, create button named ok, child to widget named dialog button .dialog.ok
#tkinter call ok=Button(dialog) , ok/dialog are refs to widget instances, not names
#tcl needs names, tkinter auto assigns unique names to new widgets, get name print str(ok), 
# can use name option to explicit name, useful when need to interface with tcl directly
# cannot chnage name once assigned, 