"""
Materia: Laboratorio de datos - FCEyN - UBA
Trabajo práctico 02
Alumnos : Santiago De Luca, Federico Borruat, Lautaro Aguilar
Fecha  : 2025-03-
Descripcion : Este archivo está dividido en cuatro partes:
              - Procesamientos de datos
              - Análisis de datos (consultas y visualizaciones)
              - Cálculo de métricas GQM
              - Recorte de tablas para el informe
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import duckdb as dd
#import seaborn as sns
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
#%% Lectura de datos
data = pd.read_csv('mnist_c_fog_tp.csv', index_col=0)
#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #                     CLASIFICACIÓN BINARIA                            # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#%%===========================================================================
# Filtrado binario del dataset
#=============================================================================
binario = data[(data['labels'] == 0) | (data['labels'] == 1)].reset_index()

cantidad_0 = (binario['labels'] == 0).sum() # 6903
cantidad_1 = (binario['labels'] == 1).sum() # 7877

proporcion = cantidad_0 * 100 / len(binario) # 46,7% son 0 

largo_test = int(len(binario) * 0.15) # Nuestro conjunto de test será el 15% del de desarrollo
test = binario[:largo_test]
train = binario[largo_test:].reset_index()
#%%===========================================================================
# Primeros acercamientos al modelo
#=============================================================================
#%% Probamos con tres píxeles del centro a diferentes alturas

alturas_importantes = [7, 13, 19]
tam_imagen = (28, 28, 3) 
im = np.ones(tam_imagen, dtype=np.uint8) * 255  

exactitudes = []

colores = [
    [255, 0, 0],   
    [0, 255, 0],   
    [0, 0, 255]    
]

for indice_trio, i in enumerate(alturas_importantes):  
    pix1 = i * 28 + 12
    pix2 = i * 28 + 13
    pix3 = i * 28 + 14
    selected_pixels = [pix1, pix2, pix3]

    X = binario[[str(pix1), str(pix2), str(pix3)]]
    y = binario['labels']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    exactitud = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo con tres píxeles del centro de fila {i}: {exactitud * 100:.3f}%")

    exactitudes.append(f"Fila {i}: {exactitud * 100:.2f}%")

    color = colores[indice_trio]  
    for index in selected_pixels:
        y, x = divmod(index, 28)  
        im[y, x] = color  

#%% Graficamos los píxeles elegidos
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, extent=[0, 28, 28, 0])

ax.set_xticks(np.arange(28))
ax.set_yticks(np.arange(28))
ax.set_xticklabels(np.arange(28), fontsize=6, rotation=90)  
ax.set_yticklabels(np.arange(28), fontsize=6)

plt.grid(color="gray", linestyle="--", linewidth=0.5)

for indice_trio, color in enumerate(colores):
    ax.scatter([], [], color=np.array(color) / 255, label=exactitudes[indice_trio])

ax.legend(loc='upper right', fontsize=10, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en valores del centro (binario, K=3)", fontsize=14)
plt.show()
#%% Probamos con tres píxeles en distintos bordes
arriba_centro = ['13','14','15']
X = binario[arriba_centro]  
y = binario['labels']  

exactitudes = []

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con valores del centro de la primera fila: {exactitud * 100:.3f}%")

arriba_izq = ['0','1','2']
X = binario[arriba_izq]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con primeros píxeles de arriba a la izquierda: {exactitud * 100:.3f}%")

centro_izq = [str(28*12),str(28*13),str(28*14)]
X = binario[centro_izq]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con primeros píxeles del centro a la izquierda: {exactitud * 100:.3f}%")

centro_der = [str((28*12) + 27),str((28*13)+27),str((28*14)+27)]
X = binario[centro_der]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con primeros píxeles de centro a la derecha: {exactitud * 100:.3f}%")

#%% Graficamos los píxeles elegidos
tam_imagen = (28, 28, 3) 
im = np.ones(tam_imagen, dtype=np.uint8) * 255  

for index in np.array(arriba_centro, dtype=int):
    f, c = divmod(index, 28)  
    im[f, c] = [128,0,128]
for index in np.array(arriba_izq, dtype=int):
    f, c = divmod(index, 28)  
    im[f, c] = [255,255,0]
for index in np.array(centro_izq, dtype=int):
    f, c = divmod(index, 28)  
    im[f, c] = [255,165,0]
for index in np.array(centro_der, dtype=int):
    f, c = divmod(index, 28)  
    im[f, c] = [165,42,42]
    
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, extent=[0, 28, 28, 0])

ax.set_xticks(np.arange(28))
ax.set_yticks(np.arange(28))
ax.set_xticklabels(np.arange(28), fontsize=6, rotation=90)  
ax.set_yticklabels(np.arange(28), fontsize=6)

plt.grid(color="gray", linestyle="--", linewidth=0.5)

ax.scatter([], [], color=np.array([128,0,128]) / 255, label="Primera fila centro: " + exactitudes[0])
ax.scatter([], [], color=np.array([255,255,0]) / 255, label="Primera izquierda: " + exactitudes[1])
ax.scatter([], [], color=np.array([255,165,0]) / 255, label="Centro izquierda: " + exactitudes[2])
ax.scatter([], [], color=np.array([165,42,42]) / 255, label="Centro derecha: " + exactitudes[3])

ax.legend(loc='lower right', fontsize=10, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en valores de bordes (binario, K=3)", fontsize=14)
plt.show()

#%% Probamos con filas enteras
exactitudes = []

# Fila central
central = np.arange(13*28, 14*28)
fila_central = central.astype(str)
X = binario[fila_central]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con todos los pixeles de la fila central : {exactitud * 100:.3f}%")

# Primera fila
primera = np.arange(0, 28)
primera_fila = primera.astype(str)
X = binario[primera_fila]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con todos los pixeles de la primera fila: {exactitud * 100:.3f}%")

#%% Graficamos las filas elegidas
tam_imagen = (28, 28, 3) 
im = np.ones(tam_imagen, dtype=np.uint8) * 255  

for index in central:
    f, c = divmod(index, 28)  
    im[f, c] = [128,0,128]
for index in primera:
    f, c = divmod(index, 28)  
    im[f, c] = [255,165,0]
    
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, extent=[0, 28, 28, 0])

ax.set_xticks(np.arange(28))
ax.set_yticks(np.arange(28))
ax.set_xticklabels(np.arange(28), fontsize=6, rotation=90)  
ax.set_yticklabels(np.arange(28), fontsize=6)

plt.grid(color="gray", linestyle="--", linewidth=0.5)

ax.scatter([], [], color=np.array([128,0,128]) / 255, label="Fila central: " + exactitudes[0])
ax.scatter([], [], color=np.array([255,165,0]) / 255, label="Primera fila: " + exactitudes[1])

ax.legend(loc='lower right', fontsize=10, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en filas enteras (binario)", fontsize=14)
plt.show()
#%%===========================================================================
# Modelo definitivo
#=============================================================================
#%% Armamos 0 y 1 promedio y calculamos la diferencia
uno_solo = dd.sql(""" SELECT *
               	FROM data
               	WHERE labels='1'
               	""").df()
uno_solo = uno_solo.iloc[:, :-1] 	 
uno_solo_porcentaje = uno_solo.mean()
uno_porcentaje = pd.DataFrame([uno_solo_porcentaje], columns=uno_solo.columns)

cero_solo = dd.sql(""" SELECT *
               	FROM data
               	WHERE labels='0'
               	""").df()
cero_solo = cero_solo.iloc[:, :-1] 	 
cero_solo_porcentaje = cero_solo.mean()
cero_porcentaje = pd.DataFrame([cero_solo_porcentaje], columns=cero_solo.columns)

diferencia_porcentajes = cero_porcentaje - uno_porcentaje
diferencia_porcentajes = diferencia_porcentajes.abs()

#%% Evaluamos para diferentes K y diferentes cantidad de píxeles con más variación
n_posibles = list(range(1,31))
k_posibles = list(range(1,20))

grid = pd.DataFrame(np.zeros((len(n_posibles), len(k_posibles)), dtype=int), index=n_posibles, columns=k_posibles)
grid_train = pd.DataFrame(np.zeros((len(n_posibles), len(k_posibles)), dtype=int), index=n_posibles, columns=k_posibles)

# El siguiente ciclo es muy costoso 
for n in n_posibles:
    n_mayor_diferencia = diferencia_porcentajes.iloc[0].nlargest(n).index.tolist()
    n_dif = []
    for x in n_mayor_diferencia:
        n_dif.append(str(x))  
        
    X = binario[n_dif]  
    y = binario['labels']  
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)
    
    for k in k_posibles:
        modelo = KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        y_pred_train = modelo.predict(X_train)
        
        exactitud = accuracy_score(y_test, y_pred)
        grid.at[n,k] = exactitud
        exactitud_train = accuracy_score(y_train,y_pred_train)
        grid_train.at[n,k] = exactitud_train

# Nos quedamos con la mejor combinación
max_exactitud = grid.max().max()
n_mejor, k_mejor = grid.stack().idxmax()

print("\nMaxima Exactitud:", max_exactitud) # 0.9981957600360848
print("Mejores (n, k):", (n_mejor, k_mejor)) # n = 20, k = 3

#%%g Graficamos para analizar el modelo
# Graficamos los píxeles elegidos
veinte_mayor_dif = diferencia_porcentajes.iloc[0].nlargest(n_mejor).index.tolist()
tam_imagen = (28, 28, 3) 
im = np.ones(tam_imagen, dtype=np.uint8) * 255  

color_base = np.array([0, 206, 209])

for i, indice in enumerate(np.array(veinte_mayor_dif, dtype=int)):
    f, c = divmod(indice, 28)  
    intensidad = 0.3 + 0.7 * (1 - i / (n_mejor - 1))
    im[f, c] = (color_base * intensidad).astype(np.uint8)
    
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, extent=[0, 28, 28, 0])

ax.set_xticks(np.arange(28))
ax.set_yticks(np.arange(28))
ax.set_xticklabels(np.arange(28), fontsize=6, rotation=90)  
ax.set_yticklabels(np.arange(28), fontsize=6)

plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.title("20 píxeles de mayor variación entre 0 y 1", fontsize=14)

plt.show()

# Graficamos exactitud en función de pixeles
grid[[1,3, 7, 17]].plot(kind="line", marker="o", 
                        figsize=(8, 5), grid=True, 
                        title="Cantidad de píxeles contra exactitud con diferentes valores de K",
                        color=["orange", "blue", "magenta", "purple"])
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
renombre_labels = [f"K = {k}" for k in [1, 3, 7, 17]]
plt.legend(renombre_labels)
plt.show()


# Graficamos performance en train y test dependiendo de cantidad de píxeles (K = 3)
grid[3].plot(kind="line", marker="o", figsize=(7, 5), label='test', grid=True, title="Cantidad de píxeles contra exactitud", zorder=3, color='#32CD32')
grid_train[3].plot(kind="line", marker="o", figsize=(7, 5), label='train', grid=True, title="Cantidad de píxeles contra exactitud", zorder=3, color='red')
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
plt.axvline(x=20, color='purple',linestyle='--',linewidth=2,label='Cantidad elegida', zorder=2)
plt.legend()
plt.show()

# Graficamos performance en train y test dependiendo de cant de píxeles desde 15 hasta 30
grid[3].plot(kind="line", marker="o", figsize=(7, 5), label='test', grid=True, title="Cantidad de píxeles contra exactitud", zorder=3, color='#32CD32')
grid_train[3].plot(kind="line", marker="o", figsize=(7, 5), label='train', grid=True, title="Cantidad de píxeles contra exactitud (de 15 a 30)", zorder=3, color='red')
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
plt.xlim(15, 30)
plt.ylim(0.994, 1)
plt.xticks(range(15,31))
plt.axvline(x=20, color='purple',linestyle='--',linewidth=2,label='Cantidad elegida', zorder=2)
plt.legend()
plt.show()

# Graficamos performance en train y test dependiendo de K (20 píxeles)
veinte_pixeles_test = grid.loc[20]
veinte_pixeles_train = grid_train.loc[20]

plt.plot(veinte_pixeles_test.index, veinte_pixeles_test.values, label='test', marker='o', zorder=3, color='#32CD32')
plt.plot(veinte_pixeles_train.index, veinte_pixeles_train.values, label='train', marker='o', zorder=3, color='red')
plt.xlabel("Valores de K")
plt.xticks(k_posibles)
plt.ylabel("Exactitud")
plt.title("K contra exactitud con 20 píxeles")
plt.axvline(x=3, color='purple',linestyle='--',label='K elegido', zorder=2)
plt.legend()
plt.show()

#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #                     CLASIFICACIÓN MULTICLASE                          # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#%%===========================================================================
# Separación de Held-out
#=============================================================================

X = data.drop('labels', axis=1)
y = data['labels']
X_dev, X_held_out, y_dev, y_held_out = train_test_split(X,y,test_size=0.15, random_state = 14)

#%%===========================================================================
# Elección del modelo
#=============================================================================
# Probamos con alturas de 2 a 10 con dos criterios distintos
alturas = list(range(2,11))
nsplits = 5
kf = KFold(n_splits=nsplits)

resultados_gini = np.zeros((nsplits, len(alturas)))
resultados_entropia = np.zeros((nsplits, len(alturas)))
res_train_entropia = np.zeros((nsplits, len(alturas)))

# El siguiente ciclo es muy costoso 
for i, (train_index, test_index) in enumerate(kf.split(X_dev)):

    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, hmax in enumerate(alturas):
        for c in ['gini', 'entropy']:
            arbol = tree.DecisionTreeClassifier(max_depth = hmax, criterion=c,random_state=14)
            arbol.fit(kf_X_train, kf_y_train)
            pred = arbol.predict(kf_X_test)
            pred_train = arbol.predict(kf_X_train)
            
            score = accuracy_score(kf_y_test,pred)
            score_train = accuracy_score(kf_y_train,pred_train)
            if c == 'gini':
                resultados_gini[i, j] = score
            else:
                resultados_entropia[i,j] = score
                res_train_entropia[i,j] = score_train

scores_promedio_gini = resultados_gini.mean(axis = 0)
scores_promedio_entropia = resultados_entropia.mean(axis = 0)
scores_promedio_train_entropia = res_train_entropia.mean(axis = 0)

for i,e in enumerate(alturas):
    print(f'Score promedio del modelo con gini hmax = {e}: {scores_promedio_gini[i]:.4f}')
    print(f'Score promedio del modelo con entropia hmax = {e}: {scores_promedio_entropia[i]:.4f}')

# Nos quedamos con la mejor combinación
mejor_altura_gini = alturas[scores_promedio_gini.idmax()] 
mejor_exact_gini = scores_promedio_gini.max()
mejor_altura_entropia = alturas[scores_promedio_entropia.idmax()] 
mejor_exact_entropia = scores_promedio_entropia.max()

mejor_altura = max((mejor_exact_gini, mejor_altura_gini),(mejor_exact_entropia, mejor_altura_entropia))[1]
mejor_criterio = max((mejor_exact_gini, mejor_altura_gini),(mejor_exact_entropia, mejor_altura_entropia))[0]
"""
Score promedio del modelo con entropia hmax = 9: 0.6491
Score promedio del modelo con entropia hmax = 10: 0.6756
"""
#%% Entrenamos el modelo sobre el held-out y reportamos performance
arbol = tree.DecisionTreeClassifier(max_depth = mejor_altura, criterion=mejor_criterio, random_state=14)
arbol.fit(X_dev, y_dev)
pred = arbol.predict(X_held_out)
score = accuracy_score(y_held_out,pred) # 0.6860

print(f'Score del modelo sobre held out con {mejor_criterio} hmax = {mejor_altura}: {score:.4f}')
#%% Graficamos para analizar el modelo
# Graficamos exactitud contra altura por criterio
plt.plot(alturas,scores_promedio_entropia, label='Entropia', marker='o')
plt.plot(alturas,scores_promedio_gini, label='Gini', marker='o')
plt.xlabel("Altura")
plt.xticks(alturas)
plt.ylabel("Exactitud")
plt.title("Altura de árbol contra exactitud (por criterio)")
#plt.axvline(x=3, color='purple',linestyle='--',label='K elegido', zorder=2)
plt.legend()
plt.show()

# Graficamos exactitud contra altura en train y test (entropia)
plt.plot(alturas,scores_promedio_entropia, label='Test', marker='o', color='#32CD32')
plt.plot(alturas,scores_promedio_train_entropia, label='Train', marker='o',color='red')
plt.xlabel("Altura")
plt.xticks(alturas)
plt.ylabel("Exactitud")
plt.title("Altura de árbol contra exactitud en train y test (entropia)")
#plt.axvline(x=3, color='purple',linestyle='--',label='K elegido', zorder=2)
plt.legend()
plt.show()
