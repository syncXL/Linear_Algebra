import tkinter  as tk
from tkinter import ttk
def tLabel(master,txt):
    return ttk.Label(master,text=txt)
def tEntry(master,txtVar,nCh,justF):
    return ttk.Entry(master,textvariable=txtVar,width=nCh,justify=justF)
def tFrame(master,coord):
    temp = ttk.Frame(master)
    temp.grid(row=coord[0],column=coord[1])
    return temp
def dispEqn(master,wid,coords):
    for i,j in enumerate(wid):
        tempF = tFrame(master,coords[i])
        tempEnt = tEntry(tempF,j[0],3,'right')
        tempLbl = tLabel(tempF,j[1])
        tempEnt.pack(side='left',anchor='nw')
        tempLbl.pack(side='left',anchor='nw')
def resetF(fName):
    for i in fName.winfo_children():
        i.destroy()
def conv(theVal):
    temp = []
    for i in theVal:
        temp.append(i.get())
    return temp
def conv_n_split(theList,row,column):
    tempR = []
    tempC = []
    theList = conv(theList)
    x = 0
    for i in range(row):
        for j in range(column):
            tempC.append(theList[x])
            x+=1
        tempR.append(tempC)
        tempC = []
    return tempR

def printer():
    print("Boo")
