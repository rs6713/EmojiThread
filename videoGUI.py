from Tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk
import httplib, urllib, base64
import json
import ast
#PIL is the Python Imaging Library
#The Image module provides a class with the same name which is used to represent a PIL image. 
#The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage objects from PIL images.
# The module also provides a number of factory functions, including functions to load images from files, and to create new images.

def sendFace(imgFace):
    
    #img.tobytes()
    #img=np.unpackbits(img)
    #print(img)
    imgFace=cv2.imencode('.png', imgFace)[1].tostring()
    #print(imgFace)
    #imgFace= base64.b64encode(imgFace)
    #print(imgFace)
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '967fba0ccc95407190ab8a7522a164ab',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        #'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion',
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, imgFace , headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        data=ast.literal_eval(data)
        #data=data.encode("ascii","replace")
        #data=json.loads(data)
        #data=data.encode("ascii","replace")
        print("Received response", data)
        rect=0
        emotion=""
        if(len(data)>0):
            #print(data[0])
            rect=data[0]['faceRectangle']
            #imageFrame.delete("all")
            
            emotions= data[0]['faceAttributes']['emotion'] 
            emotion=max(emotions.keys(), key=(lambda k: emotions[k]))
            print("Strongest emotion is:", emotion)
            #imageFrame.create_rectangle(rect['left'], rect['top'], rect['left']+rect['width'], rect['top']+rect['height'],outline="blue")
            #imageFrame.pack()
        conn.close()
        return (rect, emotion)
    except Exception as e:
        print("Error", e)
        #print("[Errno {0}]".format(e))

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
root.wm_title("Video Streaming Application")
root.config(background="#FFFFFF")

app = App(root)
imageFrame = Canvas(root, width=1200, height=1000)
imageFrame.config(background="#880022")
imageFrame.pack()
#w.pack()


cap = cv2.VideoCapture(0)

def drawFace(imageFrame, emotion, top, left):

    
    imageFrame.create_image(left, top, anchor=NW, image=emotion)#50,50, anchor="nw", top,left 

def show_frame(ct, faceRect, faceEmotion):
    ct+=1
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    #flip image captured and alter color

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)

    if(ct==5):
        #print("sending image")
        cv2.imwrite("hi.png", cv2image)
        cv2image=cv2.imread("hi.png")
        rect, emotion=sendFace(cv2image)
        if rect!=0:
            faceRect=rect
        if emotion!="":
            faceEmotion=emotion
            temp=cv2.imread( emotion+".png")    
            faceEmotion = Image.fromarray(temp)
            faceEmotion = ImageTk.PhotoImage(image=faceEmotion.resize((faceRect['width'],faceRect['height']), Image.ANTIALIAS))#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)

            #temp=Image.open(emotion+".png").convert('RGBA') 
            #faceEmotion = Image.fromarray(temp)
            #faceEmotion = ImageTk.PhotoImage(image=temp.resize((faceRect['width'],faceRect['height']), Image.ANTIALIAS))#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)
                
    if(ct==20):
        ct=0

    imageFrame.delete("all")
    #imageFrame.create_image(600,370,image=imgtk)
    imageFrame.create_image(0,0, anchor=NW, image=imgtk)#50,50, anchor="nw", 
    imageFrame.imgtk = imgtk
    if faceRect!=0:
        imageFrame.create_rectangle(faceRect['left'], faceRect['top'], faceRect['left']+faceRect['width'], faceRect['top']+faceRect['height'],outline="blue")
    if faceEmotion!="":
        drawFace(imageFrame,faceEmotion, faceRect['top'], faceRect['left'])
    
    #imageFrame.configure(image=imgtk)
    #imageFrame.create_image(50,50, anchor="nw", image=img)
    #imageFrame.create_image(50,50, anchor="nw", image=cv2image)
    #imageFrame.pack()

    imageFrame.after(50, show_frame, ct, faceRect, faceEmotion) 

    #lmain.imgtk = imgtk
    #lmain.configure(image=imgtk)
    #lmain.after(50, show_frame, ct) 

show_frame(0, 0, "")
root.mainloop() #runs till window exited/frame quitted
root.destroy() # optional;only needed under certain dev enviros, explicitly destroys main window
