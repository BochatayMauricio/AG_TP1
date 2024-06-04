import heapq
import random 
from openpyxl import Workbook
from openpyxl.styles import Font
import matplotlib.pyplot as plt

#PARAMETROS
tamanoPoblacion = 10
cantidadCorridas = 200
probabilidadMutacion = 0.05
probabilidadCrossover = 0.75

#dominio de la funcion definido en el enunciado
dominio = [0,int(2**30)-1]
poblacionInicial = []
#en esta lista acumularemos el total de f(x) de cada poblacion, cada posicion refiere al numero de la poblacion
totalPorPoblacion = []
#Minimos, maximos de cada poblacion, cada posicion refiere al numero de la poblacion
minimosPoblacion = []
maximosPoblacion = []
#promedio de cada poblacion, cada posicion refiere al numero de la poblacion
promPorPoblacion = []

#fitness de cada cromosoma de la poblacion actual
fitness = []


#FUNCIONES

#Funcion definida --> devuelve valor de f(x) con x decimal
def funcionObjetivo(x): 
    return (x/((2**30)-1))**2


#Convertir a binario el cromosoma en decimal --> me da un cromosoma binario
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

#Convertir a decimal el cromosoma.
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
    for _ in range(tamanoPoblacion):
        num = random.randint(dominio[0],dominio[1])
        poblacionInicial.append(decimalToBinary(num))
    print('Poblacion Inicial: ')
    print(poblacionInicial)
    print('-------------------------------------------------------------------------------')

#Calcular valores f(x) para cada individuo de la poblacion actual y devuelve un arreglo de los mismos
def ActualValuesPoblation(numPoblacion,poblacionAct):
    j=0
    #Valor de la funcion objetivo en x, referencia el indice con el cromosoma de poblacion actual
    valoresObjetivos = []
    for i in poblacionAct:
        valoresObjetivos.insert(j,funcionObjetivo(binaryToDecimal(i))) 
        print('Cromosoma: ',i, 'Valor funcion: ',valoresObjetivos[j])
        j=j+1
    print('-------------------------------------------------------------------------------')
    maximo = max(valoresObjetivos)
    minimo = min(valoresObjetivos)
    total = 0
    indexMax= valoresObjetivos.index(maximo) #guardo el indice porque necesito saber el cromosoma correspondiente
    for i in range(len(poblacionAct)):
        total+=valoresObjetivos[i]
    
    print("Indice crom: ",indexMax)
    cromMax = poblacionAct[indexMax]

    minimosPoblacion.insert(numPoblacion,minimo)
    maximosPoblacion.insert(numPoblacion,maximo)
    totalPorPoblacion.append(total)
    promPorPoblacion.append(total/len(valoresObjetivos))
    
    if(numPoblacion == 0):
        print('total poblacion inicial: ',totalPorPoblacion[numPoblacion])
        print('minimo de poblacion inicial: ',minimosPoblacion[numPoblacion])
        print('maximo de poblacion inicial: ',maximosPoblacion[numPoblacion],'En el cromosoma: ',cromMax)
        print('Promedio de poblacion inicial: ',promPorPoblacion[numPoblacion])
    else:
        print('total poblacion '+str(numPoblacion)+':',totalPorPoblacion[numPoblacion])
        print('minimo de poblacion '+str(numPoblacion)+':',minimosPoblacion[numPoblacion])
        print('maximo de poblacion '+str(numPoblacion)+':',maximosPoblacion[numPoblacion],'En el cromosoma: ',cromMax)
        print('Promedio de poblacion '+str(numPoblacion)+':',promPorPoblacion[numPoblacion])
    print('-------------------------------------------------------------------------------')
    return valoresObjetivos

#Calcular fitness de cada cromosoma. A cada cromosoma se lo puntua segun el valor de f(x) del cromosoma sobre el total de la poblacion
def functionFitness(poblacionAct,numPoblacion,valoresObjetivos):
    print("long pob: ",len(poblacionAct))
    for i in range(len(poblacionAct)):
        fitness.append(valoresObjetivos[i] / totalPorPoblacion[numPoblacion])  #a cada cromosoma se lo puntua segun el valor/sobre total
    
#Seleccionar cromosomas mediante ruleta aplicando elitismo
def selectCromRuletaElite(fitness:list):
    
    ruleta = []
    maxFitt = 0 
    dif = 0 #por si no se completa la ruleta se la sumamos al que mas tiene para llegar a 100%
    porcentajeFitt = []
    porcentajeTotal=0
    seleccion = [] #cromosomas seleccionados
    numWin = 0
    elites=[]
    cantElites = int(0.20*tamanoPoblacion) 

    for i in range(len(fitness)):
        porcentajeFitt.insert(i,int(fitness[i]*100)) #fitness en forma de porcentaje a cada cromosoma
        
        if(porcentajeFitt[i] == 0):
            porcentajeFitt[i] = 1

        porcentajeTotal=porcentajeTotal+porcentajeFitt[i]

    # maxFitt = max(porcentajeFitt)
    # #completo fitness para que llegue al 100% el total
    # index = porcentajeFitt.index(maxFitt) #busco el indice del cromosoma con mas porcentaje

    # if(porcentajeTotal<100):
    #     dif = 100 - porcentajeTotal
    #     porcentajeFitt[index]=porcentajeFitt[index]+dif #le sumo el porcentaje que faltaba al cromosoma candidato

    # if(porcentajeTotal>100):
    #     dif = porcentajeTotal - 100
    #     porcentajeFitt[index]=porcentajeFitt[index]-dif #se lo resto, para que la suma sea del 100%, no se exceda
    
    print("porcentaje total:",porcentajeFitt)

    #ELITISMO (buscamos los n maximos correspondientes al 20% de la longitud de la poblacion)
    #Tenemos que volver a buscarlo porque anteriormente modificamos al de mejor fittnes, entonces no me sirve el maxFitt
    maxFitness = heapq.nlargest(cantElites,fitness)
    indiceDelAnterior = -1
    for valor in maxFitness:
        indiceMax = fitness.index(valor)
        if(indiceMax in elites): 
            indiceDelAnterior = indiceMax
            indice = fitness.index(valor,indiceDelAnterior,tamanoPoblacion)
            elites.append(indice)
        else:
            indice = fitness.index(valor)
            elites.append(indice)
    
    print("Fitness maximos encontrados: ",maxFitness)
    print("Fitness de toda la poblacion: ",fitness)
    print("Elites(indice de los crom de mayor fitness): ",elites)
    for j in range(cantElites):
        seleccion.insert(j,elites[j])
        porcentajeTotal = porcentajeTotal - porcentajeFitt[elites[j]]
        porcentajeFitt[elites[j]]=0

    #llenamos la lista ruleta segun los porcentajes de cada cromosoma, 
    #mas porcentaje tiene, mas posiciones en la lista "ruleta" tendra ese cromosoma 
    for c in range(tamanoPoblacion):
        for _ in range(porcentajeFitt[c]):
            ruleta.append(c) #guardamos el indice, no el decimal del cromosoma

    print("total posiciones: ",porcentajeTotal)
    print("ruleta: ",ruleta)
    #ahora simulamos el giro de la ruleta (tamanoPoblacion-cantElites giros)
    for l in range(cantElites,tamanoPoblacion):
        numWin = random.randint(0,porcentajeTotal-1)
        seleccion.insert(l,ruleta[numWin])

    print('Ruleta resultante(Seleccion): ',seleccion)
    return seleccion

#Realizar crossover entre los cromosomas seleccionados por la ruleta y posteriormente mutacion.
def crossover(poblacionAct:list,seleccion:list):
    nuevaPoblacion = []
    duplaPadres=[] #los dos que mas salieron en la ruleta
    cantElites = int(0.20*tamanoPoblacion)
    longSeleccion = len(seleccion) - cantElites #Porque los n primeros son los elites, pasan directo a la nueva poblacion
    
    #paso a la siguiente poblacion los elites seleccionados
    for i in range(cantElites):
        print('elite a agregar: ',poblacionAct[seleccion[i]])
        nuevaPoblacion.append(poblacionAct[seleccion[i]])
   
    print("Nueva poblacion con los elites de la anterior: ",nuevaPoblacion)
    j=cantElites
    z=cantElites+1
    for _ in range(longSeleccion//2):
        duplaPadres.insert(0,seleccion[j])
        duplaPadres.insert(1,seleccion[z])
        j=j+2
        z=z+2
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
            hijo2Mut = mutacion(hijo2)

            nuevaPoblacion.append(hijo1Mut)
            nuevaPoblacion.append(hijo2Mut)
            
        else:

            hijo1Mut = mutacion(poblacionAct[duplaPadres[0]])
            hijo2Mut = mutacion(poblacionAct[duplaPadres[1]])
            
            nuevaPoblacion.append(hijo1Mut)
            nuevaPoblacion.append(hijo2Mut)

        duplaPadres.clear()
    print("nueva poblacion: ",nuevaPoblacion)
    return nuevaPoblacion

#Realizar mutacion de los cromosomas recibidos de la funcion crossover
def mutacion(cromosoma):
    probMutRandom = (random.randint(0,100))/100
    if(probMutRandom < probabilidadMutacion):
        puntoCambio = random.randint(0,29)
        valor=cromosoma.pop(puntoCambio)
        if(valor==0):
            cromosoma.insert(puntoCambio,1)
        else:
            cromosoma.insert(puntoCambio,0)
    return cromosoma

#Generar tablas de resultados obtenidos
def guardarDatos(numPoblacion,poblacionAct:list):
    #obtengo el cromosoma como lista
    indexCrom = valoresObjetivo.index(maximosPoblacion[numPoblacion])
    cromMax = poblacionAct[indexCrom]
    #convierto la lista binaria a decimal
    decimalMaximo = binaryToDecimal(cromMax)
    #convertimos de binario a string
    cromMax=format(decimalMaximo,'b')

    minimo=minimosPoblacion[numPoblacion]
    maximo=maximosPoblacion[numPoblacion]
    promedio=promPorPoblacion[numPoblacion]

    sheet['B'+str(numPoblacion+2)] = minimo
    sheet['C'+str(numPoblacion+2)] = promedio
    sheet['D'+str(numPoblacion+2)] = maximo
    sheet['E'+str(numPoblacion+2)] = str(cromMax)
    if(numPoblacion==0):
        sheet['A'+str(numPoblacion+2)] = 'Inicial'
    else:
        sheet['A'+str(numPoblacion+2)] = numPoblacion
    book.save('resultados_corridas_ruleta_elitismo.xlsx')  

#Generar graficas de los resultados obtenidos
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
    plt.savefig('Grafica_ruleta_elitismo.png')
    plt.show()
    
# ----------------------------------------------------------------
#PROGRAMA PRINCIPAL
book = Workbook()
sheet = book.active #hoja activa del excel
sheet['A1'] = 'Numero de Poblacion'
sheet['B1'] = 'Minimo'
sheet['C1'] = 'Promedio'
sheet['D1'] = 'Maximo'
sheet['E1'] = 'Cromosoma del maximo'

iniciarPoblacion()
valoresObjetivo = ActualValuesPoblation(0,poblacionInicial) #porque es la primera vez, despues invocamos con "poblation" por parametro
guardarDatos(0,poblacionInicial)
functionFitness(poblacionInicial,0,valoresObjetivo)
seleccion = selectCromRuletaElite(fitness)
siguientePoblacion = crossover(poblacionInicial,seleccion)
for j in range(1,cantidadCorridas+1):
    fitness.clear()
    valoresObjetivo.clear()
    valoresObjetivo = ActualValuesPoblation(j,siguientePoblacion)
    guardarDatos(j,siguientePoblacion)
    functionFitness(siguientePoblacion,j,valoresObjetivo)
    seleccion = selectCromRuletaElite(fitness)
    poblacionAnterior = siguientePoblacion
    siguientePoblacion = crossover(poblacionAnterior,seleccion)
grafica(maximosPoblacion,minimosPoblacion,promPorPoblacion)
