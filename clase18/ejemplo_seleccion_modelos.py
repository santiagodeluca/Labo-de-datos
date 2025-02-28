#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 13:31:28 2025

@author: mcerdeiro
"""


import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
from sklearn import tree

#%% cargamos los datos
df = pd.read_csv('seleccion_modelos.csv')

X = df.drop("Y", axis=1)
y = df.Y
#%% separamos entre dev y eval
X_dev, X_eval, y_dev, y_eval = train_test_split(X,y,test_size=0.1, random_state = 20)

#%% experimento

alturas = [1,2,3,5,13,21]
nsplits = 10
kf = KFold(n_splits=nsplits)

resultados = np.zeros((nsplits, len(alturas)))
# una fila por cada fold, una columna por cada modelo

for i, (train_index, test_index) in enumerate(kf.split(X_dev)):

    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, hmax in enumerate(alturas):
        
        arbol = tree.DecisionTreeClassifier(max_depth = hmax)
        arbol.fit(kf_X_train, kf_y_train)
        pred = arbol.predict(kf_X_test)
        score = accuracy_score(kf_y_test,pred)
        
        resultados[i, j] = score
#%% promedio scores sobre los folds
scores_promedio = resultados.mean(axis = 0)


#%% 
for i,e in enumerate(alturas):
    print(f'Score promedio del modelo con hmax = {e}: {scores_promedio[i]:.4f}')

#%% entreno el modelo elegido en el conjunto dev entero
arbol_elegido = tree.DecisionTreeClassifier(max_depth = 1)
arbol_elegido.fit(X_dev, y_dev)
y_pred = arbol_elegido.predict(X_dev)

score_arbol_elegido_dev = accuracy_score(y_dev, y_pred)
print(score_arbol_elegido_dev)

#%% pruebo el modelo elegid y entrenado en el conjunto eval
y_pred_eval = arbol_elegido.predict(X_eval)       
score_arbol_elegido_eval = accuracy_score(y_eval, y_pred_eval)
print(score_arbol_elegido_eval)
