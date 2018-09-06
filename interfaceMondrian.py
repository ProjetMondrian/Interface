#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import os
import sys
from PIL import Image,ImageTk
import tkFileDialog
import imghdr

# 100 8 10

currentImage = 'firstPicture.jpg'

def putImage(imageName):
    img = Image.open(imageName)
    img.resize((500,500)).save("imageToPut.jpg")
    img = Image.open("imageToPut.jpg")
    result = ImageTk.PhotoImage(img)
    firstPanel.configure(image=result)
    firstPanel.image = result
    global currentImage
    currentImage = imageName

def getLineNumber():
    nb = nombreLignes.get()
    return nb

def getScale():
    sc = scale.get()
    return sc

def getLinemag():
    lm = linemag.get()
    return lm

def getOption():
    op = option.get(option.curselection())
    return op
    
def firstAlgorithm():
    nb = getLineNumber()
    sc = getScale()
    lm = getLinemag()
    op = getOption()
    function = 'Mondrian.py '
    syntax = function + currentImage + ' ' + nb + ' ' + sc + ' ' +lm + ' ' +op
    os.system(syntax)
    img = Image.open('FinalResult.jpg')
    img.resize((500,500),0).save('FinalResult2.jpg')
    img = Image.open('FinalResult2.jpg')
    result = ImageTk.PhotoImage(img)
    panel.configure(image=result)
    panel.image = result

def secondAlgorithm():
    function = 'Mondrian2.py '
    num = getNumColors()
    mc = getMColorState()
    syntax = function + currentImage + ' ' + num + ' ' + mc
    os.system(syntax)
    img = Image.open('FinalResult.jpg')
    img.resize((500,500),0).save('FinalResult2.jpg')
    img = Image.open('FinalResult2.jpg')
    result = ImageTk.PhotoImage(img)
    panel.configure(image=result)
    panel.image = result

def getNumColors():
    num = numColors.get()
    return num

def getMColorState():
    mc = varMC.get()
    if mc == 0:
        return 'False'
    else:
        return 'True'
    
def close_window(): 
    fenetre.destroy()
    os.remove("imageToPut.jpg")
    os.remove("FinalResult.jpg")
    os.remove("FinalResult2.jpg")

def selectImage():
    path = tkFileDialog.askopenfilename()
    imageType = imghdr.what(path)
    if imageType == "png":
        im = Image.open(path)
        rgb_im = im.convert('RGB')
        rgb_im.save('imageToPut.jpg')
        path = "imageToPut.jpg"
    global currentImage
    currentImage = path
    putImage(path)

def preset1():
    varNombreLignes.set("50")
    nombreLignes.config(textvariable = varNombreLignes)
    varLineMag.set("4")
    linemag.config(textvariable = varLineMag)
    varTxtScale.set("20")
    txtscale.config(textvariable = varTxtScale)
    return 0

def preset2():
    varNombreLignes.set("100")
    nombreLignes.config(textvariable = varNombreLignes)
    varLineMag.set("8")
    linemag.config(textvariable = varLineMag)
    varTxtScale.set("10")
    txtscale.config(textvariable = varTxtScale)
    return 0
 
fenetre = Tk()
label = Label(fenetre, text= "Projet Mondrian")
label.pack()

leftFrame = Frame(fenetre)
leftFrame.pack(side=LEFT,fill="both",expand=True)


rightFrame = Frame(fenetre)
rightFrame.pack(side=RIGHT,fill="both",expand=True)


# pannel

chosenImage = Image.open('selection2.jpg')
photo = ImageTk.PhotoImage(chosenImage)

firstPanel = Label(rightFrame, image = photo)
firstPanel.image = photo
firstPanel.pack(side = "left", fill = "both", expand = "yes")

chosenImage = Image.open('selection3.jpg')
photo = ImageTk.PhotoImage(chosenImage)

panel = Label(rightFrame, image = photo)
panel.image = photo
panel.pack(side = "right", fill = "both", expand = "yes")




# boutons

regionTop = Frame(leftFrame)
regionTop.pack(side=TOP,fill="both",expand=True)

region1 = Frame(regionTop)
region1.pack(side=TOP,fill="both",expand=True)

region1_2 = Frame(regionTop)
region1_2.pack(side=BOTTOM,fill="both",expand=True)

space = Label(region1,text="    ").pack(side=TOP)
space = Label(region1,text="    ").pack(side=TOP)
space = Label(region1,text="    ").pack(side=TOP)
space = Label(region1,text="    ").pack(side=TOP)
space = Label(region1,text="    ").pack(side=TOP)
space = Label(region1,text="    ").pack(side=TOP)

# Images

label2 = Label(region1,text = "IMAGE SELECTION", bg = 'white')
label2.pack()

space = Label(region1,text="    ").pack(side=TOP)

importImage = Button(region1, text="Import image", command = selectImage)
importImage.pack(side=TOP)

space = Label(region1,text="    ").pack(side=TOP)

space = Label(region1,text="                                                      ").pack(side=LEFT)

image1 = Button(region1, text = "Image 1", command= lambda name = 'firstPicture.jpg' : putImage(name))
image1.pack(side=LEFT)
space = Label(region1,text="    ").pack(side=LEFT)


image2 = Button(region1, text = "Image 2", command= lambda name = 'secondPicture.jpg' : putImage(name))
image2.pack(side=LEFT)
space = Label(region1,text="    ").pack(side=LEFT)

image3 = Button(region1, text = "Image 3", command= lambda name = 'thirdImage.jpg' : putImage(name))
image3.pack(side=LEFT)
space = Label(region1,text="    ").pack(side=LEFT)

image4 = Button(region1, text = "Image 4", command= lambda name = 'fourthImage.jpg' : putImage(name))
image4.pack(side=LEFT)
space = Label(region1,text="    ").pack(side=LEFT)

image5 = Button(region1, text = "Image 5", command= lambda name = 'fifthImage.jpg' : putImage(name))
image5.pack(side = LEFT)
space = Label(region1,text="    ").pack(side=LEFT)

image6 = Button(region1, text = "Image 6", command= lambda name = 'sixthImage.jpg' : putImage(name))
image6.pack(side = LEFT)
space = Label(region1,text="    ").pack(side=LEFT)


# Parametres

space = Label(region1_2,text="    ").pack(side=TOP)
space = Label(region1_2,text="    ").pack(side=TOP)
label3 = Label(region1_2,text = "PARAMETERS ALGO 1", bg = 'white')
label3.pack()

region1_2_1 = Frame(region1_2)
region1_2_1.pack(side = TOP,fill="both",expand=True)

region1_2_2 = Frame(region1_2)
region1_2_2.pack(side = BOTTOM,fill="both",expand=True)

space = Label(region1_2_1,text="    ").pack(side=TOP)

algo1Bouton = Button(region1_2_1, text="Preset 1", command= preset1)
algo1Bouton.pack(side=TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)

algo1Bouton = Button(region1_2_1, text="Preset 2", command= preset2)
algo1Bouton.pack(side=TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)
txtNombreLignes = Label(region1_2_1,text="Number of lines").pack(side=TOP)

varNombreLignes = StringVar(fenetre)
varNombreLignes.set("50")
nombreLignes = Spinbox(region1_2_1, from_= 10, to = 100, increment = 10, textvariable = varNombreLignes)
nombreLignes.pack(side = TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)
txtNombreLignes = Label(region1_2_1,text="Line magnetisme").pack(side=TOP)

varLineMag = StringVar(fenetre)
varLineMag.set("4")
linemag = Spinbox(region1_2_1, from_= 2, to = 8, increment = 1, textvariable = varLineMag)
linemag.pack(side = TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)
txtscale = Label(region1_2_1,text="Scale").pack(side=TOP)
varTxtScale = StringVar(fenetre)
varTxtScale.set("20")
scale = Spinbox(region1_2_1, from_= 10, to = 30, increment = 5, textvariable = varTxtScale)
scale.pack(side = TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)

space = Label(region1_2_1,text="Coloration").pack(side=TOP)

option = Listbox(region1_2_1, selectmode = BROWSE, height = 2)
option.insert(1, "mean")
option.insert(2, "numerous")
option.pack(side=TOP)
option.selection_set(first = 0)

space = Label(region1_2_1,text="    ").pack(side=TOP)

algo1Bouton = Button(region1_2_1, text="Start Algo 1", command= firstAlgorithm)
algo1Bouton.pack(side=TOP)

space = Label(region1_2_1,text="    ").pack(side=TOP)


#parameters algo 2
space = Label(region1_2_2,text="    ").pack(side=TOP)

parameters2 = Label(region1_2_2,text="PARAMETERS ALGO 2", bg = 'white').pack(side=TOP)

space = Label(region1_2_2,text="    ").pack(side=TOP)
txtscale = Label(region1_2_2,text="Number of colors").pack(side=TOP)
varNumColors = StringVar(fenetre)
varNumColors.set("5")
numColors = Spinbox(region1_2_2, from_= 5, to = 20, increment = 5, textvariable = varNumColors)
numColors.pack(side = TOP)

space = Label(region1_2_2,text="    ").pack(side=TOP)

varMC = IntVar()
mColor = Checkbutton(region1_2_2, text="Mondrian colors only", variable = varMC)
mColor.pack(side = TOP)

space = Label(region1_2_2,text="    ").pack(side=TOP)
algo1Bouton = Button(region1_2_2, text="Start Algo 2", command= secondAlgorithm)
algo1Bouton.pack(side=TOP)

space = Label(region1_2_2,text="    ").pack(side=TOP)
space = Label(region1_2_2,text="    ").pack(side=TOP)
algo1Bouton = Button(region1_2_2, text="Start Algo 3", command= secondAlgorithm)
algo1Bouton.pack(side=TOP)



# Algorithmes

region2 = Frame(leftFrame)
region2.pack(side=BOTTOM,fill="both",expand=True)

##label3 = Label(region2,text = "Parameters Algo 2")
##label3.pack()

space2 = Label(region2, text = "    ").pack(side=TOP)
space2 = Label(region2, text = "    ").pack(side=BOTTOM)

quitButton = Button(region2, text="Quit", command = close_window).pack(side=BOTTOM)

fenetre.overrideredirect(True)
fenetre.overrideredirect(False)
fenetre.attributes('-fullscreen',True)
fenetre.mainloop()
