import sympy as sp
import numpy as np


#funcoes para a analise dos componentes em cada linha da netlist
def decideComponente(linhaComponentData):
    component = linhaComponentData[1]
    return component


#inicio da main
fileName = input("Insira o nome do doc netlist (Ex: netlist.net): ")
file = open(fileName, 'r')
content = file.readlines()

componentsData = []
w = 2*(np.pi)
nodals = 0
modificada = 0
regSen = False
t = sp.Symbol("t")
for i in range(len(content)):
    #remover final \n das linhas do content
    content[i] = content[i][0:-1] 
    #adiciona uma lista com os dados de cada componente na matriz component
    componentsData += [content[i].split()]

for i in range(len(componentsData)):
    #checa o tamanho da matriz e a frequencia(w)
    try:
        if componentsData[i][0][0] == "K":
            if int(componentsData[i][2]) > nodals:
                nodals = int(componentsData[i][2])
            if int(componentsData[i][3]) > nodals:
                nodals = int(componentsData[i][3])
            if int(componentsData[i][6]) > nodals:
                nodals = int(componentsData[i][6])
            if int(componentsData[i][7]) > nodals:
                nodals = int(componentsData[i][7])
        else:  
            if int(componentsData[i][1]) > nodals:
                nodals = int(componentsData[i][1])
            if int(componentsData[i][2]) > nodals:
                nodals = int(componentsData[i][2])
        if (componentsData[i][0][0] == "V") or (componentsData[i][0][0] == "E") or (componentsData[i][0][0] == "H"):
            modificada += 1
        if componentsData[i][0][0] == "H":
            modificada += 2
        if (componentsData[i][0][0] == "V") or (componentsData[i][0][0] == "I"):
            if componentsData[i][3] == "SIN":
                w = 2*(np.pi)*complex(componentsData[i][6])
                regSen = True
    except:
        print("Linha " + str(i) + " não foi reconhecida como um componente")

#monta matrizes zeradas de acordo com o numero de nos
G = np.zeros((nodals + modificada + 1, nodals + modificada + 1), dtype="complex_")
I = np.zeros(nodals + modificada + 1, dtype="complex_")

#monta a matriz de acordo com os componentes dados
indiceMod = 1
for i in range(len(content)):
    nome = componentsData[i][0][0]

    if nome == "R": #resistor
        G[int(componentsData[i][2])][int(componentsData[i][2])] += 1/complex(componentsData[i][3])
        G[int(componentsData[i][1])][int(componentsData[i][1])] += 1/complex(componentsData[i][3])
        G[int(componentsData[i][1])][int(componentsData[i][2])] += -1/complex(componentsData[i][3])
        G[int(componentsData[i][2])][int(componentsData[i][1])] += -1/complex(componentsData[i][3])


    elif nome == "I": #fonte de corrente independente
        if componentsData[i][3] == "DC":
            I[int(componentsData[i][2])] += complex(componentsData[i][4]) 
            I[int(componentsData[i][1])] += -complex(componentsData[i][4])

        elif componentsData[i][3] == "SIN":
            Ao = complex(componentsData[i][4])
            A = complex(componentsData[i][5])
            f = complex(componentsData[i][6])
            ta = complex(componentsData[i][7])
            a = complex(componentsData[i][7])
            fi = complex(componentsData[i][8])
            pi = sp.pi
            exp = sp.exp(-a*(t-ta))
            #valor = Ao + (A*exp) * sp.sin(2*pi*f*(t-ta) + (pi/180)*fi)
            fase = (pi/180) * fi
            fasor = A*(sp.cos(fase)+1j*sp.sin(fase))
            I[int(componentsData[i][2])] += fasor
            I[int(componentsData[i][1])] += -fasor

    elif nome == "G": #fonte de corrente controlada por tensão
        G[int(componentsData[i][1])][int(componentsData[i][3])] += -complex(componentsData[i][5])
        G[int(componentsData[i][1])][int(componentsData[i][4])] += complex(componentsData[i][5])
        G[int(componentsData[i][2])][int(componentsData[i][3])] += complex(componentsData[i][5])
        G[int(componentsData[i][2])][int(componentsData[i][4])] += -complex(componentsData[i][5])

    elif nome == "C": #Capacitor
        G[int(componentsData[i][1])][int(componentsData[i][1])] += complex(1j*w*complex(componentsData[i][3]))
        G[int(componentsData[i][1])][int(componentsData[i][2])] += complex(-1j*w*complex(componentsData[i][3]))
        G[int(componentsData[i][2])][int(componentsData[i][1])] += complex(-1j*w*complex(componentsData[i][3]))
        G[int(componentsData[i][2])][int(componentsData[i][2])] += complex(1j*w*complex(componentsData[i][3]))

    elif nome == "L": #Indutor
        G[int(componentsData[i][1])][int(componentsData[i][1])] += complex(1/(1j*w*complex(componentsData[i][3])))
        G[int(componentsData[i][1])][int(componentsData[i][2])] += complex(-1/(1j*w*complex(componentsData[i][3])))
        G[int(componentsData[i][2])][int(componentsData[i][1])] += complex(-1/(1j*w*complex(componentsData[i][3])))
        G[int(componentsData[i][2])][int(componentsData[i][2])] += complex(1/(1j*w*complex(componentsData[i][3])))


    elif nome == "V": #Fonte de tensao
        if componentsData[i][3] == "DC":
            G[int(componentsData[i][1])][nodals + indiceMod] += 1
            G[int(componentsData[i][2])][nodals + indiceMod] += -1
            G[nodals + indiceMod][int(componentsData[i][1])] += -1
            G[nodals + indiceMod][int(componentsData[i][2])] += 1
            I[nodals + indiceMod] += -complex(componentsData[i][4])
            print("J" + str(indiceMod) + " => " + componentsData[i][0])
            indiceMod += 1
        
        elif componentsData[i][3] == "SIN":
            Ao = complex(componentsData[i][4])
            A = complex(componentsData[i][5])
            f = complex(componentsData[i][6])
            ta = complex(componentsData[i][7])
            a = complex(componentsData[i][7])
            fi = complex(componentsData[i][8])
            pi = sp.pi
            exp = sp.exp((-1)*a*(t-ta))
            #valor = Ao + (A*exp) * sp.sin(2*pi*f*(t-ta) + (pi/180)*fi)
            fase = (pi/180) * fi
            fasor = A*(sp.cos(fase)+1j*sp.sin(fase))
            G[int(componentsData[i][1])][nodals + indiceMod] += 1
            G[int(componentsData[i][2])][nodals + indiceMod] += -1
            G[nodals + indiceMod][int(componentsData[i][1])] += -1
            G[nodals + indiceMod][int(componentsData[i][2])] += 1
            I[nodals + indiceMod] += fasor
            print("J" + str(indiceMod) + " => " + componentsData[i][0])
            indiceMod += 1
    

    elif nome == "E": #Fonte de tensao controlada por tensao
        G[int(componentsData[i][1])][nodals + indiceMod] += 1
        G[int(componentsData[i][2])][nodals + indiceMod] += -1
        G[nodals + indiceMod][int(componentsData[i][1])] += -1
        G[nodals + indiceMod][int(componentsData[i][2])] += 1
        G[nodals + indiceMod][int(componentsData[i][3])] += complex(componentsData[i][5])
        G[nodals + indiceMod][int(componentsData[i][4])] += -complex(componentsData[i][5])
        print("J" + str(indiceMod) + " => " + componentsData[i][0])
        indiceMod += 1
    
    elif nome == "F": #Fonte de corrente controlada por corrente
        G[int(componentsData[i][1])][nodals + indiceMod] += complex(componentsData[i][5])
        G[int(componentsData[i][2])][nodals + indiceMod] += -complex(componentsData[i][5])
        G[int(componentsData[i][3])][nodals + indiceMod] += 1
        G[int(componentsData[i][4])][nodals + indiceMod] += -1
        G[nodals + indiceMod][int(componentsData[i][3])] += -1
        G[nodals + indiceMod][int(componentsData[i][4])] += 1
        print("J" + str(indiceMod) + " => " + componentsData[i][0])
        indiceMod += 1
    
    elif nome == "H": #Fonte de tensao controlada por corrente
        G[int(componentsData[i][1])][nodals + indiceMod + 1] += 1
        G[int(componentsData[i][2])][nodals + indiceMod + 1] += -1
        G[int(componentsData[i][3])][nodals + indiceMod] += 1
        G[int(componentsData[i][4])][nodals + indiceMod] += -1
        G[nodals + indiceMod][int(componentsData[i][3])] += -1
        G[nodals + indiceMod][int(componentsData[i][4])] += 1
        G[nodals + indiceMod + 1][int(componentsData[i][1])] += -1
        G[nodals + indiceMod + 1][int(componentsData[i][2])] += 1
        G[nodals + indiceMod + 1][nodals + indiceMod] += complex(componentsData[i][5])
        print("J" + str(indiceMod) + " => " + componentsData[i][0] + " Control")
        print("J" + str(indiceMod + 1) + " => " + componentsData[i][0] + " Source")
        indiceMod += 2
    
    elif nome == "K": #transformador ideal
        L1 = complex(componentsData[i][4])
        L2 = complex(componentsData[i][8])
        M = complex(componentsData[i][9])
        L11 = L2/(L1*L2 - (M*M))
        L22 = L1/(L1*L2 - (M*M))
        L12 = -M/(L1*L2 - (M*M))
        G[int(componentsData[i][2])][int(componentsData[i][2])] += L11/(1j*w)
        G[int(componentsData[i][2])][int(componentsData[i][3])] += -L11/(1j*w)
        G[int(componentsData[i][2])][int(componentsData[i][6])] += L12/(1j*w)
        G[int(componentsData[i][2])][int(componentsData[i][7])] += -L12/(1j*w)
        G[int(componentsData[i][3])][int(componentsData[i][2])] += -L11/(1j*w)
        G[int(componentsData[i][3])][int(componentsData[i][3])] += L11/(1j*w)
        G[int(componentsData[i][3])][int(componentsData[i][6])] += -L12/(1j*w)
        G[int(componentsData[i][3])][int(componentsData[i][7])] += L12/(1j*w)
        G[int(componentsData[i][6])][int(componentsData[i][2])] += L12/(1j*w)
        G[int(componentsData[i][6])][int(componentsData[i][3])] += -L12/(1j*w)
        G[int(componentsData[i][6])][int(componentsData[i][6])] += L22/(1j*w)
        G[int(componentsData[i][6])][int(componentsData[i][7])] += -L22/(1j*w)
        G[int(componentsData[i][7])][int(componentsData[i][2])] += -L12/(1j*w)
        G[int(componentsData[i][7])][int(componentsData[i][3])] += L12/(1j*w)
        G[int(componentsData[i][7])][int(componentsData[i][6])] += -L22/(1j*w)
        G[int(componentsData[i][7])][int(componentsData[i][7])] += L22/(1j*w)

#transformas as matrizes em arrays do numpy
G = np.array(G)
I = np.array(I)

#apaga a linha e coluna 0 do no ground

G = np.delete(G, 0, axis=0)
G = np.delete(G, 0, axis=1)
I = np.delete(I, 0)

#resolve o sistema linear
E = np.linalg.solve(G, I)
print(E)

#printa os valores das tensões nodais
if regSen == False:
    for i in range (nodals):
        print("V" + str(i+1) + "= " + str(E[i]))
else:
    for i in range (nodals):
        parentesesInicial = 0
        signCount = 0
        real = ""
        img = ""
        V = str(E[i])
        for n in range (len(V) - 1):
            if parentesesInicial == 1:
                if (((str(V[n]) == "-")  or (str(V[n]) == "+")) and str(V[n-1]) != "e"):
                    signCount += 1
                if signCount == 2:
                    img += str(V[n])
                else:
                    real += str(V[n])
            else:
                parentesesInicial += 1
        if img[0] == "-":
            img = "+" + img[1:]
        else:
            img = "-" + img[1:]
        print("V" + str(i+1) + "= " + real + "*cos(" + str(w) + "*t)" + img + "*sin(" + str(w) + "*t")




