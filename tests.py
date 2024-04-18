num = 769051028

# binary=[]
# while (num>0):
#     digit  = num%2
#     num = int(num//2)
#     binary.append(digit)
# binary.reverse()

# COMO PALABRA
binario = format(num, 'b')

# COMO ARRAY
binario_array = [int(bit) for bit in binario]  #Binario a lista de 0s y 1s

# BINARIO A DECIMAL
decimal = int(binario,2)


print("Numero decimal: ",num)
print("Pasado a binario: ",binario)
print("Binario como lista: ",binario_array)
print("Pasado a decimal: ",decimal)