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
nodals = 0
modificada = 0
for i in range(len(content)):
    #remover final \n das linhas do content
    content[i] = content[i][0:-1] 
    #adiciona uma lista com os dados de cada componente na matriz component
    componentsData += [content[i].split()]
    #checa a quantidade de nos
    try:
        if float(componentsData[i][1]) > nodals:
            nodals = int(componentsData[i][1])
        if float(componentsData[i][2]) > nodals:
            nodals = int(componentsData[i][2])
        if (componentsData[i][0][0] == "V") or (componentsData[i][0][0] == "E") or (componentsData[i][0][0] == "H"):
            modificada += 1
        if componentsData[i][0][0] == ("H"):
            modificada += 2
    except:
        print("Linha " + str(i) + " não foi reconhecida como um componente")

#monta matrizes zeradas de acordo com o numero de nos
G = np.zeros((nodals + modificada + 1, nodals + modificada + 1))
I = np.zeros(nodals + modificada + 1)

#monta a matriz de acordo com os componentes dados
indiceMod = 1
for i in range(len(content)):
    nome = componentsData[i][0][0]

    if nome == "R": #resistor
        G[int(componentsData[i][2])][int(componentsData[i][2])] += 1/float(componentsData[i][3])
        G[int(componentsData[i][1])][int(componentsData[i][1])] += 1/float(componentsData[i][3])
        G[int(componentsData[i][1])][int(componentsData[i][2])] += -1/float(componentsData[i][3])
        G[int(componentsData[i][2])][int(componentsData[i][1])] += -1/float(componentsData[i][3])


    elif nome == "I": #fonte de corrente independente
        I[int(componentsData[i][2])] += float(componentsData[i][4]) 
        I[int(componentsData[i][1])] += -float(componentsData[i][4])

    elif nome == "G": #fonte de corrente controlada por tensão
        G[int(componentsData[i][1])][int(componentsData[i][3])] += -float(componentsData[i][5])
        G[int(componentsData[i][1])][int(componentsData[i][4])] += float(componentsData[i][5])
        G[int(componentsData[i][2])][int(componentsData[i][3])] += float(componentsData[i][5])
        G[int(componentsData[i][2])][int(componentsData[i][4])] += -float(componentsData[i][5])

    elif nome == "C": #Capacitor
        G[int(componentsData[i][1])][int(componentsData[i][1])] += j*w*float(componentsData[i][3])
        G[int(componentsData[i][1])][int(componentsData[i][2])] += -j*w*float(componentsData[i][3])
        G[int(componentsData[i][2])][int(componentsData[i][1])] += -j*w*float(componentsData[i][3])
        G[int(componentsData[i][2])][int(componentsData[i][2])] += j*w*float(componentsData[i][3])
        try:
            I[int(componentsData[i][1])] += float(componentsData[i][4])
            I[int(componentsData[i][2])] += -float(componentsData[i][4])
        except:
            pass
        
    elif nome == "L": #Indutor
        G[int(componentsData[i][1])][int(componentsData[i][1])] += 1/(j*w*float(componentsData[i][3]))
        G[int(componentsData[i][1])][int(componentsData[i][2])] += -1/(j*w*float(componentsData[i][3]))
        G[int(componentsData[i][2])][int(componentsData[i][1])] += -1/(j*w*float(componentsData[i][3]))
        G[int(componentsData[i][2])][int(componentsData[i][2])] += 1/(j*w*float(componentsData[i][3]))
        try:
            I[int(componentsData[i][1])] += -float(componentsData[i][4])
            I[int(componentsData[i][2])] += float(componentsData[i][4])
        except:
            pass

    elif nome == "V": #Fonte de tensao
        G[int(componentsData[i][1])][nodals + indiceMod] += 1
        G[int(componentsData[i][2])][nodals + indiceMod] += -1
        G[nodals + indiceMod][int(componentsData[i][1])] += -1
        G[nodals + indiceMod][int(componentsData[i][2])] += 1
        I[nodals + indiceMod] += -float(componentsData[i][4])
        print("J" + str(indiceMod) + " => " + componentsData[i][0])
        indiceMod += 1

    elif nome == "E": #Fonte de tensao controlada por tensao
        G[int(componentsData[i][1])][nodals + indiceMod] += 1
        G[int(componentsData[i][2])][nodals + indiceMod] += -1
        G[nodals + indiceMod][int(componentsData[i][1])] += -1
        G[nodals + indiceMod][int(componentsData[i][2])] += 1
        G[nodals + indiceMod][int(componentsData[i][3])] += float(componentsData[i][5])
        G[nodals + indiceMod][int(componentsData[i][4])] += -float(componentsData[i][5])
        print("J" + str(indiceMod) + " => " + componentsData[i][0])
        indiceMod += 1
    
    elif nome == "F": #Fonte de corrente controlada por corrente
        G[int(componentsData[i][1])][nodals + indiceMod] += float(componentsData[i][5])
        G[int(componentsData[i][2])][nodals + indiceMod] += -float(componentsData[i][5])
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
        G[nodals + indiceMod + 1][nodals + indiceMod] += float(componentsData[i][5])
        print("J" + str(indiceMod) + " => " + componentsData[i][0] + " Control")
        print("J" + str(indiceMod + 1) + " => " + componentsData[i][0] + " Source")
        indiceMod += 2

#transformas as matrizes em arrays do numpy
G = np.array(G)
I = np.array(I)

#apaga a linha e coluna 0 do no ground
G = np.delete(G, 0, axis=0)
G = np.delete(G, 0, axis=1)
I = np.delete(I, 0)

#resolve o sistema linear
E = np.linalg.solve(G, I)

#printa os valores das tensões nodais
for i in range (nodals):
    print("V" + str(i+1) + "= " + str(E[i]))
for i in range (modificada):
    print("J" + str(i+1) + "= " + str(E[i]))



