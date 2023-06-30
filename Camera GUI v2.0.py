## Libraries
import matplotlib.pyplot as plt
import numpy as np
from instrumental.drivers.cameras import uc480
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk


## Variables
frame=0

## Functions & Start
def Start():
    # params
    cam.start_live_video(framerate = "10Hz")

    #Remove start buttons :
    Start_camera.destroy()
    Quit.destroy()

    #Take a picture button
    ttk.Button(frm, text="Take a picture", command=Take_a_picture).grid(column=0, row=1)

    #Exposure time input
    # Label(frm, text="Exposure time (ms) :").grid(column=0, row=3)
    global entry1
    entry1 = tk.Entry(root,bd=0)
    entry1.grid(column=2,row=0,sticky="nesw")
    entry1.insert(0,"10ms")

    #Zoom
    ttk.Button(frm, text="Zoom on a point (x,y)", command=Zoom).grid(column=0, row=3)
    Label(frm, text="x :").grid(column=0,row=5,rowspan=2)
    Label(frm, text="       y :").grid(column=1,row=5,rowspan=2)
    Label(frm, text="       Zoom width (in pixels)").grid(column=2,row=5, padx=40)
    global entryX, entryY, entryw
    entryX, entryY, entryw = tk.Entry(root), tk.Entry(root), tk.Entry(root)
    entryX.grid(column=0,row=6,rowspan=2, sticky="nesw")
    entryY.grid(column=1,row=6,rowspan=2, sticky="nesw")
    entryw.grid(column=2,row=6, sticky="nesw")h
    entryw.insert(0,"200")

def Take_a_picture():
    global frame
    expotime=entry1.get()
    frame = cam.grab_image(timeout='100s', copy=True, exposure_time=expotime)
    n,p=np.shape(frame)
    Label(frm, text="Width : "+str(n)+", Length : "+str(p)).grid(column=0, row=2)

    plt.imshow(frame)   #Inserts a new image

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()
    # #Load an image in the script
    # frame = cam.grab_image(timeout='100s', copy=True, exposure_time='10ms')
    #
    # picture = _photo_image(frame)
    # label = Label(image=picture)
    # label.image = picture# keep a reference!
    # label.grid()


def Zoom():

    if entryX.get()=="" or entryY.get()=="":
        print("Error : Input zoom coordonates")
    else :
        x = int(entryX.get())
        y = int(entryY.get())
        w = int(entryw.get())


        n,p=np.shape(frame)

        zframe=np.zeros((w,w))

        for i in range(w):
            for j in range(w):
                k=i+x-w//2
                l=j+y-w//2

                if k>=0 and k<n:
                    if l>=0 and l<p:
                        zframe[i,j]=frame[k,l]

        plt.close()
        plt.plot()
        plt.subplot(1,2,1)
        plt.imshow(frame)
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.subplot(1,2,2)
        plt.imshow(zframe)
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.show()



# init camera
instruments = uc480.list_instruments()

try:
    cam = uc480.UC480_Camera(instruments[0])
    root = tk.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    Label(frm, text="Python Thorcam GUI").grid(column=0, row=0)
    Quit=Button(frm, text="Quit", command=root.destroy)
    Start_camera=Button(frm, text="Start camera", command=Start)
    Quit.grid(column=10, row=1)
    Start_camera.grid(column=0, row=1)

    root.mainloop()

except Exception:
    print("Error : No Thorcam camera detected")