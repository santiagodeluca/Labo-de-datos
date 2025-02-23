import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import tree
import duckdb as dd
#%%
arboles = pd.read_csv("guia/arboles.csv")

#%% ej 1
f, s = plt.subplots()
plt.suptitle('Historgrama de diametro', size = 'large')

sns.histplot(data = arboles, x = 'diametro', hue = 'nombre_com', bins = 10,
             palette = 'viridis')
f, s = plt.subplots()
plt.suptitle('Historgrama de altura', size = 'large')

sns.histplot(data = arboles, x = 'altura_tot', hue = 'nombre_com', bins = 10,
             palette = 'viridis')
f, s = plt.subplots()
plt.suptitle('Historgrama de inclinacion', size = 'large')

sns.histplot(data = arboles, x = 'inclinacio', hue = 'nombre_com', bins = 10,
             palette = 'viridis')
#%% ej 2
jac = dd.sql("""
             SELECT altura_tot, diametro, inclinacio
             FROM arboles
             WHERE arboles.nombre_com = 'Jacarandá';
             """).df()
euc = dd.sql("""
             SELECT altura_tot, diametro, inclinacio
             FROM arboles
             WHERE nombre_com = 'Eucalipto';
             """).df()
pin = dd.sql("""
             SELECT altura_tot, diametro, inclinacio
             FROM arboles
             WHERE nombre_com = 'Pindó';
             """).df()
cei = dd.sql("""
             SELECT altura_tot, diametro, inclinacio
             FROM arboles
             WHERE nombre_com = 'Ceibo';
             """).df()
fig, ax = plt.subplots(figsize=(7, 5))
plt.suptitle('Scatterplot diametro vs altura', size = 'large')
ax.set_xlabel('Diametro')
ax.set_ylabel('Altura')
ax.scatter(jac['diametro'], 
           jac['altura_tot'], 
           color='#1F77B4', label='Jacaranda', s=10)
ax.scatter(euc['diametro'], 
           euc['altura_tot'], 
           color='#FF7F0E', label='Eucalipto', s=10)
ax.scatter(pin['diametro'], 
           pin['altura_tot'], 
           color='#2CA02C', label='Pindo', s=10)
ax.scatter(cei['diametro'], 
           cei['altura_tot'], 
           color='red', label='Ceibo', s=10)
ax.legend()
#%% ej 3
tree2gini = tree.DecisionTreeClassifier(criterion = "gini", max_depth=2)
tree2gini = tree2gini.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [15,10])
tree.plot_tree(tree2gini, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

tree2ent = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=2)
tree2ent = tree2gini.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [15,10])
tree.plot_tree(tree2ent, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

tree3gini = tree.DecisionTreeClassifier(criterion = "gini", max_depth=3,min_samples_split=3)
tree3gini = tree3gini.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [20,10])
tree.plot_tree(tree3gini, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

tree3ent = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=3,min_samples_split=3)
tree3ent = tree3ent.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [20,10])
tree.plot_tree(tree3ent, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

tree4gini = tree.DecisionTreeClassifier(criterion = "gini", max_depth=4,min_samples_split=4)
tree4gini = tree4gini.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [50,10])
tree.plot_tree(tree4gini, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

tree4ent = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=4,min_samples_split=4)
tree4ent = tree4ent.fit(arboles[['diametro','altura_tot','inclinacio']], arboles['nombre_com'])

plt.figure(figsize= [50,10])
tree.plot_tree(tree4ent, feature_names = ['diametro','altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

diamYalt = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=3,min_samples_split=3)
diamYalt = diamYalt.fit(arboles[['diametro','altura_tot']], arboles['nombre_com'])
plt.figure(figsize= [20,10])
tree.plot_tree(diamYalt, feature_names = ['diametro','altura_tot'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

diamYinc = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=3,min_samples_split=3)
diamYinc = diamYinc.fit(arboles[['diametro','inclinacio']], arboles['nombre_com'])
plt.figure(figsize= [20,10])
tree.plot_tree(diamYinc, feature_names = ['diametro','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)

altYinc = tree.DecisionTreeClassifier(criterion = "entropy", max_depth=3,min_samples_split=3)
altYinc = altYinc.fit(arboles[['altura_tot','inclinacio']], arboles['nombre_com'])
plt.figure(figsize= [20,10])
tree.plot_tree(altYinc, feature_names = ['altura_tot','inclinacio'], class_names = arboles['nombre_com'],filled = True, rounded = True, fontsize = 10)
#%% ej 4
# En general el primer corte se hace sobre la altura, aunque algunas veces sobre el diametro, nunca inc.
#%% ej 5
lista_arboles = [tree2ent,tree2gini,tree3gini,tree3ent,tree4gini,tree4ent]
lista_pred = []

for a in lista_arboles:
    datonuevo = pd.DataFrame([dict(zip(arboles[['diametro','altura_tot','inclinacio']], [56,22,8]))])
    lista_pred.append(a.predict(datonuevo)[0])
    
datonuevo = pd.DataFrame([dict(zip(arboles[['diametro','altura_tot']], [56,22]))])
lista_pred.append(diamYalt.predict(datonuevo)[0])
datonuevo = pd.DataFrame([dict(zip(arboles[['diametro','inclinacio']], [56,8]))])
lista_pred.append(diamYinc.predict(datonuevo)[0])
datonuevo = pd.DataFrame([dict(zip(arboles[['altura_tot','inclinacio']], [22,8]))])
lista_pred.append(altYinc.predict(datonuevo)[0])

# Todos los arboles armados predicen que es eucalipto, asi que conluyo que asi es.