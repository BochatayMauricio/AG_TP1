import random 
import numpy as np
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
#Valor de la funcion objetivo en x, referencia el indice con el cromosoma de poblacion actual
valueObjetive = []
#poblacion actual
poblation = []

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
    for i in poblationAct:
        valueObjetive.insert(j,functionObjetive(binaryToDecimal(i))) 
        print('Cromosoma: ',i, 'Valor funcion: ',valueObjetive[j])
        j+=j
    print('-------------------------------------------------------------------------------')
    max=min= valueObjetive[0]
    total = 0
    for i in valueObjetive:
        total+=i
        if(i<min):
            min = i
        if(i>max):
            max = i
    
    minimePoblational.insert(numPoblation,min)
    maximePoblational.insert(numPoblation,max)
    totalValue.append(total)
    prom.append(total/len(valueObjetive))
    if(numPoblation == 0):
        print('total poblacion inicial: ',totalValue[numPoblation])
        print('minimo de poblacion inicial: ',minimePoblational[numPoblation])
        print('maximo de poblacion inicial: ',maximePoblational[numPoblation])
        print('Promedio de poblacion inicial: ',prom[numPoblation])
    else:
        print('total poblacion actual: ',totalValue[numPoblation])
        print('minimo de poblacion actual: ',minimePoblational[numPoblation])
        print('maximo de poblacion actual: ',maximePoblational[numPoblation])
        print('Promedio de poblacion actual: ',prom[numPoblation])
    print('-------------------------------------------------------------------------------')

def functionFitness(poblation,numPoblation):
    long = len(poblation)
    for i in range(long):
        fitness.insert(i,valueObjetive[i] / totalValue[numPoblation])  #a cada cromosoma se lo puntua según el valor/sobre total

def selectCrom(fitness:list):
    ruleta = []
    maxFitt = 0 
    dif = 0 #por si no se completa la ruleta se la sumamos al que mas tiene para llegar a 100%
    rulPos = 0 #numero de la ruleta
    percenFitt = []
    percenTotal=0
    seleccion = [] #cromosomas seleccionados
    numWin = 0
    for i in range(10):
        percenFitt.insert(i,int(fitness[i]*100)) #fitness en forma de porcentaje a cada cromosoma
        if(percenFitt[i] == 0):
            percenFitt[i] = 1

        if(percenFitt[i]>maxFitt):
            maxFitt = percenFitt[i]

        percenTotal+=percenFitt[i]
    
    if(percenTotal<100):
        dif = 100 - percenTotal
        index = percenFitt.index(maxFitt) #busco el indice del cromosoma con mas porcentaje
        percenFitt[index]+=dif #le sumo el porcentaje que faltaba al cromosoma candidato

    if(percenTotal>100):
        dif = percenTotal - 100
        index = percenFitt.index(maxFitt) #busco el indice del cromosoma con mas porcentaje
        percenFitt[index]-=dif #se lo resto, para que la suma sea del 100%, no se exceda

    #con dos for anidados, llenamos el arreglo ruleta segun los porcentajes de cada cromosoma, 
    #mas porcentaje tiene mas posiciones en el arreglo tendra ese cromosoma
    for c in range(10):
        for i in range(percenFitt[c]):
            ruleta.insert(rulPos,c) #guardamos el indice, no el decimal del cromosoma
            rulPos+=1
    #ahora simulamos el giro de la ruleta
    for j in range(10):
        numWin = random.randint(1,100)
        seleccion.insert(j,ruleta[numWin])
    
    print('Ruleta resultante: ',seleccion)
    return seleccion

def crossover(poblation:list,seleccion:list):
    newPoblation = []
    

    return newPoblation


#PROGRAMA PRINCIPAL
initialPoblation()
ActualValuesPoblation(0,initial) #porque es la primera vez, despues invocamos con "poblation" por parametro
functionFitness(initial,0)
seleccion = selectCrom(fitness)
newPoblation = crossover(poblation,seleccion)