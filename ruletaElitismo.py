import random 
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
import matplotlib.pyplot as plt
import math

#dominio de la funcino definido en el enunciado
domain = [0,int(2**30)-1]
initial = []
#en esta lista acumularemos el total de f(x) de cada poblacion
totalValue = []
#Minimos ,maximos de cada poblacion, cada posicion refiere al numero de la poblacion
minimePoblational = []
maximePoblational = []
#promedio de cada poblacion, cada posicion refiere al numero de la poblacion
prom = []

#fitness de cada cromosoma de la poblacion actual
fitness = []

#FUNCIONES


#Funcion definida --> devuelve valor de f(x) con x decimal
def functionObjetive(x): 
    return (x/((2**30)-1))**2


#Convierto a binario el gen en decimal --> me da un cromosoma binario
def decimalToBinary(num:int):
    binary=[]
    while (num>0):
        digit  = num%2
        num = int(num//2)
        binary.append(digit)
    if(len(binary) < 30):
        for j in range(len(binary),30):
            binary.append(0)
    binary.reverse()
    return binary

#Convierto a decimal el cromosoma.
def binaryToDecimal(binary:list):
    decimal = 0
    i = 1
    for d in binary:
        if(d == 1):
            index = int(len(binary)) - i
            decimal = int(decimal) + int(2**index)
        i=i+1
    return decimal

#Generar poblacion inicial
def initialPoblation():
    for _ in range(10):
        num = random.randint(domain[0],domain[1])
        initial.append(decimalToBinary(num))
    print('Poblacion Inicial: ')
    print(initial)
    print('-------------------------------------------------------------------------------')

def ActualValuesPoblation(numPoblation,poblationAct):
    j=0
    #Valor de la funcion objetivo en x, referencia el indice con el cromosoma de poblacion actual
    valueObjetive = []
    for i in poblationAct:
        valueObjetive.insert(j,functionObjetive(binaryToDecimal(i))) 
        print('Cromosoma: ',i, 'Valor funcion: ',valueObjetive[j])
        j=j+1
    print('-------------------------------------------------------------------------------')
    max=min= valueObjetive[0]
    total = 0
    indexMax=0
    for i in range(10):
        total+=valueObjetive[i]
        if(valueObjetive[i]<min):
            min = valueObjetive[i]
        if(valueObjetive[i]>max):
            max = valueObjetive[i]
            indexMax = i
    
    print("Indice crom: ",indexMax)
    cromMax = poblationAct[indexMax]

    minimePoblational.insert(numPoblation,min)
    maximePoblational.insert(numPoblation,max)
    totalValue.append(total)
    prom.append(total/len(valueObjetive))
    
    if(numPoblation == 0):
        print('total poblacion inicial: ',totalValue[numPoblation])
        print('minimo de poblacion inicial: ',minimePoblational[numPoblation])
        print('maximo de poblacion inicial: ',maximePoblational[numPoblation],'En el cromosoma: ',cromMax)
        print('Promedio de poblacion inicial: ',prom[numPoblation])
    else:
        print('total poblacion '+str(numPoblation)+':',totalValue[numPoblation])
        print('minimo de poblacion '+str(numPoblation)+':',minimePoblational[numPoblation])
        print('maximo de poblacion '+str(numPoblation)+':',maximePoblational[numPoblation],'en el cromosoma: ',cromMax)
        print('Promedio de poblacion '+str(numPoblation)+':',prom[numPoblation])
    print('-------------------------------------------------------------------------------')
    return valueObjetive

def functionFitness(poblation,numPoblation,valueObjetive):
    print("long pob: ",len(poblation))
    for i in range(0,10):
        fitness.insert(i,valueObjetive[i] / totalValue[numPoblation])  #a cada cromosoma se lo puntua según el valor/sobre total
    
def selectCromRuletaElite(fitness:list):
    ruleta = []
    maxFitt = 0 
    dif = 0 #por si no se completa la ruleta se la sumamos al que mas tiene para llegar a 100%
    rulPos = 0 #numero de la ruleta
    percenFitt = []
    percenTotal=0
    seleccion = [] #cromosomas seleccionados
    numWin = 0
    elites = [-1,-1] #dupla de los mejores de la poblacion

    for i in range(10):
        percenFitt.insert(i,int(fitness[i]*100)) #fitness en forma de porcentaje a cada cromosoma
        if(percenFitt[i] == 0):
            percenFitt[i] = 1

        if(percenFitt[i]>maxFitt):
            maxFitt = percenFitt[i]

        percenTotal=percenTotal+percenFitt[i]

    #completo fittnes para que llegue al 100% el total
    index = percenFitt.index(maxFitt) #busco el indice del cromosoma con mas porcentaje
    if(percenTotal<100):
        dif = 100 - percenTotal
        percenFitt[index]=percenFitt[index]+dif #le sumo el porcentaje que faltaba al cromosoma candidato

    if(percenTotal>100):
        dif = percenTotal - 100
        percenFitt[index]=percenFitt[index]-dif #se lo resto, para que la suma sea del 100%, no se exceda
    
    print("porcentaje total:",percenFitt)
    #ELITISMO
    max1=0
    max2=0
    for c in range(10):
        if(fitness[c]>max1):
            max2=max1
            max1=fitness[c]
            elites[1]=elites[0]
            elites[0]=c

        elif(fitness[c]>max2 and fitness[c]!=max1):
            max2=fitness[c]
            elites[1]=c 

    print("Elites: ",elites)
    seleccion.insert(0,elites[0])
    seleccion.insert(1,elites[1])
    

    #con dos for anidados, llenamos el arreglo ruleta segun los porcentajes de cada cromosoma, 
    #mas porcentaje tiene mas posiciones en el arreglo tendra ese cromosoma
    for c in range(10):
        for _ in range(percenFitt[c]):
            ruleta.insert(rulPos,c) #guardamos el indice, no el decimal del cromosoma
            rulPos+=1
    
    #ahora simulamos el giro de la ruleta(10 giros)
    for l in range(2,10):
        numWin = random.randint(0,99)
        seleccion.insert(l,ruleta[numWin])
    print('Ruleta resultante(Selección): ',seleccion)
    return seleccion

def crossover(poblation:list,seleccion:list):
    newPoblation = []
    duplaPadres=[] #los dos que mas salieron en la ruleta
    #Probabilidad de crossover
    probabilidadCrossover = 0.75

    #paso a la siguiente poblacion los elites(los dos primeros de la seleccion)
    newPoblation.insert(0,poblation[seleccion[0]])
    newPoblation.insert(1,poblation[seleccion[1]])
   
    j=2
    z=3
    for _ in range(4):
        duplaPadres.insert(0,seleccion[j])
        duplaPadres.insert(1,seleccion[z])
        j+=2
        z+=2
        print(duplaPadres)
        probabilidadRandom = (random.randint(0,100))/100
        if(probabilidadCrossover > probabilidadRandom):
            #Hago el cruzamiento
            puntoCorte = random.randint(0,29)
            
            p11=[] #parte izquierda del padre 1
            p12=[] #parte derecha del padre 2
            p21=[] #parte izquierda del padre 1
            p22=[]  #parte derecha del padre 2
            print('Punto de corte:',puntoCorte)
            p11 = poblation[duplaPadres[0]][0:puntoCorte]
            p12 = poblation[duplaPadres[0]][puntoCorte:30]
            p21 = poblation[duplaPadres[1]][0:puntoCorte]
            p22 = poblation[duplaPadres[1]][puntoCorte:30]
            print('Parte 1 padre1:', p11)
            print('Parte 2 padre1:', p12)
            print('Parte 1 padre2:', p21)
            print('Parte 2 padre2:', p22)
            #Ya obtenidos los cromosomas divididos por el punto de corte random, hacemos el cruzamiento

            hijo1=p11+p22
            hijo2=p12+p21
            
            hijo1Mut = mutacion(hijo1)
            hijo2MUt = mutacion(hijo2)
            
            hijo1Mut = mutacion(hijo1)
            hijo2MUt = mutacion(hijo2)
            
        else:

            hijo1Mut = mutacion(poblation[duplaPadres[0]])
            hijo2MUt = mutacion(poblation[duplaPadres[1]])
            
        newPoblation.append(hijo1Mut)
        newPoblation.append(hijo2MUt)

        duplaPadres.clear()
    return newPoblation

def mutacion(cromosoma):
    probabilidadMutacion=0.05
    probMutRandom = (random.randint(0,100))/100
    if(probMutRandom < probabilidadMutacion):
        puntoCambio = random.randint(0,29)
        valor=cromosoma.pop(puntoCambio)
        if(valor==0):
            cromosoma.insert(puntoCambio,1)
        else:
            cromosoma.insert(puntoCambio,0)
    return cromosoma

def guardarDatos(numPoblation,poblation:list):
    indexCrom = valuesObjetive.index(maximePoblational[numPoblation])

    cromMax = poblation[indexCrom]
    minimo=minimePoblational[numPoblation]
    maximo=maximePoblational[numPoblation]
    promedio=prom[numPoblation]

    sheet['B'+str(numPoblation+2)] = minimo
    sheet['C'+str(numPoblation+2)] = promedio
    sheet['D'+str(numPoblation+2)] = maximo
    sheet['E'+str(numPoblation+2)] = str(cromMax)
    if(numPoblation==0):
        sheet['A'+str(numPoblation+2)] = 'Inicial'
    else:
        sheet['A'+str(numPoblation+2)] = numPoblation
    book.save('resultados_corridas_ruleta_elitismo.xlsx')  

def grafica(maximos,minimos,promedios):
    axis = []
    for i in range(len(maximos)):
        axis.append(i)

    #grafico
    fig, ax = plt.subplots()
    ax.plot(axis,maximos,color='tab:red',label='Maximos')
    ax.plot(axis,minimos,color='tab:green',label='Minimos')
    ax.plot(axis,promedios,color='tab:orange',label='Promedios')
    plt.title("Maximos, Minimos y Promedios por poblacion")
    plt.xlabel("Numero de poblacion")
    plt.ylabel("Valor f(x)")
    ax.legend(loc = 'lower right')
    plt.show()
    
#PROGRAMA PRINCIPAL
book = Workbook()
sheet = book.active #hoja activa del excel
sheet['A1'] = 'Numero de Poblacion'
sheet['B1'] = 'Minimo'
sheet['C1'] = 'Promedio'
sheet['D1'] = 'Maximo'
sheet['E1'] = 'Cromosoma del maximo'

initialPoblation()
valuesObjetive = ActualValuesPoblation(0,initial) #porque es la primera vez, despues invocamos con "poblation" por parametro
guardarDatos(0,initial)
functionFitness(initial,0,valuesObjetive)
seleccion = selectCromRuletaElite(fitness)
siguientePoblacion = crossover(initial,seleccion)
for j in range(1,21):
    fitness.clear()
    valuesObjetive = ActualValuesPoblation(j,siguientePoblacion)
    guardarDatos(j,siguientePoblacion)
    functionFitness(siguientePoblacion,j,valuesObjetive)
    seleccion = selectCromRuletaElite(fitness)
    poblacionAnterior = siguientePoblacion
    siguientePoblacion = crossover(poblacionAnterior,seleccion)
grafica(maximePoblational,minimePoblational,prom)
