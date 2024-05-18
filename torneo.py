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

def funcionInverse(y):
    return math.sqrt(y)*(2**30-1)

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
    long = len(poblation)
    print("long pob: ",long)
    for i in range(10):
        fitness.insert(i,valueObjetive[i] / totalValue[numPoblation])  #a cada cromosoma se lo puntua según el valor/sobre total

def selectCromTorneo(fitness:list):
    seleccion = []
    while len(seleccion) < 10:
        index1=index2=-1
        while True: #elegimos dos individuos distintos de la poblacion y los llevamos a torneo, el de mejor fitness será seleccionado
            index1=random.randint(0,9)
            index2=random.randint(0,9)
            if(index1!=index2):
                break
        if(fitness[index1]>fitness[index2]):
            seleccion.append(index1)
        else:
            seleccion.append(index2)
    print("Seleccion: ",seleccion)
    return seleccion

def crossover(poblation:list,seleccion:list):
    newPoblation = []
    duplaPadres=[] #los dos que mas salieron en la ruleta
    #Probabilidad de crossover
    probabilidadCrossover = 0.75
    j=0
    z=1
    for _ in range(5):
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

            newPoblation.append(hijo1Mut)
            newPoblation.append(hijo2MUt)
        else:
            padre1Mut = mutacion(poblation[duplaPadres[0]])
            padre2Mut = mutacion(poblation[duplaPadres[1]])
            
            newPoblation.append(padre1Mut)
            newPoblation.append(padre2Mut)

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
    book.save('resultados_corridas_torneo.xlsx')  

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
seleccion = selectCromTorneo(fitness)
siguientePoblacion = crossover(initial,seleccion)
for j in range(1,21):
    fitness.clear()
    valuesObjetive = ActualValuesPoblation(j,siguientePoblacion)
    guardarDatos(j,siguientePoblacion)
    functionFitness(siguientePoblacion,j,valuesObjetive)
    seleccion = selectCromTorneo(fitness)
    poblacionAnterior = siguientePoblacion
    siguientePoblacion = crossover(poblacionAnterior,seleccion)
grafica(maximePoblational,minimePoblational,prom)
