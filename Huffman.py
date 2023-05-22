
from bitarray import bitarray
import numpy as np
import heapq
from collections import defaultdict

# mapear el valor codificado de cada simbolo
codigo = {}



# Creamos nuestra clase de arbol donde los objetos seran determiandos por el simbolo y su probabilidad
class ArbolNodo:
	#Los objetos tendran las siguientes caracteristicas
	def __init__(self, data, apariciones):
		self.izq = None #Rama a la izquierda
		self.der = None #A la derecha
		self.data = data #Simbolo
		self.apariciones = apariciones #Veces que aparece el simbolo
	#Siempre trabajamos con la menos frecuencia
	def __lt__(self, other):
		return self.apariciones < other.apariciones

#funcion para guardar los simbolos con sun codificacion en binario
def Valores(raiz, bits):
	if raiz is None:
		return
	if raiz.data != '$':
		codigo[raiz.data] = bits
	#El algortimos nos dice que al valor izquierdo le damos un 0 y al derecho le damos un 1
	Valores(raiz.izq, bits + "0")
	Valores(raiz.der, bits + "1")

#Algortimos para crear el alrbol bianrio
def AlgoritmoHuff(size):
	global Arbol #Vamos a usar esta variable en varios puntos, por eso es global
	for key in apariciones: #los diccionarios no permiten tener la misma deficion mas de una vez
		Arbol.append(ArbolNodo(key, apariciones[key]))
	heapq.heapify(Arbol)
	while len(Arbol) != 1: #cuando sea 1, significa que hemos llegamos a la raiz
		#Creamos la rama del lado ziquierdo
		izq = heapq.heappop(Arbol)
		#Creamos la rama del lado derecho
		der = heapq.heappop(Arbol)
		#El valor de la rama es la suma de apariciones
		rama = ArbolNodo('$', izq.apariciones + der.apariciones)
		rama.izq = izq
		rama.der = der
		heapq.heappush(Arbol, rama)
	Valores(Arbol[0], "")

# Guardar las veces que aparecen los simbolos en el diccionario
apariciones = defaultdict(int)
# funcion para determinar cuantas veces aprecen los simbolos
def calc_apariciones(simbolos, longitud):
	for i in range(longitud):
		apariciones[simbolos[i]] += 1

# funcion que hace iteracion de nuestra cadena de bits para determianr cual es su valor
def decodificar(raiz, s):
	Original = ""
	actual = raiz
	n = len(s)
	for i in range(n):
		if s[i] == '0':
			actual = actual.izq
		else:
			actual = actual.der

		# reached leaf node
		if actual.izq is None and actual.der is None:
			Original += actual.data
			actual = raiz
	return Original #+ '\0'

# main
if __name__ == "__main__":
	Arbol = []
	try:
		with open("Txtdeprueba.txt", "rb") as f:#Abrimos cualquier archivo en modo binario
			numpy_data = np.fromfile(f, 'H')
	except IOError:
		print('Error While Opening the file!')
	simbolos=[]#Lista de simbolos que se encuentran en formato de numpy
	print(numpy_data)
	#ciclamos los simbolos a nuestra lista y los convertimos en str
	for i in range(len(numpy_data)):
		simbolos.append(str(numpy_data[i]))
	print("Aqui!!!",simbolos)
	Codificado, Decodificado = "", ""
	calc_apariciones(simbolos, len(simbolos))# llamamos una funcion que calcule la frecuencia, veces que cada simbolo aparece
	AlgoritmoHuff(len(simbolos))#Nuestra funcion que codifica de acuerdo al algoritmo de huffman
	print("Character With their Frequencies:")
	for key in sorted(codigo, reverse=True):
		print(key, codigo[key])
	for i in simbolos:
		Codificado += codigo[i]
	print("\nEncoded Huffman data:")
	Bitstring=bitarray(Codificado) #Cinvertimos nuestra cadena de caracteres, str, a una de bits
	print(Bitstring)
	print(len(Bitstring))
	with open("HEXACODED.txt", "wb") as f:  # Lo escribimos en un nuevo archivo
		Bitstring.tofile(f) #escribimos nuestra cadena a un archivo
	Decodificado = decodificar(Arbol[0], Codificado)
	print("\nDecoded Huffman Data:")
