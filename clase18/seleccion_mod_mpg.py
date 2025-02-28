#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 13:31:28 2025

@author: mcerdeiro
"""

import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor

#%% cargamos los datos
df = pd.read_csv('auto-mpg.xls')
df['acc_n'] = (df['acceleration'] - df['acceleration'].min())/(df['acceleration'].max() - df['acceleration'].min())
df['wei_n'] = (df['weight'] - df['weight'].min())/(df['weight'].max() - df['weight'].min())
df['hor_n'] = (df['horsepower'] - df['horsepower'].min())/(df['horsepower'].max() - df['horsepower'].min())
df['dis_n'] = (df['displacement'] - df['displacement'].min())/(df['displacement'].max() - df['displacement'].min())

X = df[['acc_n', 'wei_n','hor_n','dis_n']]
y = df.mpg
#%% separamos entre dev y eval
X_dev, X_eval, y_dev, y_eval = train_test_split(X,y,test_size=0.1, random_state = 20)

#%% experimento

vecinos = range(1,51)
nsplits = 10
kf = KFold(n_splits=nsplits)

resultados = np.zeros((nsplits, len(vecinos)))
# una fila por cada fold, una columna por cada modelo

for i, (train_index, test_index) in enumerate(kf.split(X_dev)):

    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, k in enumerate(vecinos):
        neigh = KNeighborsRegressor(n_neighbors=k)
        neigh.fit(kf_X_train, kf_y_train)

        pred = neigh.predict(kf_X_test)
        mse = mean_squared_error(kf_y_test,pred)
        
        resultados[i, j] = mse
#%% promedio scores sobre los folds
mse_promedio = resultados.mean(axis = 0)


#%% 
for i,e in enumerate(vecinos):
    print(f'MSE promedio del modelo con k = {e}: {mse_promedio[i]:.4f}')

#%% entreno el modelo elegido en el conjunto dev entero
k_elegido = KNeighborsRegressor(n_neighbors=4)
k_elegido.fit(X_dev, y_dev)
y_pred = k_elegido.predict(X_dev)

mse_k_elegido = mean_squared_error(y_dev, y_pred)
print('MSE sobre el conjunto de desarrollo: ' + str(mse_k_elegido))

#%% pruebo el modelo elegid y entrenado en el conjunto eval
y_pred_eval = k_elegido.predict(X_eval)       
k_elegido_eval = mean_squared_error(y_eval, y_pred_eval)
print('MSE sobre el conjunto held-out: ' + str(k_elegido_eval))
