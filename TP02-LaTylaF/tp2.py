#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import duckdb as dd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
#%%
data = pd.read_csv('mnist_c_fog_tp.csv', index_col=0)
prueba = data.iloc[:,:-1]
#%%
#Plot imagen
n = 8464
img = np.array(prueba.iloc[n]).reshape((28,28))
plt.imshow(img, cmap='gray')
plt.title('Número de la fila ' + str(n))
plt.show()
#%% Clasificación binaria
binario = data[(data['labels'] == 0) | (data['labels'] == 1)].reset_index()

cantidad_0 = (binario['labels'] == 0).sum() # 6903
cantidad_1 = (binario['labels'] == 1).sum() # 7877

proporcion = cantidad_0 * 100 / len(binario) # 46,7% son 0 

largo_test = int(len(binario) * 0.15) # Nuestro conjunto de test será el 15% del de desarrollo
test = binario[:largo_test]
train = binario[largo_test:].reset_index()
#%%
#comparamos los valores de pixeles del centro 
alturas_importantes = [9, 13, 19]
for i in alturas_importantes:
    pix1 = str(i * 28 + 12)
    pix2 = str(i * 28 + 13)
    pix3 = str(i * 28 + 14)
    X = binario[[pix1,pix2,pix3]]  
    y = binario['labels']  
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)
    
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_train, y_train)
    
    y_pred = modelo.predict(X_test)
    
    exactitud = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo con tres pixeles del centro de fila {i}: {exactitud * 100:.3f}%")
#%%
#comparamos con prediccion en valores en los bordes
X = binario[['13','14','15']]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo con valores del centro de la primera fila: {exactitud * 100:.3f}%")

X = binario[['0','1','2']]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo con primeros píxeles de arriba a la izquierda: {exactitud * 100:.3f}%")
#%% probamos con la fila central a altura 13
arr = np.arange(13*28, 14*28)
fila_central = arr.astype(str)
X = binario[fila_central]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo con todos los pixeles de la fila central : {exactitud * 100:.3f}%")
#%% problamos con la primera fila
arr = np.arange(0, 28)
primera_fila = arr.astype(str)
X = binario[primera_fila]  
y = binario['labels']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo con todos los pixeles de la primera fila: {exactitud * 100:.3f}%")
#%% Comparamos modelos para elegir el mejor
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

n_posibles = list(range(1,31))
k_posibles = list(range(1,20))

matriz = pd.DataFrame(np.zeros((len(n_posibles), len(k_posibles)), dtype=int), index=n_posibles, columns=k_posibles)

# El siguiente ciclo es MUY costoso computacionalmente
for n in n_posibles:
    n_mayor_diferencia = diferencia_porcentajes.iloc[0].nlargest(n).index.tolist()
    n_dif = []
    for x in n_mayor_diferencia:
        n_dif.append(str(x))  
    for k in k_posibles:
        
        X = binario[n_dif]  
        y = binario['labels']  
        
        # NO SE DEJAN FIJO TRAIN Y TEST
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=14)
        
        modelo = KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        
        exactitud = accuracy_score(y_test, y_pred)
        matriz.loc[n,k] = exactitud


max_exactitud = matriz.max().max()
row_label, col_label = matriz.stack().idxmax()

print("\nMaxima Exactitud:", max_exactitud) #0.9981957600360848
print("Mejores (n, k):", (row_label, col_label)) #n=20, k = 3

"""
plt.figure(figsize=(18, 6))
sns.heatmap(matriz.loc[matriz.index > 15, matriz.columns > 1], annot=True, cmap="coolwarm", fmt=".6f", 
            linewidths=0.5, annot_kws={"size": 8})
plt.xlabel("K values")
plt.ylabel("Number of Points")
plt.title("KNN Accuracy Heatmap")
plt.show()
"""
#%%
"""X_promedios = data.groupby('labels').mean()
variaciones = X_promedios.var()
cien_mas_importantes = variaciones.nlargest(100).index esto da 0.647
"""
X = data.drop('labels', axis=1)
y = data['labels']
"""variaciones = X.var()
treinta_mas_importantes = variaciones.nlargest(100).index 
X_seleccionados = X[treinta_mas_importantes] da 0.63"""
X_dev, X_held_out, y_dev, y_held_out = train_test_split(X,y,test_size=0.15, random_state = 14)

#%%
alturas = list(range(2,11))
nsplits = 5
kf = KFold(n_splits=nsplits)

resultados_gini = np.zeros((nsplits, len(alturas)))
resultados_entropia = np.zeros((nsplits, len(alturas)))

for i, (train_index, test_index) in enumerate(kf.split(X_dev)):

    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, hmax in enumerate(alturas):
        for c in ['gini', 'entropy']:
            arbol = tree.DecisionTreeClassifier(max_depth = hmax, criterion=c,random_state=14)
            arbol.fit(kf_X_train, kf_y_train)
            pred = arbol.predict(kf_X_test)
            score = accuracy_score(kf_y_test,pred)
            
            if c == 'gini':
                resultados_gini[i, j] = score
            else:
                resultados_entropia[i,j] = score

scores_promedio_gini = resultados_gini.mean(axis = 0)
scores_promedio_entropia = resultados_entropia.mean(axis = 0)

for i,e in enumerate(alturas):
    print(f'Score promedio del modelo con gini hmax = {e}: {scores_promedio_gini[i]:.4f}')
    print(f'Score promedio del modelo con entropia hmax = {e}: {scores_promedio_entropia[i]:.4f}')
    
"""
Score promedio del modelo con gini hmax = 9: 0.6491
Score promedio del modelo con entropia hmax = 10: 0.6756
"""
#%% entrenamos el modelo final 
arbol = tree.DecisionTreeClassifier(max_depth = 10, criterion="entropy", random_state=14)
arbol.fit(X_dev, y_dev)
pred = arbol.predict(X_held_out)
score = accuracy_score(y_held_out,pred)

print(f'Score del modelo sobre held out con entropia hmax = {e}: {score:.4f}')
#0.5401



