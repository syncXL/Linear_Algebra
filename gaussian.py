import numpy as np
import time
from general import subscripts
class Guassian:
    def __init__(self):
        pass
    def changeEqn(self,eqn):
        self.eqn = eqn
        self.pivR,self.pivC = 0,0
        self.allPivC = []
        self.defaultPiv = [(i,i) for i in range(eqn.shape[1]-1)]
        self.identity = np.eye(self.eqn.shape[0],dtype= float)
        self.xVal = ["x" + subscripts[i] for i in range(1,eqn.shape[1])]
        self.ref = False
    def isPivot(self,row,col):
        temp = list(self.eqn[row:,col])
        filtL = self.filterL(temp)
        return self.interPret(temp,filtL,row)
    def interPret(self,theL,filtL,indLim):
        if len(filtL) == 0:
            return -1,True
        elif len(filtL) == 1:
            return theL.index(min(filtL))+indLim,True
        else:
            if 1 in theL:
                return theL.index(1) +indLim,False
            elif -1 in theL:
                return theL.index(-1) +indLim,False
            else:
                return theL.index(min(filtL)) + indLim,False
    def filterL(self,theL):
        returnP = []
        for i in theL:
            if i != 0:
                returnP.append(i)
        return returnP
    def makePivot(self):
        for i,j in enumerate(self.eqn):
            if i > self.pivR:
                self.identity[i] = (self.eqn[self.pivR][self.pivC] *self.identity[i]) - (self.eqn[i][self.pivC] * self.identity[self.pivR])
                self.eqn[i] = (self.eqn[self.pivR][self.pivC] * j) - (self.eqn[i][self.pivC] *self.eqn[self.pivR])
    def getPiv(self):
        getP ,pBool= self.isPivot(self.pivR,self.pivC)
        # print(f"gtP {getP},{pBool}")
        if getP == -1:
            self.pivC +=1
            if self.pivC < (self.eqn.shape[1]-1):
                self.getPiv()
            else:
                self.moveRow(getP,pBool)
        else:
            self.allPivC.append((self.pivR,self.pivC))
            self.moveRow(getP,pBool)
    def increasePiv(self):
        self.pivR = self.pivR + 1 if self.pivR <= self.eqn.shape[0] else self.pivR
        self.pivC = self.pivC + 1 if self.pivC < (self.eqn.shape[1] -1) else self.pivC
    def moveRow(self,getP,pBool):
        if self.pivR != getP or getP == -1:
            temp,tempIdn = self.eqn[getP].copy(),self.identity[getP].copy()
            self.eqn[getP],self.identity[getP] = self.eqn[self.pivR],self.identity[self.pivR]
            self.eqn[self.pivR],self.identity[self.pivR] = temp,tempIdn
        if pBool:
            self.increasePiv()
        else:
            self.makePivot()
            self.increasePiv()
    def solve_ref(self):
        while not self.ref:
            self.getPiv()
            # print(min(self.eqn.shape),self.pivC)
            if len(self.allPivC) == min(self.eqn.shape) or self.pivC == len(self.eqn[0])-1:
                self.ref = True
            # print(self.eqn)
        self.InRef = self.eqn.copy()
    def get_rref(self):
        self.nonZero = []
        for i in self.allPivC:
            cols = self.eqn[:,i[1]].copy()
            temp = []
            for j in range(len(cols)):
                if cols[j] != 0 and j != i[0]:
                    temp.append(j)
            self.nonZero.append(temp)
        # print(self.nonZero)
    def divCoeff(self):
        for i,j in enumerate(self.allPivC):
            if self.eqn[j[0]][j[1]] != 1:
                self.identity[j[0]] = self.identity[j[0]] / self.eqn[j[0]][j[1]]
                self.eqn[j[0]] = self.eqn[j[0]] / self.eqn[j[0]][j[1]]
    def row_reduce(self):
        rev_All_Piv = self.allPivC[::-1]
        rev_non_zero = self.nonZero[::-1]
        for i,j in enumerate(rev_All_Piv):
            for k in rev_non_zero[i]:
                self.identity[k] = (self.eqn[j[0]][j[1]] * self.identity[k]) - (self.eqn[k][j[1]] * self.identity[j[0]])
                self.eqn[k] = (self.eqn[j[0]][j[1]] * self.eqn[k]) - (self.eqn[k][j[1]] * self.eqn[j[0]])
    def solve_rref(self):
        self.get_rref()
        self.row_reduce()
        self.divCoeff()
    def solve(self):
        self.solve_ref()
        # print(self.allPivC)
        self.solve_rref()
        self.filterV()
        return self.beautify()
    def filterV(self):
        pointer = 0
        freeIndex = []
        self.solution = []
        noSolBool = True
        setofsol = [self.eqn[:,-1]]
        self.basicV = []
        for i in self.eqn:
            lastVal = self.filterL(i)
            if len(lastVal) == 1 and lastVal[-1] == i[-1]:
                self.solution = "No Solution"
                noSolBool = False
        if noSolBool:
            for i in range(self.eqn.shape[1]-1):
                if len(self.allPivC) != pointer and self.allPivC[pointer][1] == i:
                    self.basicV.append(True)
                    pointer+=1
                else:
                    self.basicV.append(False)
                    temp = -1 * self.eqn[:,i]
                    setofsol.append(temp)
                    freeIndex.append(i)
            for i,j in enumerate(setofsol):
                self.solution.append(self.getSolution(j)) if i == 0 else self.solution.append(self.getSolution(j,freeIndex[i-1]))
            self.solution = np.array(self.solution).transpose()
    def getSolution(self,answer,tAns=-1):
        pointer = 0
        self.theSol = []
        for i,j in enumerate(self.basicV):
            if j:
                self.theSol.append(answer[pointer])
                pointer +=1
            else:
                self.theSol.append(1) if i == tAns else self.theSol.append(0)
        return self.theSol
    def beautify(self):
        if isinstance(self.solution,str):
            return f"{self.InRef},\n\n{self.eqn},\n\nNo Solution,\n\nLinear Dependent,\n\nNo Identity"
        else:
            self.solInText = f"{self.solution[:,0].transpose()}"
            pointer = 1
            linInd =True
            for i,j in enumerate(self.basicV):
                if not j:
                    self.solInText += f" + {self.xVal[i]}{self.solution[:,pointer].transpose()}"
                    linInd = False
                    self.identity = "No identity"
                    pointer+=1
            return f"{self.InRef}\n\n,\n\n{self.eqn},\n\n{self.solInText},\n\n{linInd},\n\n{self.identity}"

x = np.array([[5,-1,2,7],
              [-2,6,9,0],
              [-7,5,-3,-7]],dtype=float)
# y = np.array([[-9,-5],[3,11,-1]],dtype=float)
theAns = Guassian()
theAns.changeEqn(x)
print(theAns.solve())
# XiNV =  theAns.identity
# print(XiNV)


# start = time.perf_counter()

# print(time.perf_counter()-start)
