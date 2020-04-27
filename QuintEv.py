from qiskit import *
import os
import random
import time
import numpy as np
import math
qc = QuantumCircuit(3,3)
vc = QuantumCircuit(3,3)#for visualization
sim_backend = BasicAer.get_backend('qasm_simulator')
statevec_backend = Aer.get_backend('statevector_simulator')
qubitNumber = 3
statevec = []
netInput = [0.000 for x in range(19)]
mystatevec = ["0+0i" for x in range(2**qubitNumber)]
mystatevec1 = [0.000 for x in range(2*2**qubitNumber)]
mystatevec1[0] = 1.0
mystatevec[0] = "1+0i"
vecExpectation = [0.000 for x in range(2**qubitNumber)]
vecExpectation[0] = 1.0
netExpectation = [0.000 for x in range(qubitNumber)]
Victory = 0
gweights0 = []
gweights1 = []
turn = 0
def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

class storageNet():
    def __init__(self, weights0, weights1, myid):
        self.weights0 = weights0[:]
        self.weights1 = weights1[:]
        self.id = myid
    def store(self, weights0, weights1):
        for x in range(len(weights0)):
            self.weights0[x] = weights0[x][:]
        for x in range(len(weights1)):
            self.weights1[x] = weights1[x][:]
    def transfer(self):
        global gweights0
        global gweights1
        gweights0 = self.weights0
        gweights1 = self.weights1
    def read(self):
        return self.weights0, self.weights1, self.id
    def load1(self):
        player1.load(self.weights0,self.weights1,self.id)
    def load2(self):
        player2.load(self.weights0,self.weights1,self.id)
    def mutate(self):
        self.weights0[math.floor(random.random()*19)][math.floor(random.random()*12)] += random.random()-.5
        self.weights1[math.floor(random.random()*12)][math.floor(random.random()*7)] += random.random()-.5
    def save(self):
        Memory = open(str(self.id)+".txt", "w+").close()
        Memory = open(str(self.id)+".txt", "w")
        Memory.write(str(self.weights0)+","+str(self.weights1))
        Memory.close()

class workerNet():
    def __init__(self, weights0, weights1, myid):
        self.weights0 = weights0
        self.weights1 = weights1
        self.id = myid
    def load(self, weights0, weights1, myid):
        self.weights0 = weights0
        self.weights1 = weights1
        self.id = myid
    def run(self, l0):
        l1 = nonlin(np.dot(l0,self.weights0))
        l2 = nonlin(np.dot(l1,self.weights1))
        return l2

def screen():
    os.system("cls")
    print("        _          ")
    print("   (P1)| | (0)     ")
    print("        I          ")
    print("       | | (1)     ")
    print("        I          ")
    print("   (P2)| | (2)     ")
    print("        -          ")
    print("(ex. H,1 CX,21 M,2)")
    print("(Op. X Y Z H CX M )")
    print("                   ")
    print("Net Expectation:    "+str(netExpectation))
    print("Vector Expectation: "+str(vecExpectation))
    print("Statevector:        "+str(mystatevec))
    print(vc)
    
def player1turn():
    global statevec
    global mystatevec1
    global vecExpectation
    global netExpectation
    global Victory
    if(player1.id==0):
        screen()
    netInput = [0.000 for x in range(19)]
    for x in range(3):
        netInput[x] = netExpectation[x]
    for x in range(16):
        netInput[x+3] = mystatevec1[x]
    move = player1.run(np.array(netInput))
    highest = 0
    index = 0
    for x in range(7):
        if(highest<move[x]):
            highest = move[x]
            index = x
    if(index == 0):
        qc.h(1)
        qc.barrier()
        vc.h(1)
        vc.barrier()
    elif(index == 1):
        qc.x(1)
        qc.barrier()
        vc.x(1)
        vc.barrier()
    elif(index == 2):
        qc.y(1)
        qc.barrier()
        vc.y(1)
        vc.barrier()
    elif(index == 3):
        qc.z(1)
        qc.barrier()
        vc.z(1)
        vc.barrier()
    elif(index == 4):
        qc.measure([1],[1])  
        qc.barrier()
        vc.measure([1],[1])  
        vc.barrier()
        statevec = execute(qc, statevec_backend, shots=1).result().get_statevector(qc)
        while(qc.data != []):
            qc.data.pop()
        qc.initialize(statevec,[x for x in range(qubitNumber)])
        real = statevec.real
        imag = statevec.imag
        vecExpectation = real[:]
        netExpectation = [0.000 for x in range(qubitNumber)]
        for x in range(len(vecExpectation)):
            vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
            mybinary = "{0:b}".format(x)
            while(len(list(mybinary))<qubitNumber):
                mybinary = "0"+mybinary
            mybinary = list(mybinary)
            mybinary.reverse()
            for y in range(qubitNumber):
                netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
    elif(index == 5):
        qc.measure([2],[2])  
        qc.barrier()
        vc.measure([2],[2])  
        vc.barrier()
        statevec = execute(qc, statevec_backend, shots=1).result().get_statevector(qc)
        while(qc.data != []):
            qc.data.pop()
        qc.initialize(statevec,[x for x in range(qubitNumber)])
        real = statevec.real
        imag = statevec.imag
        vecExpectation = real[:]
        netExpectation = [0.000 for x in range(qubitNumber)]
        for x in range(len(vecExpectation)):
            vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
            mybinary = "{0:b}".format(x)
            while(len(list(mybinary))<qubitNumber):
                mybinary = "0"+mybinary
            mybinary = list(mybinary)
            mybinary.reverse()
            for y in range(qubitNumber):
                netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
        if(netExpectation[2] == 1):
            Victory = 1
    elif(index == 6):
        qc.cx(1,2)
        qc.barrier()
        vc.cx(1,2)
        vc.barrier()
    statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
    real = statevec.real
    imag = statevec.imag
    vecExpectation = real[:]
    netExpectation = [0.000 for x in range(qubitNumber)]
    for x in range(len(vecExpectation)):
        vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
        mybinary = "{0:b}".format(x)
        while(len(list(mybinary))<qubitNumber):
            mybinary = "0"+mybinary
        mybinary = list(mybinary)
        mybinary.reverse()
        for y in range(qubitNumber):
            netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
    statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
    for x in range(len(statevec)):
        mystatevec[x] = str(round(real[x],3))+"+"+str(round(imag[x],3))+"i"
        mystatevec1[2*x] = round(real[x],3)
        mystatevec1[2*x+1] = round(imag[x],3)

def player2turn():
    global statevec
    global mystatevec1
    global vecExpectation
    global netExpectation
    global Victory
    if(player1.id==0):
        screen()
    netInput = [0.000 for x in range(19)]
    for x in range(3):
        netInput[x] = netExpectation[2-x]
    netInput[3] = mystatevec1[0]
    netInput[4] = mystatevec1[1]
    netInput[11] = mystatevec1[2]
    netInput[12] = mystatevec1[3]
    netInput[7] = mystatevec1[4]
    netInput[8] = mystatevec1[5]
    netInput[15] = mystatevec1[6]
    netInput[16] = mystatevec1[7]
    netInput[5] = mystatevec1[8]
    netInput[6] = mystatevec1[9]
    netInput[13] = mystatevec1[10]
    netInput[14] = mystatevec1[11]
    netInput[9] = mystatevec1[12]
    netInput[10] = mystatevec1[13]
    netInput[17] = mystatevec1[14]
    netInput[18] = mystatevec1[15]
    

    move = player2.run(np.array(netInput))
    highest = 0
    index = 0
    for x in range(7):
        if(highest<move[x]):
            highest = move[x]
            index = x
    if(index == 0):
        qc.h(1)
        qc.barrier()
        vc.h(1)
        vc.barrier()
    elif(index == 1):
        qc.x(1)
        qc.barrier()
        vc.x(1)
        vc.barrier()
    elif(index == 2):
        qc.y(1)
        qc.barrier()
        vc.y(1)
        vc.barrier()
    elif(index == 3):
        qc.z(1)
        qc.barrier()
        vc.z(1)
        vc.barrier()
    elif(index == 4):
        qc.measure([1],[1])  
        qc.barrier()
        vc.measure([1],[1])  
        vc.barrier()
        statevec = execute(qc, statevec_backend, shots=1).result().get_statevector(qc)
        while(qc.data != []):
            qc.data.pop()
        qc.initialize(statevec,[x for x in range(qubitNumber)])
        real = statevec.real
        imag = statevec.imag
        vecExpectation = real[:]
        netExpectation = [0.000 for x in range(qubitNumber)]
        for x in range(len(vecExpectation)):
            vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
            mybinary = "{0:b}".format(x)
            while(len(list(mybinary))<qubitNumber):
                mybinary = "0"+mybinary
            mybinary = list(mybinary)
            mybinary.reverse()
            for y in range(qubitNumber):
                netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
    elif(index == 5):
        qc.measure([0],[0])  
        qc.barrier()
        vc.measure([0],[0])  
        vc.barrier()
        statevec = execute(qc, statevec_backend, shots=1).result().get_statevector(qc)
        while(qc.data != []):
            qc.data.pop()
        qc.initialize(statevec,[x for x in range(qubitNumber)])
        real = statevec.real
        imag = statevec.imag
        vecExpectation = real[:]
        netExpectation = [0.000 for x in range(qubitNumber)]
        for x in range(len(vecExpectation)):
            vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
            mybinary = "{0:b}".format(x)
            while(len(list(mybinary))<qubitNumber):
                mybinary = "0"+mybinary
            mybinary = list(mybinary)
            mybinary.reverse()
            for y in range(qubitNumber):
                netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
        if(netExpectation[0] == 1):
            Victory = 2
    elif(index == 6):
        qc.cx(1,0)
        qc.barrier()
        vc.cx(1,0)
        vc.barrier()
    statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
    real = statevec.real
    imag = statevec.imag
    vecExpectation = real[:]
    netExpectation = [0.000 for x in range(qubitNumber)]
    for x in range(len(vecExpectation)):
        vecExpectation[x] = round(real[x]**2+imag[x]**2,3)
        mybinary = "{0:b}".format(x)
        while(len(list(mybinary))<qubitNumber):
            mybinary = "0"+mybinary
        mybinary = list(mybinary)
        mybinary.reverse()
        for y in range(qubitNumber):
            netExpectation[y] = round(netExpectation[y]+vecExpectation[x]*int(mybinary[y]),3)
    statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
    for x in range(len(statevec)):
        mystatevec[x] = str(round(real[x],3))+"+"+str(round(imag[x],3))+"i"
        mystatevec1[2*x] = round(real[x],3)
        mystatevec1[2*x+1] = round(imag[x],3)

def main():
    global gweights0
    global gweights1
    global Victory
    global mystatevec1
    global mystatevec
    global vecExpectation
    global netExpectation
    global statevec
    global turn
    for i in range(100):
        winners = [] 
        for x in range(50):    
            print("generation: "+str(i))
            print("match: "+str(x))
            vecExpectation = [0.000 for t in range(2**qubitNumber)]
            vecExpectation[0] = 1.0
            statevec = []
            netExpectation = [0.000 for t in range(qubitNumber)]
            mystatevec = ["0+0i" for t in range(2**qubitNumber)]
            mystatevec1 = [0.000 for t in range(2*2**qubitNumber)]
            mystatevec1[0] = 1.0
            mystatevec[0] = "1+0i"           
            gweights0 = []
            gweights1 = []
            turn = 0
            exec("a"+str(2*x)+".load1()")
            exec("a"+str(2*x+1)+".load2()")
            qc.h(1)
            qc.barrier()
            vc.h(1)
            vc.barrier()
            statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
            real = statevec.real
            imag = statevec.imag
            vecExpectation = real[:]
            netExpectation = [0.000 for t in range(qubitNumber)]
            for j in range(len(vecExpectation)):
                vecExpectation[j] = round(real[j]**2+imag[j]**2,3)
                mybinary = "{0:b}".format(j)
                while(len(list(mybinary))<qubitNumber):
                    mybinary = "0"+mybinary
                mybinary = list(mybinary)
                mybinary.reverse()
                for y in range(qubitNumber):
                    netExpectation[y] = round(netExpectation[y]+vecExpectation[j]*int(mybinary[y]),3)
            statevec = execute(qc,statevec_backend,shots=1).result().get_statevector(qc)
            for j in range(len(statevec)):
                mystatevec[j] = str(round(real[j],3))+"+"+str(round(imag[j],3))+"i"
                mystatevec1[2*j] = round(real[j],3)
                mystatevec1[2*j+1] = round(imag[j],3)
            while(Victory == 0):
                if(turn > 15):
                    Victory = 3
                player1turn()
                if(Victory == 0):
                    player2turn()
                    turn += 1
            if(Victory == 1):
                print("player1 wins!..............")
                winners.append(2*x)
                exec("a"+str(2*x)+".transfer()")
                exec("a"+str(100+x)+".store(gweights0,gweights1)")
                exec("a"+str(150+x)+".store(gweights0,gweights1)")
                for z in range(5):
                    exec("a"+str(150+x)+".mutate()")
            elif(Victory == 2):
                print("player2 wins!!!!!!!!!!!!!!!!!!!")
                winners.append(2*x+1)
                exec("a"+str(2*x+1)+".transfer()")
                exec("a"+str(100+x)+".store(gweights0,gweights1)")
                exec("a"+str(150+x)+".store(gweights0,gweights1)")
                for z in range(5):
                    exec("a"+str(150+x)+".mutate()")
            elif(Victory == 3):
                if(len(winners)>0 and math.floor(2*random.random())==1):
                    if(math.floor(random.random()*2)==1):
                        exec("a"+str(2*x)+".transfer()")
                        exec("a"+str(100+x)+".store(gweights0,gweights1)")
                        exec("a"+str(winners[math.floor(random.random()*len(winners))])+".transfer()")
                        exec("a"+str(150+x)+".store(gweights0,gweights1)")
                        for z in range(8):
                            exec("a"+str(100+x)+".mutate()")
                        for z in range(2):
                            exec("a"+str(150+x)+".mutate()")
                    else:
                        exec("a"+str(winners[math.floor(random.random()*len(winners))])+".transfer()")
                        exec("a"+str(100+x)+".store(gweights0,gweights1)")
                        exec("a"+str(2*x+1)+".transfer()")
                        exec("a"+str(150+x)+".store(gweights0,gweights1)")
                        for z in range(2):
                            exec("a"+str(100+x)+".mutate()")
                        for z in range(8):    
                            exec("a"+str(150+x)+".mutate()")
                else:
                    exec("a"+str(2*x)+".transfer()")
                    exec("a"+str(100+x)+".store(gweights0,gweights1)")
                    exec("a"+str(2*x+1)+".transfer()")
                    exec("a"+str(150+x)+".store(gweights0,gweights1)")
                    for z in range(8):
                        exec("a"+str(100+x)+".mutate()")
                        exec("a"+str(150+x)+".mutate()")

            while(qc.data != []):
                qc.data.pop()
            while(vc.data != []):
                vc.data.pop()
            Victory = 0
        for x in range(100):
            exec("a"+str(100+x)+".transfer()")
            exec("a"+str(x)+".store(gweights0,gweights1)")
random.seed(time.time())
for x in range(200):
    weightsa = 2*np.random.random((19,12))-1
    weightsb = 2*np.random.random((12,7))-1
    exec("a"+str(x)+" = storageNet(weightsa[:],weightsb[:],"+str(x)+")")
player1 = workerNet(0,0,0)
player2 = workerNet(0,0,0)
main()

for x in range(100):
    exec("a"+str(x)+".save()")
input("Results Saved: ")