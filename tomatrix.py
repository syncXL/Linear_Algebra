import tkinter as tk
import  numpy as np
from gaussian import Guassian
from general import *
from layout  import *
from tkinter import ttk
subscripts = ['\u2080','\u2081','\u2082','\u2083','\u2084','\u2085','\u2086','\u2087','\u2088','\u2089']
gClass = Guassian()
def addEquator(param,eqn):
    return param,eqn
def returnSub(val):
    global subscripts
    returnedVal = ""
    for i in val:
        returnedVal += subscripts[int(i)]
    return returnedVal
def labeller(numofParam):
    value = []
    for i in range(1,numofParam+1):
        value.append(f"x{returnSub(str(i))} +") if i != numofParam else value.append(f"x{returnSub(str(i))} =")
    
    return value
def returnCoords(rows,column,stY=0):
    combs = []
    for i in range(1,rows+1):
        for k in range(stY,column):
            combs.append([i,k])
    return combs
def useStyle():
    styler = ttk.Style()
    styler.theme_use('default')
    styler.configure('TEntry',width=5)
def gridFrame(master,r,c):
    tFrame = ttk.Frame(master,width=500,height=250)
    tFrame.pack(side="top", fill="x", anchor="nw",expand=True)
    return tFrame
def  gridConfig(tFrame,r,c,val):
    loopAction(r+1,lambda i:tFrame.grid_rowconfigure(i,weight=val))
    loopAction(c+1,lambda i:tFrame.grid_columnconfigure(i,weight=val))
def gridButton(master,txt,commnd):
    return ttk.Button(master,text=txt,command=commnd)
def structure(row,column):
    struct = [tk.IntVar() for i in range(row*column)]
    return struct
def grider(master,pairedWid,coord):
    temp=ttk.Frame(master)
    temp.grid(row=coord[0],column=coord[1])
    for i in pairedWid:
        i.pack(side='left',anchor='nw')
def placer(wid,coord):
    if len(coord)==2:
        wid.grid(row=coord[0],column=coord[1],sticky='nw')
    elif len(coord) == 3:
        wid.grid(row=coord[0],column=coord[1],rowspan=coord[2],sticky='w')
    else:
        wid.grid(row=coord[0],column=coord[1],columnspan=coord[3],sticky='w')
def displayer(master,widgets,coords):
    for i,j in enumerate(widgets):
        if not isinstance(j,list):
            placer(j,coords[i])
        else:
            grider(master,j,coords[i])
def sametxt_diffLbl(num,theTxt,master):
    tempL = []
    for i in range(num):
        for j in theTxt:
            tempL.append(tLabel(master,j))
    return tempL
def multiplier(theL,num):
    tempL = theL.copy()
    for i in range(num):
        theL.extend(tempL)
    return theL
def add_remove_reset(addRem,rCol):
    global defParam,defEqn,labels,coefficients,values,solveEqn,allVal
    if rCol:
        defParam = defParam + 1 if addRem else defParam - 1
    else:
        defEqn = defEqn + 1 if addRem else defEqn - 1
        values = structure(1,defEqn)
    labels = wid()
    coefficients = replaceList(structure(defEqn,defParam),coefficients)
    allVal = intertwine(coefficients,values,defParam)
    resetF(QFrame)
    solveEqn = ttk.Button(QFrame,text="Solve Equation",command=lambda:tomatrix(allVal))
    disp_qFrame()
def wid():
    global defParam,defEqn
    labels = multiplier(labeller(defParam),defEqn-1)
    return labels
def limCheck(theButts,theLimits,theTypes):
    global defEqn,defParam
    limits = [defEqn,defParam]
    for i,j in enumerate(theButts):
        if theLimits[i] == limits[theTypes[i]]:
            j.configure(state="disabled")
def getVal():
    global coefficients,solveEqn 
    for i in coefficients:
        try:
            i.get()
            solveEqn.configure(state='active')
        except tk.TclError:
            solveEqn.configure(state='disabled')
            break
    QFrame.after(1000,getVal)
def tomatrix(val):
    global gClass
    theMatrix = np.array(conv_n_split(val,defEqn,defParam+1),dtype=float)
    gClass.changeEqn(theMatrix)
    global theSolution
    theSolution = gClass.solve()
    for i in theSolution:
        print(i,end="\n\n")
    disp_ansFrame()
def disp_qFrame():
    global solveEqn
    addParam = gridButton(QFrame,"Add Parameter",lambda:add_remove_reset(1,1))
    remParam = gridButton(QFrame,"Remove Parameter",lambda:add_remove_reset(0,1))
    addParam.grid(row=0,column=0,columnspan=2,sticky='w')
    remParam.grid(row=0,column=3,columnspan=2)
    addEqn = gridButton(QFrame,"Add Equation",lambda:add_remove_reset(1,0))
    remEqn = gridButton(QFrame,"Remove Equation",lambda:add_remove_reset(0,0))
    val_wid_n_coord = [[tEntry(QFrame,i,3,'right') for i in values],returnCoords(defEqn,defParam+1,defParam)]
    coeff_n_label = pairList(coefficients,labels)
    all_q_coord = returnCoords(defEqn,defParam)
    dispEqn(QFrame,coeff_n_label,all_q_coord)
    displayer(QFrame,val_wid_n_coord[0],val_wid_n_coord[1])
    addEqn.grid(row=defEqn+1,column=0,columnspan=2,sticky='w')
    remEqn.grid(row=defEqn+1,column=3,columnspan=2)
    solveEqn.grid(row=defEqn+2,column=0,rowspan=defParam)
    limCheck([addParam,remParam,addEqn,remEqn],[10,2,10,2],[1,1,0,0])

def disp_ansFrame():
    global labels,AnsFrame
    for i in labels:
        ttk.Label(AnsFrame,text=i).pack(side='top',anchor="nw")




defParam,defEqn = addEquator(2,2)
labels = wid()
root = tk.Tk()
root.geometry('500x500')
root.resizable(False,False)
useStyle()
QFrame = gridFrame(root,0,0)
AnsFrame = gridFrame(root,1,0)
coefficients = structure(defEqn,defParam)
values = structure(1,defEqn)
allVal = intertwine(coefficients,values,defParam)
solveEqn = ttk.Button(QFrame,text="Solve Equation",command=lambda:tomatrix(allVal))
disp_qFrame()
getVal()
root.mainloop()