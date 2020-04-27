from qiskit import *
import os
qc = QuantumCircuit(3,3)
vc = QuantumCircuit(3,3)#for visualization
sim_backend = BasicAer.get_backend('qasm_simulator')
statevec_backend = Aer.get_backend('statevector_simulator')
qubitNumber = 3
statevec = []
mystatevec = ["0+0i" for x in range(2**qubitNumber)]
mystatevec[0] = "1+0i"
vecExpectation = [0.000 for x in range(2**qubitNumber)]
vecExpectation[0] = 1
netExpectation = [0.000 for x in range(qubitNumber)]
Victory = 0

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
        if((int(list(qbt)[0]) != 2 and int(list(qbt)[0]) != 0 and int(list(qbt)[-1]) != 0) or (operation.lower() == "m" and int(qbt) == 2)):
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
                    if(int(qbt) == 2):
                        Victory = 1
                else:
                    input("It measured 0")
                flag2 = False
            elif(operation.lower() == "cx"):
                qc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                qc.barrier()
                vc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
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
        if((int(list(qbt)[0]) != 2 and int(list(qbt)[0]) != 0 and int(list(qbt)[-1]) != 2) or (operation.lower() == "m" and int(qbt) == 0)):
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
                qc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
                qc.barrier()
                vc.cx(int(list(qbt)[0]),int(list(qbt)[-1]))
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

def main():
    global statevec
    global mystatevec
    global vecExpectation
    global netExpectation
    qc.h(1)
    qc.barrier()
    vc.h(1)
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
        player1turn()
        if(Victory == 0):
            player2turn()
main()

input("Congratulations!!! Player "+str(Victory)+" Won!!!")