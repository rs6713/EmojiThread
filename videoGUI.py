from Tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk
import httplib, urllib, base64
import json
import ast
from threading import Thread
from Queue import Queue
#PIL is the Python Imaging Library
#The Image module provides a class with the same name which is used to represent a PIL image. 
#The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage objects from PIL images.
# The module also provides a number of factory functions, including functions to load images from files, and to create new images.

        
        
def sendFace():
    global currentRect, currentEmotion, emotionPics
    while True:   
        #img.tobytes()
        #img=np.unpackbits(img)
        #print(img)
        print("Threaded sending face")
        imgFace = q.get()
        q.task_done()
        print("Got queue item")
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
                currentRect=[]
                currentEmotion=[]
                for res in data:
                    #print(data[0])
                    rect=res['faceRectangle']
                    #imageFrame.delete("all")
                    
                    emotions= res['faceAttributes']['emotion'] 

                    currentEmotion.append(max(emotions.keys(), key=(lambda k: emotions[k])))
                    print("Strongest emotion is:", currentEmotion)
                    #imageFrame.create_rectangle(rect['left'], rect['top'], rect['left']+rect['width'], rect['top']+rect['height'],outline="blue")
                    #imageFrame.pack()

                    currentRect.append(rect)
                    
                    print("Saying task complete")
            
            conn.close()
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
        print ("hi there, everyone!")

root = Tk()
root.wm_title("Video Streaming Application")
root.config(background="#FFFFFF")

app = App(root)
imageFrame = Canvas(root, width=1200, height=1000)
imageFrame.config(background="#880022")
imageFrame.pack()
#w.pack()

emotionsAvail=["neutral","happiness", "sadness", "surprise" , "contempt","disgust", "anger", "fear"]
#"happiness", "sadness", "surprise", , "contempt","disgust", "anger", "fear"
def loadEmotions():
    result={}
    for e in emotionsAvail:
        temp= e+".gif"
        c=Image.open(temp)
        #temp=temp.resize((300,300))#, Image.ANTIALIAS

        #temp=cv2.imread(temp)
        #temp=Image.open(temp).resize((300,300))    
        #faceEmotion = Image.fromarray(temp)

        #currentEmotion= ImageTk.PhotoImage(image=temp.resize((300,300),Image.ANTIALIAS ) )
        result[e]=c

        #temp = ImageTk.PhotoImage(file=temp)
        #result[e]=temp

        #result[e]= PhotoImage(file=temp)

        #result[e] = PhotoImage(Image.open(temp) )
        #result[e]=cv2.imread( e+".png")    
    return result

#Load emotion images

emotionPics= loadEmotions()
print(emotionPics)


currentEmotion=[]
currentRect=[]
cap = cv2.VideoCapture(0)
concurrent=50
q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=sendFace)
    t.daemon = True
    t.start()

def drawFace(imageFrame, emotion, top, left):

    imageFrame.create_image(left, top, anchor=NW, image=emotion)#50,50, anchor="nw", top,left 

def show_frame(ct):
    
    global emotionPics, currentEmotion, currentRect

    ct+=1
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    #flip image captured and alter color

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)

    if(ct==5):
        #print("sending image")
        #cv2.imwrite("hi.png", cv2image)
        #cv2image=cv2.imread("hi.png")
        try:
            q.put(cv2image)
            q.join()
        except KeyboardInterrupt:
            sys.exit(1)
        #rect, emotion=sendFace(cv2image)
        #if rect!=0:
        #    faceRect=rect
        #if emotion!="":
            #faceEmotion=emotion


            #temp=cv2.imread( emotion+".png")    
            #faceEmotion = Image.fromarray(temp)
            # currentEmotion= ImageTk.PhotoImage(image=faceEmotion)
            
            
            #currentEmotion = ImageTk.PhotoImage(file=emotion+".png")
            
            #faceEmotion = Image.fromarray(temp)
            #faceEmotion = ImageTk.PhotoImage(image=faceEmotion.resize((faceRect['width'],faceRect['height']), Image.ANTIALIAS))#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)
            #print("Resizing image from", temp.width(), temp.height(), " to: ", faceRect['width'], faceRect['height'])

            #faceEmotion=temp
            #faceEmotion=temp.zoom(faceRect['width']/ temp.width() ,faceRect['height']/temp.height() )
            #faceEmotion=temp.resize((faceRect['width'],faceRect['height']), Image.ANTIALIAS)
            
            #temp=Image.open(emotion+".png").convert('RGBA') 
            #faceEmotion = Image.fromarray(temp)
            #faceEmotion = ImageTk.PhotoImage(image=temp.resize((faceRect['width'],faceRect['height']), Image.ANTIALIAS))#.resize((1200,1000), Image.ANTIALIAS).resize((1200,1000), Image.ANTIALIAS)
                
    if(ct==10):
        ct=0

    imageFrame.delete("all")
    #imageFrame.create_image(600,370,image=imgtk)
    imageFrame.create_image(0,0, anchor=NW, image=imgtk)#50,50, anchor="nw", 
    imageFrame.imgtk = imgtk
   
    for i in range(len(currentRect)):
        #imageFrame.create_rectangle(currentRect[i]['left'], currentRect[i]['top'], currentRect[i]['left']+currentRect[i]['width'], currentRect[i]['top']+currentRect[i]['height'],outline="blue")
        
        if(isinstance(currentEmotion[i], basestring)):
            newCurrentEmotion=[]
            for u in range(len(currentRect)):
                curr=emotionPics[currentEmotion[u]]
                curr=ImageTk.PhotoImage(image=curr.resize((currentRect[u]['width'],currentRect[u]['height']),Image.ANTIALIAS ) )
                newCurrentEmotion.append(curr)
            currentEmotion=newCurrentEmotion

        #print("Create emoticon image",currentRect['left'], currentRect['top'], currentEmotion, currentEmotion.height() )
        imageFrame.create_image(currentRect[i]['left'], currentRect[i]['top'], anchor=NW, image=currentEmotion[i])#faceRect['left'], faceRect['top']
        imageFrame.currentEmotion=currentEmotion[i]
        imageFrame.image=currentEmotion[i]
        #drawFace(imageFrame,faceEmotion, faceRect['top'], faceRect['left'])
    
    #imageFrame.configure(image=imgtk)
    #imageFrame.create_image(50,50, anchor="nw", image=img)
    #imageFrame.create_image(50,50, anchor="nw", image=cv2image)
    #imageFrame.pack()

    imageFrame.after(50, show_frame, ct) 

    #lmain.imgtk = imgtk
    #lmain.configure(image=imgtk)
    #lmain.after(50, show_frame, ct) 

show_frame(0)
root.mainloop() #runs till window exited/frame quitted
root.destroy() # optional;only needed under certain dev enviros, explicitly destroys main window
