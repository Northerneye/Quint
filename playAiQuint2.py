from qiskit import *
import os
import numpy as np
qubitNumber = 4
qc = QuantumCircuit(qubitNumber,qubitNumber)
vc = QuantumCircuit(qubitNumber,qubitNumber)#for visualization
sim_backend = BasicAer.get_backend('qasm_simulator')
statevec_backend = Aer.get_backend('statevector_simulator')
statevec = []
mystatevec = ["0+0i" for x in range(2**qubitNumber)]
mystatevec[0] = "1+0i"
mystatevec1 = [0.000 for x in range(2*2**qubitNumber)]
mystatevec1[0] = 1.0
vecExpectation = [0.000 for x in range(2**qubitNumber)]
vecExpectation[0] = 1
netExpectation = [0.000 for x in range(qubitNumber)]
Victory = 0

def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

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
    print("(ex. H,1 CX,12 M,2)")
    print("(Op. X Y Z H CX M )")
    print("                   ")
    print("Net Expectation:    "+str(netExpectation))
    print("Vector Expectation: "+str(vecExpectation))
    print("Statevector:        "+str(mystatevec))
    print(vc)
   
def player1turn():
    global statevec
    global vecExpectation
    global netExpectation
    global Victory
    screen()
    flag1 = True
    flag2 = True
    while(flag1 or flag2):
        operation = input("Player 1 Operation(ex. H): ")
        qbt = input("Player 1 Qubit(s)(ex. 1): ")
        if((int(list(qbt)[0]) != 3 and int(list(qbt)[0]) != 0 and int(list(qbt)[-1]) != 0) or (operation.lower() == "m" and int(qbt) == 3)):
            flag1 = False
            if(operation.lower() == 'h'):
                qc.h(int(qbt))
                qc.barrier()
                vc.h(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'x'):
                qc.x(int(qbt))
                qc.barrier()
                vc.x(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'y'):
                qc.y(int(qbt))
                qc.barrier()
                vc.y(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'z'):
                qc.z(int(qbt))
                qc.barrier()
                vc.z(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'm'):
                qc.measure([int(qbt)],[int(qbt)])  
                qc.barrier()
                vc.measure([int(qbt)],[int(qbt)])  
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
                if(netExpectation[int(qbt)] == 1):
                    input("It measured 1")
                    if(int(qbt) == 3):
                        Victory = 1
                else:
                    input("It measured 0")
                flag2 = False
            elif(operation.lower() == "cx"):
                if(int(list(qbt)[0]) != int(list(qbt)[-1])):
                    qc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                    qc.barrier()
                    vc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                    vc.barrier()
                    flag2 = False
            elif(operation.lower() == "ccx"):
                if(int(list(qbt)[0]) != int(list(qbt)[-1]) and int(list(qbt)[1]) != int(list(qbt)[-1]) and int(list(qbt)[0]) != int(list(qbt)[1])):
                    qc.ccx(int(list(qbt)[0]),int(list(qbt)[1]),int(list(qbt)[-1]))
                    qc.barrier()
                    vc.ccx(int(list(qbt)[0]),int(list(qbt)[1]),int(list(qbt)[-1]))
                    vc.barrier()
                    flag2 = False
            else:
                print("Operation Error, please re-enter move")
        else:
            print("Qubit Number Error, please re-enter move")
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
    global vecExpectation
    global netExpectation
    global Victory
    screen()
    flag1 = True
    flag2 = True
    while(flag1 or flag2):
        operation = input("Player 2 Operation(ex. H): ")
        qbt = input("Player 2 Qubit(s)(ex. 1): ")
        if((int(list(qbt)[0]) != 3 and int(list(qbt)[0]) != 0 and int(list(qbt)[-1]) != 3) or (operation.lower() == "m" and int(qbt) == 0)):
            flag1 = False
            if(operation.lower() == 'h'):
                qc.h(int(qbt))
                qc.barrier()
                vc.h(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'x'):
                qc.x(int(qbt))
                qc.barrier()
                vc.x(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'y'):
                qc.y(int(qbt))
                qc.barrier()
                vc.y(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'z'):
                qc.z(int(qbt))
                qc.barrier()
                vc.z(int(qbt))
                vc.barrier()
                flag2 = False
            elif(operation.lower() == 'm'):
                qc.measure([int(qbt)],[int(qbt)])  
                qc.barrier()
                vc.measure([int(qbt)],[int(qbt)])  
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
                if(netExpectation[int(qbt)] == 1):
                    input("It measured 1")
                    if(int(qbt) == 0):
                        Victory = 2
                else:
                    input("It measured 0")
                flag2 = False
            elif(operation.lower() == "cx"):
                if(int(list(qbt)[0]) != int(list(qbt)[-1])):
                    qc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                    qc.barrier()
                    vc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                    vc.barrier()
                    flag2 = False
            elif(operation.lower() == "ccx"):
                if(int(list(qbt)[0]) != int(list(qbt)[-1]) and int(list(qbt)[1]) != int(list(qbt)[-1]) and int(list(qbt)[0]) != int(list(qbt)[1])):
                    qc.ccx(int(list(qbt)[0]),int(list(qbt)[1]),int(list(qbt)[-1]))
                    qc.barrier()
                    vc.ccx(int(list(qbt)[0]),int(list(qbt)[1]),int(list(qbt)[-1]))
                    vc.barrier()
                    flag2 = False
            else:
                print("Operation Error, please re-enter move")
        else:
            print("Qubit Number Error, please re-enter move")
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



def ai1turn():
    global statevec
    global mystatevec1
    global vecExpectation
    global netExpectation
    global Victory
    screen()
    netInput = [0.000 for x in range(36)]
    for x in range(4):
        netInput[x] = netExpectation[x]
    for x in range(32):
        netInput[x+4] = mystatevec1[x]
    move = aiPlayer.run(np.array(netInput))
    highest = 0
    index = 0
    for x in range(16):
        if(highest<move[x]):
            highest = move[x]
            index = x
    if(index == 0):
        qc.h(1)
        qc.barrier()
        vc.h(1)
        vc.barrier()
    if(index == 1):
        qc.h(2)
        qc.barrier()
        vc.h(2)
        vc.barrier()
    elif(index == 2):
        qc.x(1)
        qc.barrier()
        vc.x(1)
        vc.barrier()
    elif(index == 3):
        qc.x(2)
        qc.barrier()
        vc.x(2)
        vc.barrier()
    elif(index == 4):
        qc.y(1)
        qc.barrier()
        vc.y(1)
        vc.barrier()
    elif(index == 5):
        qc.y(2)
        qc.barrier()
        vc.y(2)
        vc.barrier()
    elif(index == 6):
        qc.z(1)
        qc.barrier()
        vc.z(1)
        vc.barrier()
    elif(index == 7):
        qc.z(2)
        qc.barrier()
        vc.z(2)
        vc.barrier()
    elif(index == 8):
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
    elif(index == 9):
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
    elif(index == 10):
        qc.measure([3],[3])  
        qc.barrier()
        vc.measure([3],[3])  
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
        if(netExpectation[3] == 1):
            Victory = 1
    elif(index == 11):
        qc.cx(1,2)
        qc.barrier()
        vc.cx(1,2)
        vc.barrier()
    elif(index == 12):
        qc.cx(2,1)
        qc.barrier()
        vc.cx(2,1)
        vc.barrier()
    elif(index == 13):
        qc.cx(1,3)
        qc.barrier()
        vc.cx(1,3)
        vc.barrier()
    elif(index == 14):
        qc.cx(2,3)
        qc.barrier()
        vc.cx(2,3)
        vc.barrier()
    elif(index == 15):
        qc.ccx(1,2,3)
        qc.barrier()
        vc.ccx(1,2,3)
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

def ai2turn():
    global statevec
    global mystatevec1
    global vecExpectation
    global netExpectation
    global Victory
    screen()
    netInput = [0.000 for x in range(36)]
    for x in range(4):
        netInput[x] = netExpectation[3-x]
    netInput[4] = mystatevec1[0]
    netInput[5] = mystatevec1[1]
    netInput[20] = mystatevec1[2]
    netInput[21] = mystatevec1[3]
    netInput[12] = mystatevec1[4]
    netInput[13] = mystatevec1[5]
    netInput[28] = mystatevec1[6]
    netInput[29] = mystatevec1[7]
    netInput[8] = mystatevec1[8]
    netInput[9] = mystatevec1[9]
    netInput[24] = mystatevec1[10]
    netInput[25] = mystatevec1[11]
    netInput[16] = mystatevec1[12]
    netInput[17] = mystatevec1[13]
    netInput[32] = mystatevec1[14]
    netInput[33] = mystatevec1[15]
    netInput[6] = mystatevec1[16]
    netInput[7] = mystatevec1[17]
    netInput[22] = mystatevec1[18]
    netInput[23] = mystatevec1[19]
    netInput[14] = mystatevec1[20]
    netInput[15] = mystatevec1[21]
    netInput[30] = mystatevec1[22]
    netInput[31] = mystatevec1[23]
    netInput[10] = mystatevec1[24]
    netInput[11] = mystatevec1[25]
    netInput[26] = mystatevec1[26]
    netInput[27] = mystatevec1[27]
    netInput[18] = mystatevec1[28]
    netInput[19] = mystatevec1[29]
    netInput[34] = mystatevec1[30]
    netInput[35] = mystatevec1[31]

    move = aiPlayer.run(np.array(netInput))
    highest = 0
    index = 0
    for x in range(16):
        if(highest<move[x]):
            highest = move[x]
            index = x
    if(index == 0):
        qc.h(2)
        qc.barrier()
        vc.h(2)
        vc.barrier()
    if(index == 1):
        qc.h(1)
        qc.barrier()
        vc.h(1)
        vc.barrier()
    elif(index == 2):
        qc.x(2)
        qc.barrier()
        vc.x(2)
        vc.barrier()
    elif(index == 3):
        qc.x(1)
        qc.barrier()
        vc.x(1)
        vc.barrier()
    elif(index == 4):
        qc.y(2)
        qc.barrier()
        vc.y(2)
        vc.barrier()
    elif(index == 5):
        qc.y(1)
        qc.barrier()
        vc.y(1)
        vc.barrier()
    elif(index == 6):
        qc.z(2)
        qc.barrier()
        vc.z(2)
        vc.barrier()
    elif(index == 7):
        qc.z(1)
        qc.barrier()
        vc.z(1)
        vc.barrier()
    elif(index == 8):
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
    elif(index == 9):
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
    elif(index == 10):
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
    elif(index == 11):
        qc.cx(2,1)
        qc.barrier()
        vc.cx(2,1)
        vc.barrier()
    elif(index == 12):
        qc.cx(1,2)
        qc.barrier()
        vc.cx(1,2)
        vc.barrier()
    elif(index == 13):
        qc.cx(2,0)
        qc.barrier()
        vc.cx(2,0)
        vc.barrier()
    elif(index == 14):
        qc.cx(1,0)
        qc.barrier()
        vc.cx(1,0)
        vc.barrier()
    elif(index == 15):
        qc.ccx(1,2,0)
        qc.barrier()
        vc.ccx(1,2,0)
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
    global statevec
    global mystatevec
    global vecExpectation
    global netExpectation
    qc.h(1)
    vc.h(1)
    qc.h(2)
    qc.barrier()
    vc.h(2)
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
    while(Victory == 0):
        if(turnorder == 1):
            player1turn()
            if(Victory == 0):
                ai2turn()
        if(turnorder == 2):
            ai1turn()
            if(Victory == 0):
                player2turn()
aiPlayer = workerNet(0,0,0)
turnorder = int(input("would you like to be player1 or player2(ex. 1): "))
name = input("Which net would you like to play: ")
myfile = open(name+".txt", "r")
Memory = myfile.read()
weights0a = []
weights1a = []
for x in range(10):
    Memory.replace("  "," ")
Memory = Memory.replace(" ",",")
Memory = Memory.replace("\n",",")
for x in range(10):
    Memory = Memory.replace(",,",",")
Memory = Memory.replace("[,","[")
Memory = Memory.replace(",]","]")
exec("weights0a, weights1a = "+Memory)
weights0a = np.array(weights0a)
weights1a = np.array(weights1a)
aiPlayer.load(weights0a,weights1a,0)
myfile.close()
main()
os.system("cls")
screen()
input("Congratulations!!! Player "+str(Victory)+" Won!!!")