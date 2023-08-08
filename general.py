subscripts = ['\u2080','\u2081','\u2082','\u2083','\u2084','\u2085','\u2086','\u2087','\u2088','\u2089']
def loopAction(num,cmd):
    for i in range(num):
        cmd(i)
def maxlen(theList):
    lenOfList = [len(i) for i in theList]
    return(max(lenOfList))
def intertwine(fList,sList,stage):
    temp = fList.copy()
    nT =1
    for i in range(len(sList)):
        ind = (stage *nT) + i
        temp.insert(ind,sList[i])
        nT +=1
    return temp
def pairList(*theList):
    theList = list(theList)
    pairedList = []
    mLen = maxlen(theList)
    for i in range(mLen):
        tempL = []
        for j in theList:
            try:
                tempL.append(j[i])
            except IndexError:
                pass
        pairedList.append(tempL)
    return pairedList
def replaceList(list1,replacedL):
    for i in range(len(list1)):
        try:
            list1[i] = replacedL[i]
        except IndexError:
            break
    return list1

def copyL(n,val):
    tempL = val[0]
    for i in range(n):
        val.append(tempL)
    return val
