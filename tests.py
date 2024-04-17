num = 769051028

# binary=[]
# while (num>0):
#     digit  = num%2
#     num = int(num//2)
#     binary.append(digit)
# binary.reverse()

# COMO ARRAY
# binario = bin(num)
# binario_solo = binario[2:]  #Elimina el prefijo '0b'
# binario_array = [int(bit) for bit in binario_solo]  #Binario a lista de 0 y 1

# COMO PALABRA
binario = format(num, 'b')

# BINARIO A DECIMAL
decimal = int(binario,2)


print("Numero decimal: ",num)
print("Pasado a binario: ",binario)
print("Pasado a decimal: ",decimal)