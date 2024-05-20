import random 
from openpyxl import Workbook
from openpyxl.styles import Font
import matplotlib.pyplot as plt


#PARAMETROS
tamañoPoblacion = 10
cantidadCorridas = 20
probabilidadMutacion = 0.05
probabilidadCrossover = 0.75

#dominio de la funcino definido en el enunciado
dominio = [0,int(2**30)-1]
poblacionInicial = []
#en esta lista acumularemos el total de f(x) de cada poblacion
totalPorPoblacion = []
#Minimos ,maximos de cada poblacion, cada posicion refiere al numero de la poblacion
minimosPoblacion = []
maximosPoblacion = []
#promedio de cada poblacion, cada posicion refiere al numero de la poblacion
prom = []

#fitness de cada cromosoma de la poblacion actual
fitness = []

#FUNCIONES


#Funcion definida --> devuelve valor de f(x) con x decimal
def funcionObjetivo(x): 
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
def iniciarPoblacion():
    for _ in range(tamañoPoblacion):
        num = random.randint(dominio[0],dominio[1])
        poblacionInicial.append(decimalToBinary(num))
    print('Poblacion Inicial: ')
    print(poblacionInicial)
    print('-------------------------------------------------------------------------------')

def ActualValuesPoblation(numPoblacion,poblacionAct):
    j=0
    #Valor de la funcion objetivo en x, referencia el indice con el cromosoma de poblacion actual
    valoresObjetivos = []
    for i in poblacionAct:
        valoresObjetivos.insert(j,funcionObjetivo(binaryToDecimal(i))) 
        print('Cromosoma: ',i, 'Valor funcion: ',valoresObjetivos[j])
        j=j+1
    print('-------------------------------------------------------------------------------')
    max=min= valoresObjetivos[0]
    total = 0
    indexMax=0
    for i in range(len(poblacionAct)):
        total+=valoresObjetivos[i]
        if(valoresObjetivos[i]<min):
            min = valoresObjetivos[i]
        if(valoresObjetivos[i]>max):
            max = valoresObjetivos[i]
            indexMax = i
    
    print("Indice crom: ",indexMax)
    cromMax = poblacionAct[indexMax]
    
    minimosPoblacion.insert(numPoblacion,min) 
    maximosPoblacion.insert(numPoblacion,max)
    totalPorPoblacion.append(total)
    prom.append(total/len(valoresObjetivos))
 
    if(numPoblacion == 0):
        print('total poblacion inicial: ',totalPorPoblacion[numPoblacion])
        print('minimo de poblacion inicial: ',minimosPoblacion[numPoblacion])
        print('maximo de poblacion inicial: ',maximosPoblacion[numPoblacion],'En el cromosoma: ',cromMax)
        print('Promedio de poblacion inicial: ',prom[numPoblacion])
    else:
        print('total poblacion '+str(numPoblacion)+':',totalPorPoblacion[numPoblacion])
        print('minimo de poblacion '+str(numPoblacion)+':',minimosPoblacion[numPoblacion])
        print('maximo de poblacion '+str(numPoblacion)+':',maximosPoblacion[numPoblacion],'en el cromosoma: ',cromMax)
        print('Promedio de poblacion '+str(numPoblacion)+':',prom[numPoblacion])
    print('-------------------------------------------------------------------------------')

    return valoresObjetivos

def functionFitness(poblacionAct,numPoblacion,valoresObjetivos):
    print("long pob: ",len(poblacionAct))
    for i in range(len(poblacionAct)):
        fitness.insert(i,valoresObjetivos[i] / totalPorPoblacion[numPoblacion])  #a cada cromosoma se lo puntua según el valor/sobre total

def selectCromRuleta(fitness:list):
    ruleta = []
    maxFitt = 0 
    dif = 0 #por si no se completa la ruleta se la sumamos al que mas tiene para llegar a 100%
    rulPos = 0 #numero de la ruleta
    porcentajeFitt = []
    porcentajeTotal=0
    seleccion = [] #cromosomas seleccionados
    numWin = 0

    for i in range(len(fitness)):
        porcentajeFitt.insert(i,int(fitness[i]*100)) #fitness en forma de porcentaje a cada cromosoma
        if(porcentajeFitt[i] == 0):
            porcentajeFitt[i] = 1

        if(porcentajeFitt[i]>maxFitt):
            maxFitt = porcentajeFitt[i]

        porcentajeTotal+=porcentajeFitt[i]
    
    #completo fittnes para que llegue al 100% el total
    index = porcentajeFitt.index(maxFitt) #busco el indice del cromosoma con mas porcentaje

    if(porcentajeTotal<100):
        dif = 100 - porcentajeTotal
        porcentajeFitt[index]=porcentajeFitt[index]+dif #le sumo el porcentaje que faltaba al cromosoma candidato

    if(porcentajeTotal>100):
        dif = porcentajeTotal - 100
        porcentajeFitt[index]=porcentajeFitt[index]-dif #se lo resto, para que la suma sea del 100%, no se exceda

    #con dos for anidados, llenamos el arreglo ruleta segun los porcentajes de cada cromosoma, 
    #mas porcentaje tiene mas posiciones en el arreglo tendra ese cromosoma
    for c in range(len(fitness)):
        for _ in range(porcentajeFitt[c]):
            ruleta.insert(rulPos,c) #guardamos el indice, no el decimal del cromosoma
            rulPos+=1
    
    #ahora simulamos el giro de la ruleta(10 giros)
    for l in range(tamañoPoblacion):
        numWin = random.randint(0,99)
        seleccion.insert(l,ruleta[numWin])
    print('Ruleta resultante(Selección): ',seleccion)
    return seleccion

def crossover(poblacionAct:list,seleccion:list):
    nuevaPoblacion = []
    duplaPadres=[] #los dos que mas salieron en la ruleta
    longSeleccion = len(seleccion)

    j=0
    z=1
    for _ in range(longSeleccion//2):
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
            p12=[] #parte derecha del padre 1
            p21=[] #parte izquierda del padre 2
            p22=[]  #parte derecha del padre 2
            print('Punto de corte:',puntoCorte)
            p11 = poblacionAct[duplaPadres[0]][0:puntoCorte]
            p12 = poblacionAct[duplaPadres[0]][puntoCorte:30]
            p21 = poblacionAct[duplaPadres[1]][0:puntoCorte]
            p22 = poblacionAct[duplaPadres[1]][puntoCorte:30]
            print('Parte 1 padre1:', p11)
            print('Parte 2 padre1:', p12)
            print('Parte 1 padre2:', p21)
            print('Parte 2 padre2:', p22)
            #Ya obtenidos los cromosomas divididos por el punto de corte random, hacemos el cruzamiento
            hijo1=p11+p22
            hijo2=p12+p21
            
            hijo1Mut = mutacion(hijo1)
            hijo2MUt = mutacion(hijo2)
            
        else:

            hijo1Mut = mutacion(poblacionAct[duplaPadres[0]])
            hijo2MUt = mutacion(poblacionAct[duplaPadres[1]])
            
        nuevaPoblacion.append(hijo1Mut)
        nuevaPoblacion.append(hijo2MUt)

        duplaPadres.clear()
    return nuevaPoblacion

def mutacion(cromosoma):
    cromosomaMutado = cromosoma
    probMutRandom = (random.randint(0,100))/100
    if(probMutRandom < probabilidadMutacion):
        puntoCambio = random.randint(0,29)
        valor=cromosomaMutado.pop(puntoCambio)
        if(valor==0):
            cromosomaMutado.insert(puntoCambio,1)
        else:
            cromosomaMutado.insert(puntoCambio,0)
    return cromosomaMutado

def guardarDatos(nomPoblacion,poblacionAct:list):
    #obtengo el cromosoma como lista
    indexCrom = valoresObjetivos.index(maximosPoblacion[nomPoblacion])
    cromMax = poblacionAct[indexCrom]
    #convierto la lista binaria a decimal
    decimalMaximo = binaryToDecimal(cromMax)
    #convertimos de binario a string
    cromMax=format(decimalMaximo,'b')
    minimo=minimosPoblacion[nomPoblacion]
    maximo=maximosPoblacion[nomPoblacion]
    promedio=prom[nomPoblacion]

    sheet['B'+str(nomPoblacion+2)] = minimo
    sheet['C'+str(nomPoblacion+2)] = promedio
    sheet['D'+str(nomPoblacion+2)] = maximo
    sheet['E'+str(nomPoblacion+2)] = cromMax
    if(nomPoblacion==0):
        sheet['A'+str(nomPoblacion+2)] = 'Inicial'
    else:
        sheet['A'+str(nomPoblacion+2)] = nomPoblacion
    book.save('resultados_corridas_ruleta.xlsx')  

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
    plt.savefig('Grafica_ruleta.png')
    plt.show()
    




#PROGRAMA PRINCIPAL
book = Workbook()
sheet = book.active #hoja activa del excel
sheet['A1'] = 'Numero de Poblacion'
sheet['B1'] = 'Minimo'
sheet['C1'] = 'Promedio'
sheet['D1'] = 'Maximo'
sheet['E1'] = 'Cromosoma del maximo'


iniciarPoblacion()
valoresObjetivos = ActualValuesPoblation(0,poblacionInicial) #porque es la primera vez, despues invocamos con "poblation" por parametro
guardarDatos(0,poblacionInicial)
functionFitness(poblacionInicial,0,valoresObjetivos)
seleccion = selectCromRuleta(fitness)
siguientePoblacion = crossover(poblacionInicial,seleccion)
for j in range(1,cantidadCorridas+1):
    fitness.clear()
    valoresObjetivos.clear()
    valoresObjetivos = ActualValuesPoblation(j,siguientePoblacion)
    guardarDatos(j,siguientePoblacion)
    functionFitness(siguientePoblacion,j,valoresObjetivos)
    seleccion = selectCromRuleta(fitness)
    poblacionAnterior = siguientePoblacion
    siguientePoblacion = crossover(poblacionAnterior,seleccion)
grafica(maximosPoblacion,minimosPoblacion,prom)
