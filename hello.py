from Tkinter import *

root= Tk()
#Tk root widget. window with a title bar provided by your window manager

w= Label(root, text="Hello World!")
#label widget, display text,icon, image
w.pack()
#size itself to contents, and make visible 
#(only once enter event loop can display)

root.mainloop()
#enter tkinter event loop, stay till close window.
#Handles user events, 
#windowing system(redraw evnts/window config msgs), 
#tkinter queued operations(geometry management(queued by pack), display updates)