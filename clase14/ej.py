import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
import duckdb as dd
from sklearn.datasets import load_iris
#%%===========================================================================
iris = load_iris(as_frame = True)

data = iris.frame

nbins = 35

f, s = plt.subplots(2,2)
plt.suptitle('Historgrama de los 4 atributos', size = 'large')

sns.histplot(data = data, x = 'sepal width (cm)', hue = 'target', bins = nbins, stat = 'probability', 
             ax = s[0,0], palette = 'viridis')
sns.histplot(data = data, x = 'sepal length (cm)', hue = 'target', bins = nbins, stat = 'probability', 
             ax = s[0,1], palette = 'viridis')
sns.histplot(data = data, x = 'petal length (cm)', hue = 'target', bins = nbins, stat = 'probability', 
             ax = s[1,0], palette = 'viridis')
sns.histplot(data = data, x = 'petal width (cm)', hue = 'target', bins = nbins, stat = 'probability', 
             ax = s[1,1], palette = 'viridis')
 #%%
lista_umbrales = np.arange(4, 6, 0.1).tolist()
mejor_umbral = 4

def proporcion(matriz):
    correctos = 0
    for i in range(3):
        correctos += matriz[i][i]
    
    return correctos/150

for u in lista_umbrales:
    def clasificador_iris(pet_l):
        #pet_l = fila('petal length (cm)')
        if pet_l < 2.5:
            res = 0
        elif pet_l > u:
            res = 2
        else:
            res = 1titanic_training.csv
        return res
    
    data_clasif = data.copy()
    data_clasif['clase_asignada'] = data_clasif['petal length (cm)'].map(clasificador_iris)
    
    matriz_confusion = np.zeros((3,3))
    
    for i in range(3):
        for j in range(3):
            filtro = (data_clasif['target']==i) & (data_clasif['clase_asignada'] == j)
            cuenta = len(data_clasif[filtro])
            matriz_confusion[i,j] = cuenta
#%%

data = pd.read_csv('titanic_training.csv')
        
clases_count = dd.sql("""
                      SELECT PClass, count(*) AS Cantidad
                      FROM data
                      GROUP BY PClass
                      """).df()

niños_total = dd.sql("""
               SELECT Count(*)
               FROM data
               WHERE Age < 6
               """).df() # 68
total = dd.sql("""
               SELECT Count(*)
               FROM data;
               """).df() #891

proporcion_niños = niños_total / total

sobrevivieron_niños= dd.sql("""
                      SELECT count(*) AS Cantidad
                      FROM data
                      WHERE Age < 6 AND SURVIVED = 1;
                      """).df()
            
fig, ax = plt.subplots()

ax.plot('Fare', 'Survived', data=data, 
        marker='o', 
        color='orange',
        linewidth=2,
        linestyle='--',
        label='sobrevivio')

def sobrevivio(x):
    vive = False
    p = 0 
    if x['Sex'] == 'female':
        p+=1.5
    if x['Age'] < 6:
        p+=1
    if x['Pclass'] == 1:
        p+=0.5
    if x['Fare'] > 26:
        p+=0.5
    return p
                      
sob = dd.sql("""
                      SELECT *
                      FROM data
                      WHERE SURVIVED = 1;
                      """).df()
l = []
for i, fila in sob.iterrows():
    l.append(sobrevivio(fila))
    
av = sum(l) / len(l)
    
proporcion_niños_sobrevivieron = sobrevivieron_niños/niños_total

d = pd.read_csv('titanic_competencia.csv')
def sobre(x):
    p = 0 
    if x['Sex'] == 'female':
        p+=1.5
    if x['Age'] < 6:
        p+=1
    if x['Pclass'] == 1:
        p+=0.5
    if x['Fare'] > 26:
        p+=0.5
    res = 0 
    if p > 1.5:
        res = 1 
    return res
resutl = []
for i, v in d.iterrows():
    resutl.append(sobre(v))