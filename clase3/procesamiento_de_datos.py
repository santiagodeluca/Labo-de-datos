empleado_01 = [
    {'DNI' : 33456234, 'Edad' : 40, 'Cantidad de hijos' : 0, 'Salario' : 25000},
    {'DNI' : 20222333, 'Edad' : 45, 'Cantidad de hijos' : 2, 'Salario' : 20000},
    {'DNI' : 45432345, 'Edad' : 41, 'Cantidad de hijos' : 1, 'Salario' : 10000}
    ]

def  superanSalarioActividad01(matriz, umbral):
    res = []
    for fila in matriz: 
        if fila['Salario'] > umbral:
            res.append(fila)
    return res

#print(superanSalarioActividad01(empleado_01, 15000))

empleado_02 = empleado_01 + [
    {'DNI' : 43967304, 'Edad' : 37, 'Cantidad de hijos' : 0, 'Salario' : 12000},
    {'DNI' : 42236276, 'Edad' : 36, 'Cantidad de hijos' : 0, 'Salario' : 18000}
    ]

#print(superanSalarioActividad01(empleado_02, 15000))

empleado_03 = [
    {'DNI' : 33456234, 'Salario' : 25000, 'Edad' : 40, 'Cantidad de hijos' : 0},
    {'DNI' : 20222333, 'Salario' : 20000, 'Edad' : 45, 'Cantidad de hijos' : 2},
    {'DNI' : 45432345, 'Salario' : 10000, 'Edad' : 41, 'Cantidad de hijos' : 1},
    {'DNI' : 43967304, 'Salario' : 12000, 'Edad' : 37, 'Cantidad de hijos' : 0},
    {'DNI' : 42236276, 'Salario' : 18000, 'Edad' : 36, 'Cantidad de hijos' : 0}
    ]

#print(superanSalarioActividad01(empleado_03, 15000))
# sigue funcionando porque para hacer las filas use diccionarios, sino habria que cambiar la fucnion

empleado_04 = [['DNI', 'Edad', 'Cantidad de hijos', 'Salario'], 
               [33456234,40,0,25000],
               [20222333,45,2,20000],
               [45432345,41,1,10000],
               [43967304,37,0,12000],
               [42236276,36,0,18000]]

def superanSalarioActividad04(matriz, umbral):
    res = []
    for fila in matriz:
        if isinstance(fila[0], int) and fila[3] > umbral:
            res.append(fila)
    return res 

#print(superanSalarioActividad04(empleado_04, 15000))

"""
1. Agregar mas filas no modifico la funcion, pero alternar el orden, 
si las filas no las planteaba como diccionarios, implicaria cambiar el "indice"
que indicaria la columna.
2. Cambiar la forma de representar la matriz requirio que cambie la forma de recorrer
en el ciclo la matriz. 
3. Ahorrar tiempo principalmente y tambien usar funciones mas "seguras" ya que al usar
bibliotecas muy utilizadas el codigo de esas funciones fue muy revisado y utilizado, 
y suficientemente testeado para practicamente asegurar que no tiene errores. 
"""
               
