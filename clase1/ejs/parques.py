import pandas as pd

def leer_parque(nombre_archivo, parque):
    res = []
    df = pd.read_csv(nombre_archivo)
    #df.info()
    for f in df.iterrows():
        if f[1]['espacio_ve'] == parque:
            res.append(f[1].to_dict())
    return res

l = leer_parque(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv','GENERAL PAZ')
#print(len(l))

def especies(lista_arboles):
    res = []
    for arbol in lista_arboles:
        if arbol['nombre_com'] not in res:
            res.append(arbol['nombre_com'])
    return res

#print(especies(l))

def contar_ejemplares(lista_arboles):  
    res = {}
    for arbol in lista_arboles:
        esp = arbol['nombre_com']
        if esp not in res:
            res[esp] = 1
        else:
            res[esp] += 1
    return res

#print(contar_ejemplares(l)['Jacarandá'])
#print(contar_ejemplares(leer_parque(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv','ANDES, LOS'))["Tilo"])
#print(contar_ejemplares(leer_parque(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv','CENTENARIO'))['Laurel'])

def obtener_alturas(lista_arboles, especie):
    res = []
    for arbol in lista_arboles:
        if arbol['nombre_com'] == especie:
            res.append(float(arbol['altura_tot']))
    return res

#print(obtener_alturas(l, 'Jacarandá'))

def altura_maxima(lista_arboles, especie):
    res = 0
    for n in obtener_alturas(lista_arboles, especie):
        if n > res:
            res = n
    return res

def altura_promedio(lista_arboles, especie):
    lista = obtener_alturas(lista_arboles, especie)
    return sum(lista)/len(lista)

#print('General Paz: Max = ' + str(altura_maxima(l, "Jacarandá")) + ', Prom = ' + str(altura_promedio(l, "Jacarandá")))
andes = leer_parque(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv','ANDES, LOS')
#print('Los Andes: Max = ' + str(altura_maxima(andes, "Jacarandá")) + ', Prom = ' + str(altura_promedio(andes, "Jacarandá")))
centenario = leer_parque(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv','CENTENARIO')
#print('Centenario: Max = ' + str(altura_maxima(centenario, "Jacarandá")) + ', Prom = ' + str(altura_promedio(centenario, "Jacarandá")))

def obtener_inclinaciones(lista_arboles, especie):
    res = []
    for arbol in lista_arboles:
        if arbol['nombre_com'] == especie:
            res.append(float(arbol['inclinacio']))
    return res

#print(obtener_inclinaciones(l, 'Jacarandá'))

def especimen_mas_inclinado(lista_arboles):
    especies_lista = especies(lista_arboles)
    maximo = 0
    especie_mas_inclinada = especies_lista[0]
    for esp in especies_lista:
        if max(obtener_inclinaciones(lista_arboles, esp)) > maximo:
            maximo = max(obtener_inclinaciones(lista_arboles, esp))
            especie_mas_inclinada = esp
    return especie_mas_inclinada + ' inlinado ' + str(maximo) + ' grados.'

#print(especimen_mas_inclinado(centenario))

def inclinacion_promedio(lista_arboles, especie):
    inclinaciones = obtener_inclinaciones(lista_arboles, especie)
    return sum(inclinaciones)/len(inclinaciones)

def especie_promedio_mas_inclinada(lista_arboles):
    especies_lista = especies(lista_arboles)
    especie_mas_inlcinada = especies_lista[0]
    promedio = inclinacion_promedio(lista_arboles, especie_mas_inlcinada)
    for esp in especies_lista:
        if inclinacion_promedio(lista_arboles, esp) > promedio:
            especie_mas_inlcinada = esp
            promedio = inclinacion_promedio(lista_arboles, esp)
    return especie_mas_inlcinada + ' tiene una inclinación promedio de ' + str(promedio) + ' grados.'

#print(especie_promedio_mas_inclinada(andes))