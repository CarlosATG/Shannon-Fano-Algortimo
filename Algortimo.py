"""
Algoritmo de codificacion Shannon Fano analizando cada 2 bytes, 16 bits, de informacion y 
determinando la probabiliad de aparicion de cada simbolo. 
Despues, empezar a partir la infomracion por promedios equiprobables para asignarle un valor al simbolo.
De esta manera el valor que mas aparezca en el 

"""
import numpy as np
def Binario (promedio):
    # Prueba de un promedio=[0.3,0.25,0.2,0.12,0.08,0.05]
    lista_fini=[]# Posiciones en la lista
    lista_fini.append(0)
    lista_fini.append(len(promedio)-1)
    PRUEBA =['']*len(promedio)
    while True:
        if len(lista_fini) == 1:
            break
        Incio=lista_fini[0]
        Final = lista_fini[1]
        Izquierda=0
        Vida= sum(promedio[Incio:Final+1])
        Suma_promedios = Vida / 2
        for i in range(Incio, Final):
            Izquierda += promedio[i]
            if Izquierda >=Suma_promedios :#Encuentro cuando son equiprobables
                memoria=Final
                Final=i
                lista_fini.append(i)
                lista_fini.sort()
                break
        if Incio == i:
            PRUEBA[i]+= '0'
            PRUEBA[i+1]+='1'
        else:
            for i in range(Incio, Final+1):
                    PRUEBA[i] += '0'
            for i in range(Final+1, memoria+1):
                    PRUEBA[i]+='1'
        if lista_fini[0]== lista_fini[1]:
            if lista_fini[-1]==lista_fini[-2]+1:
                del lista_fini[0]
                del lista_fini[0]
                continue
            elif len(lista_fini)==3:
                del lista_fini[0]
                continue
            del lista_fini[0]
            del lista_fini[0]
            del lista_fini[0]
            lista_fini.append(memoria+1)
            lista_fini.sort()
            if lista_fini[0]==lista_fini[1]:
                 del lista_fini[0]
    return PRUEBA;
def get_hex(Encoded):
    Hexalist=[]
    for i in range (len(Encoded)):
        Binary=int(Encoded[i], 2)
        Hexalist.append(Binary)
    np_Hexalist=np.array(Hexalist)
    np_Hexalist = np_Hexalist.astype('H')
    return np_Hexalist;
dtype = np.dtype('H')
try:
    with open("FILE", "rb") as f:
        numpy_data = np.fromfile(f, dtype)
        print(numpy_data)
        lenght = len(numpy_data)
        counter = []
        unique, counts = np.unique(numpy_data, return_counts=True)
        lover=dict(zip(unique, counts))
        promedio=[]
        Aparicion= dict(sorted(lover.items(), key=lambda item: item[1], reverse=True))
        Valores_en_Orden=[]
        for key in Aparicion.keys():
            Valores_en_Orden.append(key)
        print(Aparicion)
        for value in Aparicion.values():
            promedio.append(value/lenght)
        print(lenght, promedio)
        Bincoded= Binario(promedio)
        Hexcoded= get_hex(Bincoded)
        Hexadict=dict(zip(Valores_en_Orden, Hexcoded))
        Codificado=[]
        for value in numpy_data:
            if value in Hexadict:
                Codificado.append(Hexadict[value])
        np_Codificado= np.array(Codificado)
        with open("File", "wb") as f:
             f.write(np_Codificado)
        with open("File", "rb") as f:
            numpy_data = np.fromfile(f, 'H')
            posibilidades= list(Hexadict.values())
            print(numpy_data[184])
            DeCoded=[]
            for i in range(len(numpy_data)):
                founded= list(Hexadict.keys())[list(Hexadict.values()).index(numpy_data[i])]
                DeCoded.append(founded)
            print(DeCoded)
            np_DeCoded = np.array(DeCoded)
            print(np_DeCoded)
            np_DeCoded = np_DeCoded.astype(dtype)
            print(np_DeCoded)
        with open("FILE","wb") as f:
            f.write(np_DeCoded)
except IOError:
    print('Error While Opening the file!')
