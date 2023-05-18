"""
Carlos Andres Torres

Algoritmo de codificacion Shannon Fano analizando cada 2 bytes, 16 bits, de informacion y
determinando la probabiliad de aparicion de cada simbolo.
Despues, empezar a partir la infomracion por promedios equiprobables para asignarle un valor al simbolo.
De esta manera el valor que mas aparezca tendra como valor un 0 y el que tenga menor probabilidad de aparecer sera
el mas grande. Siguiendo la idea de que la informacion tiene una relacion inversa con su probabilidad de aparecer

"""
import numpy as np
def Binario (promedio): #Funcion para codificar a partir de la cantidad de veces que aparece un simbolo
    # para comprobar la eficiencia del ciclo promedio=[0.3,0.25,0.2,0.12,0.08,0.05]
    lista_fini=[]# Posiciones en la lista para ir partiendo y evaluando valores
    lista_fini.append(0)#La posicion de inicio
    lista_fini.append(len(promedio)-1)#El ultimo lugar asi, tenemos una lista [0,x], donde x es el ultimo lugar de los promedios
    PRUEBA =['']*len(promedio)#Creamos nuestra lista para los valores codificado con longitud igual a la de los promedios, ya que hay esa cantidad de simbolos
    while True: #Simple ciclo que nos permite codificar sin importar el tamanio
        if len(lista_fini) == 1:#Salimos del programa si nuestra lista de posiciones solo tiene un valor
            break
        Incio=lista_fini[0]#Indicamos el valor de incio para evaluar
        Final = lista_fini[1]#Indicamos el valor final a evaluar
        Izquierda=0#Contador de probabilidades empezando del lado izquierdo, en el caso inicial del valor en la posicion 0
        Equiprobable= sum(promedio[Incio:Final+1])#Evaluamos un valor pro medio de la suma de probailidades en la posicion de la lista promedio
        #que empiece en Inicio y termine en el ultimo lugar
        Suma_promedios = Equiprobable / 2 #Tenemos la suma de los promedios en ese intervalo
        for i in range(Incio, Final):#Vamos a movernos en ese rango, ya que las posiciones van a ir cambiando
            Izquierda += promedio[i]#Sumador de promedios
            if Izquierda >=Suma_promedios :#Encuentro cuando son equiprobables para romper el ciclo
                memoria=Final#Creamos un valor que recuerda hasta donde llegar
                Final=i# Posicion en la lista donde la suma izquierda es equiprobable a los demas del lado derecho
                lista_fini.append(i)#Este valor lo agregamos a nuestra lista de posiciones importantes
                lista_fini.sort()#Acomodamos los valores, ya que al agregarlo se va al final de la lista y lo queremos en su posicion intermedia
                break#salimos del for
        if Incio == i:#Si inicio, posicion en al lsita, es igual a la nueva posicion calculada
            #Esto nos sirve para no atorarnos
            PRUEBA[i]+= '0'#agregamos un 0 a esta posicion
            PRUEBA[i+1]+='1'#Agregamos un 1 a la siguiente
        else:#Si no son iguales los valores, entonces
            for i in range(Incio, Final+1):#Rango desde el inicio hasta el valor intermedio +1, dada la naturaleza del for se detiene un valor antes
                    PRUEBA[i] += '0'#lado izquierdo se pone un 0 hasta llegar a este valor intermedio
            for i in range(Final+1, memoria+1):#Comenzamos un valor a la derecha despues para no agregar un 1 al mismo que ya tiene un nuevo 0
                    PRUEBA[i]+='1'
        if lista_fini[0]== lista_fini[1]:#Condicion en caso de que haya valor iguales en als primeras dos posiciones de la lista de posiciones
            #Como agregamos i como un indicador, puede que al ser igual que inicio tengamos un problema
            if lista_fini[-1]==lista_fini[-2]+1:#En caso de que los dos ultimos valores sean diferentes por un 1 vamos a borrar, se entiende mas adelante
                del lista_fini[0]
                del lista_fini[0]
                continue
            elif len(lista_fini)==3:#Si solo tenemos 3 valores, entonces nos falta evaluar un intervalo, por lo que solo borramos la posicion de inicio
                del lista_fini[0]
                continue
            #SI no se cumple lo anterior entonces borramos los tres primeros valores.
            del lista_fini[0]
            del lista_fini[0]
            del lista_fini[0]
            lista_fini.append(memoria+1)#Despues agregamos el valor que teniamos originalmente como final +1 para no vovler a evaluar el mismo numero
            lista_fini.sort()#Acomodamos la lista
    return PRUEBA;#Regresamos la lista con el codigo de valores bianrios

#Funcion para hacer los valores hexadecimal
def get_hex(Encoded):
    Hexalist=[]#Creamos la lista
    for i in range (len(Encoded)):#Queremos un rango igual al valor de la cantidad de valores que tenemos
        Binary=int(Encoded[i], 2)#Encontramos su base 2
        Hexalist.append(Binary)#lo agregamos a la lista
    np_Hexalist=np.array(Hexalist)#Creamos un arreglo
    np_Hexalist = np_Hexalist.astype('H')#Lo hacemos base 8
    return np_Hexalist;#Regresamos la nueva lsita codificada

dtype = np.dtype('H')
#Main, aqui subimos los archivos, creamos el diccionario y lo decodificamos
try:
    with open("Txtdeprueba.txt", "rb") as f:#Abrimos cualquier archivo en modo binario
        numpy_data = np.fromfile(f, dtype)
        lenght = len(numpy_data) #Vamos a necesitar la longitud de infomracion, por lo que lo guardamos en una variable
        unique, counts = np.unique(numpy_data, return_counts=True)# Nos da los valore y las veces que aparecen
        Acomodado=dict(zip(unique, counts))#Creamos un diccionario para guardar los valores y su cantidad de apariciones
        Aparicion= dict(sorted(Acomodado.items(), key=lambda item: item[1], reverse=True))#Acomodamos el diccionario por orden del valor: veces que aparece
        promedio=[]#Lista para gaurdar el promedio de cada simbolo
        Valores_en_Orden=[]#Aqui guardamos los valores en orden
        for key in Aparicion.keys():#Guardamos los valores acomodados
            Valores_en_Orden.append(key)
        for value in Aparicion.values():#Calculamos el promedio de cada simbolo
            promedio.append(value/lenght)#Promedio es igual a cantidad de apariciones entre el total
        Bincoded= Binario(promedio)#Llamamos funcion que codifica y le da valor de 0 y 1 de acuerdo a promedio
        Hexcoded= get_hex(Bincoded)#Hacemos legible este codigo
        Hexadict=dict(zip(Valores_en_Orden, Hexcoded))#Creamos un diccionario con el simbolo y su valor
        Codificado=[]#Vamos a codificar nuestra infomacion con el esquema que calculamos
        for value in numpy_data:#Para cada valor en la cadena original de bytes
            if value in Hexadict:#Si los 2 bytes estan en nuestros diccionario
                Codificado.append(Hexadict[value])#NUestra lista tendra el valor codificado
        np_Codificado= np.array(Codificado)#Lo hacemos un arreglo de numpy
        with open("HEXACODED.txt", "wb") as f:#Lo escribimos en un nuevo archivo
             f.write(np_Codificado)
        with open("HEXACODED.txt", "rb") as f:#Decodificamos uno a uno
            numpy_data = np.fromfile(f, 'H')
            posibilidades= list(Hexadict.values())#Usamos el diccionario para obtener los valores
            DeCoded=[]#lista para guardar datos decodificados
            for i in range(len(numpy_data)):#ciclo para encontrar el valor
                founded= list(Hexadict.keys())[list(Hexadict.values()).index(numpy_data[i])]#Buscamos el valor y regresamos la llave
                DeCoded.append(founded)#Agregamos la llave a esta nueva lista
            np_DeCoded = np.array(DeCoded)#lo hacemos un arreglo de numpy
            np_DeCoded = np_DeCoded.astype(dtype)#le damos el tipo de dato correcto
        with open("decodificado.txt","wb") as f:#escrbimos esto en un nuevo archivo
            f.write(np_DeCoded)
except IOError:
    print('Error While Opening the file!')
