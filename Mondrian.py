from PIL import Image
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import random
from operator import add
import sys
import os

sys.setrecursionlimit(1500)

#image_name = 'test9.jpg'
image_name = sys.argv[1]
scale = sys.argv[3]
scale = int(scale)

outputSize = (1000,1000)

line_mag = sys.argv[4]
line_mag = int(line_mag)

## We define here the number of lines that we want
#number_of_lines = 10
number_of_lines = sys.argv[2]
number_of_lines = int(number_of_lines)
# the number of lines must be even


'''

all the values above must be between 1 and 100, the bigger the value, the more pixelated it will be
resize = final size of picture
scale = the scale of the mondrian painting
cleanvalue = scale to cleanup ... doesnt really work
marge = how to compare colors for the cleanup, the bigger the better

'''


''' USEFUL FUNCTIONS '''

# transforms a list into a matrix 
def listToMatrix(alist,width,height):
    a = [[]] * height
    for i in range(height):
        a[i] = [[]] * width
    k = 0
    for i in range(0,height):
        for j in range(0,width):
            a[i][j] = alist[k]
            k = k +1
    return a




''' FUNCTIONS CREATED FOR THE ALGORITHM '''

# from the edge decomposition of an image, removes pixel's noise from resizing
def removeBlackWhiteImperfection(matrix,width,height):
    for i in range (0,height):
        for j in range (0, width):
            if matrix[i][j] > (100,100,100):
                matrix[i][j] = (255,255,255)
            else:
                matrix[i][j] = (0,0,0)
    return matrix

# gets the vertical distance between two black pixels 
def getLengthY(length,a,firstPoint):
    numrows = len(a)   
    if firstPoint[0] < numrows:
        if a[firstPoint[0]][firstPoint[1]] == (255,255,255):
            firstPoint[0] = firstPoint[0] + 1
            length = getLengthY(length + 1,a,firstPoint)
    return length

# gets the horizontal distance between two black pixels
def getLengthX(length,a,firstPoint):
    numcols = len(a[0])
    if firstPoint[1] < numcols:
        if a[firstPoint[0]][firstPoint[1]] == (255,255,255):
            firstPoint[1] = firstPoint[1] + 1
            length = getLengthX(length + 1,a, firstPoint)
    return length

# fills the white region of a picture
def fillBlanks(NoColorImage, ColorImage, width, height):
    imgToFill = Image.open(NoColorImage)
    imgOrigin = Image.open(ColorImage)
    pixelsNotColored = list(imgToFill.getdata())
    pixelsColored = list(imgOrigin.getdata())
    a = listToMatrix(pixelsColored,width,height)
    b = listToMatrix(pixelsNotColored,width,height)
    b = removeBlackWhiteImperfection(b,width,height)
    for i in range (0,(height)):
        for j in range (0,(width)):
            if b[i][j] == (255,255,255):
                firstPoint = [i,j]
                firstXPoint = [i,j]
                firstYPoint = [i,j]
                surfaceW = getLengthX(0,b,firstXPoint)
                surfaceH = getLengthY(0,b,firstYPoint)
                b = fillColor(a,b,firstPoint,surfaceH,surfaceW)            
    c = [0] * (width*height)
    index = 0 
    for i in range (0,height):
        for j in range (0, width):
            c[index] = b[i][j]
            index = index + 1
    return c

# fills color into a specific region
def fillColor(a,b,firstPoint,h,w):
    R = 0
    G = 0
    B = 0
    for i in range (firstPoint[0],h + firstPoint[0]):
        for j in range (firstPoint[1],w + firstPoint[1]):
            listToAdd = a[i][j]
            R = R + listToAdd[0]
            G = G + listToAdd[1]
            B = B + listToAdd[2]
    RGB = [R,G,B]
    RGB = np.array(RGB)
    newColor = RGB/(h*w)
    newColor = (newColor[0],newColor[1],newColor[2])

    for i in range (firstPoint[0],h + firstPoint[0]):
        for j in range (firstPoint[1],w + firstPoint[1]):
            b[i][j] = newColor
    return b



# gets the distance between 2 vertical black lines
def getFirstX(direction,matrix,value,line):
    numrows = len(matrix)
    if value < numrows and value > 0:
        if direction == "up" :
            if matrix[value][line] == 0 :
                value = getFirstX("up",matrix,value + 1,line)
            return value
        if direction == "down" :
            if matrix[value][line] == 0 :
                value = getFirstX("down",matrix,value - 1,line)
            return value
    else :
        return value

# get the distance between 2 horizontal black lines
def getFirstY(direction,matrix,value,line):
    numcols = len(matrix[0])
    if value < numcols and value > 0:
        if direction == "right" :
            if matrix[line][value] == 0 :
                value = getFirstY("right",matrix,value + 1,line)
            return value
        if direction == "left" :
            if matrix[line][value] == 0 :
                value = getFirstY("left",matrix,value - 1,line)
            return value
    else :
        return value 

# plots a horizontal line
def plot_horizontal(line_ed,xcoor,ycoor,realImage,blankImage,edges,w,h):
    ylen = len(ycoor)
    lineToDraw = np.argmax(line_ed)
    value = line_ed[lineToDraw]
    if ylen == 0 :
        # ( X , Y )
        firstPoint = (0,lineToDraw)      
        secondPoint = (width,lineToDraw)
        cv.line(realImage, firstPoint, secondPoint, (0,0,0),1)
        cv.line(blankImage, firstPoint, secondPoint, (0,0,0),1)
        
        line_ed[lineToDraw] = 0
        line_ed[lineToDraw + 1] = 0
        line_ed[lineToDraw - 1] = 0
        line_ed[lineToDraw + 2] = 0
        line_ed[lineToDraw - 2] = 0

        for i in range (0,width):
            ycoor.append((i,lineToDraw))
        
        return line_ed,ycoor,realImage,blankImage
    else:
        if value/255 > w/line_mag:
            firstPoint = (0,lineToDraw)
            secondPoint = (width,lineToDraw)
            cv.line(realImage, firstPoint, secondPoint, (0,0,0),1)
            cv.line(blankImage, firstPoint, secondPoint, (0,0,0),1)

            line_ed[lineToDraw] = 0
            line_ed[lineToDraw + 1] = 0
            line_ed[lineToDraw - 1] = 0
            line_ed[lineToDraw + 2] = 0
            line_ed[lineToDraw - 2] = 0

            for i in range (0,width):
                ycoor.append((i,lineToDraw))
            
            return line_ed,ycoor,realImage,blankImage

        else :
            leftY = getFirstY("right",edges,0,lineToDraw)
            rightY = getFirstY("left",edges,w-1,lineToDraw)

            listY = []
            for a in range (0,len(xcoor)):
                if xcoor[a][1] == lineToDraw :
                    listY.append(xcoor[a][0])
            
            leftY = min(listY, key=lambda x:abs(x-leftY))
            rightY = min(listY, key=lambda x:abs(x-rightY))
            
            approxFirstPoint = (leftY,lineToDraw)
            approxSecondPoint = (rightY,lineToDraw)
            cv.line(realImage, approxFirstPoint, approxSecondPoint, (0,0,0),1)
            cv.line(blankImage, approxFirstPoint, approxSecondPoint, (0,0,0),1)

            line_ed[lineToDraw] = 0
            line_ed[lineToDraw + 1] = 0
            line_ed[lineToDraw - 1] = 0
            line_ed[lineToDraw + 2] = 0
            line_ed[lineToDraw - 2] = 0

            for i in range (leftY,rightY):
                ycoor.append((i,lineToDraw))
            
            return line_ed,ycoor,realImage,blankImage

# plots a vertical line
def plot_vertical(column_ed,xcoor,ycoor,realImage,blankImage,edges,w,h):
    xlen = len(xcoor)
    lineToDraw = np.argmax(column_ed)
    value = column_ed[lineToDraw]
    if xlen == 0 :
        # ( X , Y )
        firstPoint = (lineToDraw,0)      
        secondPoint = (lineToDraw,height)
        cv.line(realImage, firstPoint, secondPoint, (0,0,0),1)
        cv.line(blankImage, firstPoint, secondPoint, (0,0,0),1)

        column_ed[lineToDraw] = 0
        column_ed[lineToDraw + 1] = 0
        column_ed[lineToDraw - 1] = 0
        column_ed[lineToDraw + 2] = 0
        column_ed[lineToDraw - 2] = 0

        for j in range (0,height): ##maybe height + 1
            xcoor.append((lineToDraw,j))
            
        return column_ed,xcoor,realImage,blankImage
    else:
        if value/255 > h/line_mag:
            firstPoint = (lineToDraw,0)
            secondPoint = (lineToDraw,height)
            cv.line(realImage, firstPoint, secondPoint, (0,0,0),1)
            cv.line(blankImage, firstPoint, secondPoint, (0,0,0),1)

            column_ed[lineToDraw] = 0
            column_ed[lineToDraw + 1] = 0
            column_ed[lineToDraw - 1] = 0
            column_ed[lineToDraw + 2] = 0
            column_ed[lineToDraw - 2] = 0

            for j in range (0,height):
                xcoor.append((lineToDraw,j))
            
            return column_ed,xcoor,realImage,blankImage

        else :
            downX = getFirstX("up",edges,0,lineToDraw)
            upX = getFirstX("down",edges,h-1,lineToDraw)

            listX = []
            for a in range (0,len(ycoor)):
                if ycoor[a][0] == lineToDraw :
                    listX.append(ycoor[a][1])
                    
            downX = min(listX, key=lambda x:abs(x-downX))
            upX = min(listX, key=lambda x:abs(x-upX))
            
            approxFirstPoint = (lineToDraw,downX)
            approxSecondPoint = (lineToDraw,upX)
            cv.line(realImage, approxFirstPoint, approxSecondPoint, (0,0,0),1)
            cv.line(blankImage, approxFirstPoint, approxSecondPoint, (0,0,0),1)

            column_ed[lineToDraw] = 0
            column_ed[lineToDraw + 1] = 0
            column_ed[lineToDraw - 1] = 0
            column_ed[lineToDraw + 2] = 0
            column_ed[lineToDraw - 2] = 0

            for j in range (downX,upX):
                xcoor.append((lineToDraw,j))
                
            return column_ed,xcoor,realImage,blankImage





''' Program '''

## Selection of the image
img = Image.open(image_name)
img.save("ImageToWorkWith.jpg")
img = Image.open("ImageToWorkWith.jpg")
originalWidth, originalHeight = img.size


## We define the height and the width so that the algorithme doesnt have too many pixels to work with
width = originalWidth/scale
height = originalHeight/scale
img.resize((width,height)).save("LessPixelsImage.jpg")


imgblank = np.zeros([height,width,3],dtype=np.uint8)
imgblank.fill(255)
cv.imwrite("blank.jpg",imgblank)



## We use the image with less pixels
img = Image.open("LessPixelsImage.jpg")



## We get the RGB decomposition of each pixels into an array
pixels = list(img.getdata())



## We remove black pixels to not get errors with contour
for i in range (0,len(pixels)):
    if pixels[i][0] < 20 and pixels[i][1] < 20 and pixels[2] < 20:
        pixels[i] = (20,20,20)
img.putdata(pixels)
img.save("LessPixelsImageWithoutBlack.jpg")
img = Image.open("LessPixelsImageWithoutBlack.jpg")
pixels = list(img.getdata())



## Since all RGB values are in an array, we will put them inside a matrix  so that it will be easier to manipulate them

a = listToMatrix(pixels,width,height)

"""
Some examples to verify the indexes
print(a[0][0])
print(pixels[0])
print(a[1][0])
print(pixels[50])
print(a[49][49])
print(pixels[2499])
"""


## We extract inside an array the edges of the image
imgingray = cv.imread("LessPixelsImageWithoutBlack.jpg",0)
img = cv.imread("LessPixelsImageWithoutBlack.jpg")
edges = cv.Canny(imgingray,100,200)




## For each line of pixels, we look where are the principals edges
line_ed = [0] * (height)
for i in range(0,height-1):
    line_ed[i] = np.sum(edges[i])



## For each column of pixels, we look where are the principals edges
column_ed = [0] * (width)
for j in range(0,width-1):
    somme = 0
    for i in range(0,height-1):
        somme = somme + edges[i][j]
    column_ed[j] = somme


ycoor = []
xcoor = []

## We put 0 in line_ed so that there wont be a horizontal line at the edge of the painting
line_ed[0] = 0
line_ed[1] = 0
line_ed[height-1] = 0
line_ed[height-2] = 0

## We put 0 in column_ed so that there wont be a vertical line at the edge of the painting
column_ed[0] = 0
column_ed[1] = 0
column_ed[width-1] = 0
column_ed[width-2] = 0
iteration = 0

while iteration < number_of_lines:
    if iteration%2 == 0 : 
        line_ed,ycoor,img,imgblank = plot_horizontal(line_ed,xcoor,ycoor,img,imgblank,edges,width,height)
    else :
        column_ed,xcoor,img,imgblank = plot_vertical(column_ed,xcoor,ycoor,img,imgblank,edges,width,height)
    iteration = iteration + 1

cv.imwrite("TemporaryResult.jpg",img)
cv.imwrite("blank.jpg",imgblank)

##cv.imread("superposition.jpg")       
##cv.imwrite("superposition.jpg",img)

resultatList = fillBlanks("blank.jpg", "LessPixelsImageWithoutBlack.jpg", width, height)
img = Image.open("TemporaryResult.jpg")
img.putdata(resultatList)
img = img.resize(outputSize, 0)
img.save("FinalResult.jpg")

os.remove("ImageToWorkWith.jpg")
os.remove("LessPixelsImage.jpg")
os.remove("blank.jpg")
os.remove("LessPixelsImageWithoutBlack.jpg")
os.remove("TemporaryResult.jpg")

