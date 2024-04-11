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

def ActualValuesPoblation(numPoblation):
    j=0
    for i in initial:
        valueObjetive.insert(j,functionObjetive(binaryToDecimal(i))) 
        j+=j
    print(valueObjetive)
    max=min= valueObjetive[0]
    total = 0
    for i in valueObjetive:
        total+=i
        if(i<min):
            min = i
        if(i>max):
            max = i
    
    minimePoblational.insert(0,min)
    maximePoblational.insert(0,max)

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


def functionFitness(poblation,numPoblation):
    long = len(poblation)
    for i in range(long):
        fitness[i] = valueObjetive[i] / totalValue[numPoblation]
        
#PROGRAMA PRINCIPAL
initialPoblation()
ActualValuesPoblation(0)
