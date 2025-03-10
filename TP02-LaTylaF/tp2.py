"""
Materia: Laboratorio de datos - FCEyN - UBA
Trabajo práctico 02
Alumnos : Santiago De Luca, Federico Borruat, Lautaro Aguilar
Fecha  : 2025-03-10
Descripcion : Este archivo está dividido en tres partes:
              - Análisis exploratorio
              - Clasificación binaria
              - Clasificación multiclase
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 
import matplotlib.cm as cm 
import duckdb as dd
import seaborn as sns
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, confusion_matrix
#%% Lectura de datos
data = pd.read_csv('mnist_c_fog_tp.csv', index_col=0)
#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #                     ANÁLISIS EXPLORATORIO                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
X_train_bi, X_test_bi, y_train_bi, y_test_bi = train_test_split(binario.drop('labels', axis=1), binario['labels'], test_size=0.15, random_state=14)

cantidad_0 = (binario['labels'] == 0).sum() # 6903
cantidad_1 = (binario['labels'] == 1).sum() # 7877

proporcion = cantidad_0 * 100 / len(binario) # 46,7% son 0 
print(f"Porcentaje de ceros en el dataset binario: {proporcion}%")
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

    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_train_bi[[str(pix1), str(pix2), str(pix3)]], y_train_bi)

    y_pred = modelo.predict(X_test_bi[[str(pix1), str(pix2), str(pix3)]])
    exactitud = accuracy_score(y_test_bi, y_pred)
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

ax.legend(loc='upper right', fontsize=13.5, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en valores del centro (binario, K=3)", fontsize=14)
plt.show()
#%% Probamos con tres píxeles en distintos bordes
# Borde de arriba al centro
exactitudes = []

arriba_centro = ['13','14','15']

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[arriba_centro], y_train_bi)
y_pred = modelo.predict(X_test_bi[arriba_centro])

exactitud = accuracy_score(y_test_bi, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con valores del centro de la primera fila: {exactitud * 100:.3f}%")

# Borde de arriba a la izquierda
arriba_izq = ['0','1','2']

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[arriba_izq], y_train_bi)
y_pred = modelo.predict(X_test_bi[arriba_izq])

exactitud = accuracy_score(y_test_bi, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con primeros píxeles de arriba a la izquierda: {exactitud * 100:.3f}%")

# Borde de centro izquierda
centro_izq = [str(28*12),str(28*13),str(28*14)]

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[centro_izq], y_train_bi)
y_pred = modelo.predict(X_test_bi[centro_izq])

exactitud = accuracy_score(y_test_bi, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con primeros píxeles del centro a la izquierda: {exactitud * 100:.3f}%")

# Borde de centro derecha
centro_der = [str((28*12) + 27),str((28*13)+27),str((28*14)+27)]

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[centro_der], y_train_bi)
y_pred = modelo.predict(X_test_bi[centro_der])

exactitud = accuracy_score(y_test_bi, y_pred)
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

ax.legend(loc='lower right', fontsize=13.5, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en valores de bordes (binario, K=3)", fontsize=14)
plt.show()

#%% Probamos con filas enteras
exactitudes = []

# Fila central
central = np.arange(13*28, 14*28)
fila_central = central.astype(str)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[fila_central], y_train_bi)
y_pred = modelo.predict(X_test_bi[fila_central])

exactitud = accuracy_score(y_test_bi, y_pred)
exactitudes.append(f"{exactitud * 100:.2f}%")
print(f"Precisión del modelo con todos los pixeles de la fila central : {exactitud * 100:.3f}%")

# Primera fila
primera = np.arange(0, 28)
primera_fila = primera.astype(str)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_bi[primera_fila], y_train_bi)
y_pred = modelo.predict(X_test_bi[primera_fila])

exactitud = accuracy_score(y_test_bi, y_pred)
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

ax.legend(loc='lower right', fontsize=14, title="Exactitud", title_fontsize=12)
plt.title("Exactitud de KNN en filas enteras (binario, K=3)", fontsize=14)
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
n_posibles = list(range(1,25))
k_posibles = list(range(1,13))

grid = pd.DataFrame(np.zeros((len(n_posibles), len(k_posibles)), dtype=float), index=n_posibles, columns=k_posibles)
grid_train = pd.DataFrame(np.zeros((len(n_posibles), len(k_posibles)), dtype=float), index=n_posibles, columns=k_posibles)

# El siguiente ciclo es muy costoso 
for n in n_posibles:
    n_mayor_diferencia = diferencia_porcentajes.iloc[0].nlargest(n).index.tolist()
    n_dif = []
    for x in n_mayor_diferencia:
        n_dif.append(str(x))  
            
    for k in k_posibles:
        modelo = KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_train_bi[n_dif], y_train_bi)
        
        y_pred = modelo.predict(X_test_bi[n_dif])
        y_pred_train = modelo.predict(X_train_bi[n_dif])
        
        exactitud = accuracy_score(y_test_bi, y_pred)
        grid.at[n,k] = exactitud
        exactitud_train = accuracy_score(y_train_bi,y_pred_train)
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

n_pixels = len(veinte_mayor_dif)
intensities = np.linspace(0.4, 1.0, n_pixels)  

for i, indice in enumerate(np.array(veinte_mayor_dif, dtype=int)):
    f, c = divmod(indice, 28)  
    im[f, c] = (color_base * intensities[i]).astype(np.uint8)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(im, extent=[0, 28, 28, 0])
ax.set_xticks(np.arange(28))
ax.set_yticks(np.arange(28))
ax.set_xticklabels(np.arange(28), fontsize=6, rotation=90)  
ax.set_yticklabels(np.arange(28), fontsize=6)
plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.title("20 píxeles de mayor variación entre 0 y 1", fontsize=14)

# Agregamos al gráfico un label del degradé en los colores
cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", [color_base / 255 * 0.4, color_base / 255])
norm = mcolors.Normalize(vmin=0.4, vmax=1.0)
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Variación de píxel", fontsize=12)
cbar.set_ticks([0.4, 1.0])
cbar.set_ticklabels(["Mayor variación", "Menor variación"])  

plt.show()

# Graficamos exactitud en función de pixeles
grid[[1,3, 7, 12]].plot(kind="line", marker="o", 
                        figsize=(8, 5), grid=True, 
                        title="Cantidad de píxeles contra exactitud con diferentes valores de K",
                        color=["orange", "blue", "magenta", "purple"])
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
renombre_labels = [f"K = {k}" for k in [1, 3, 7, 12]]
plt.legend(renombre_labels)
plt.show()


# Graficamos performance en train y test dependiendo de cantidad de píxeles (K = 3)
grid[3].plot(kind="line", marker="o", figsize=(7, 5), label='test', grid=True, zorder=3, color='#32CD32')
grid_train[3].plot(kind="line", marker="o", figsize=(7, 5), label='train', grid=True, title="Cantidad de píxeles contra exactitud con K = 3", zorder=3, color='red')
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
plt.axvline(x=20, color='purple',linestyle='--',linewidth=2,label='Cantidad elegida', zorder=2)
plt.legend()
plt.show()

# Graficamos performance en train y test dependiendo de cant de píxeles desde 15 hasta 30
grid[3].plot(kind="line", marker="o", figsize=(7, 5), label='test', grid=True, zorder=3, color='#32CD32')
grid_train[3].plot(kind="line", marker="o", figsize=(7, 5), label='train', grid=True, title="Cantidad de píxeles contra exactitud (de 15 a 30) con K = 3", zorder=3, color='red')
plt.xlabel("Cantidad de píxeles")
plt.ylabel("Exactitud")
plt.xlim(15, 24)
plt.ylim(0.994, 1)
plt.xticks(range(15,25))
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
# Primeros acercamientos al modelo
#=============================================================================
# Entrenamos dos árboles sin k-folding
X = data.drop('labels', axis=1)
y = data['labels']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

# Árbol de máxima profundidad 2 con gini
arbol_gini_2 = tree.DecisionTreeClassifier(criterion = "gini", max_depth=2)
arbol_gini_2.fit(X_train, y_train)
pred = arbol_gini_2.predict(X_test)
exactitud = accuracy_score(y_test, pred)
print(f'Score del modelo con gini hmax = 2: {exactitud:.4f}') #0.2043
# Graficamos
plt.figure(figsize= (26,10))
tree.plot_tree(arbol_gini_2, feature_names=[f'Pixel {i}' for i in range(784)], filled=True, fontsize=14)
plt.show()

# Árbol de máxima profundidad 3 con entropia
arbol_entropia_3 = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=3)
arbol_entropia_3.fit(X_train, y_train)
pred = arbol_entropia_3.predict(X_test)
exactitud = accuracy_score(y_test, pred)
print(f'Score del modelo con entropia hmax = 3: {exactitud:.4f}') #0.29


#%%===========================================================================
# Separación de Held-out
#=============================================================================

X = data.drop('labels', axis=1)
y = data['labels']
X_dev, X_held_out, y_dev, y_held_out = train_test_split(X,y,test_size=0.15, random_state = 14)

#%%===========================================================================
# Elección del modelo
#=============================================================================
# Probamos con alturas de 2 a 10 con dos criterios distintos usando k-folding
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
mejor_altura_gini = alturas[np.argmax(scores_promedio_gini)] 
mejor_exact_gini = max(scores_promedio_gini)
mejor_altura_entropia = alturas[np.argmax(scores_promedio_entropia)] 
mejor_exact_entropia = max(scores_promedio_entropia)

mejor_altura = max((mejor_exact_gini, mejor_altura_gini),(mejor_exact_entropia, mejor_altura_entropia))[1]
mejor_exactitud = max((mejor_exact_gini, mejor_altura_gini),(mejor_exact_entropia, mejor_altura_entropia))[0]
mejor_criterio = max((mejor_exact_gini, 'gini'),(mejor_exact_entropia, 'entropy'))[1]

#%% Entrenamos el modelo sobre el held-out y reportamos performance
arbol = tree.DecisionTreeClassifier(max_depth = mejor_altura, criterion=mejor_criterio, random_state=14)
arbol.fit(X_dev, y_dev)
pred = arbol.predict(X_held_out)
score = accuracy_score(y_held_out,pred) # 0.6860
print(f'Score del modelo sobre held out con {mejor_criterio} hmax = {mejor_altura}: {score:.4f}')
#%% Graficamos para analizar el modelo
# Graficamos la matriz de confusión
matriz_confusion = confusion_matrix(y_held_out, pred)
plt.figure(figsize=(9, 6)) 
sns.heatmap(matriz_confusion, annot=True, fmt='d', cmap='Greens')
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de confusión en el modelo final de clasificación multiclase')
plt.show()

# Graficamos exactitud contra altura por criterio
plt.plot(alturas,scores_promedio_entropia, label='Entropia', marker='o')
plt.plot(alturas,scores_promedio_gini, label='Gini', marker='o')
plt.xlabel("Altura")
plt.xticks(alturas)
plt.ylabel("Exactitud")
plt.title("Exactitud contra altura de árbol (por criterio)")
plt.legend()
plt.show()

# Graficamos exactitud contra altura en train y test (entropia)
plt.plot(alturas,scores_promedio_entropia, label='Test', marker='o', color='#32CD32')
plt.plot(alturas,scores_promedio_train_entropia, label='Train', marker='o',color='red')
plt.xlabel("Altura")
plt.xticks(alturas)
plt.ylabel("Exactitud")
plt.title("Exactitud contra altura de árbol en train y test (entropía)")
plt.legend()
plt.show()
