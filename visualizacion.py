import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
import duckdb as dd

#%%===========================================================================
wine = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/wine.csv', sep = ';')

plt.scatter(data = wine, x = 'fixed acidity', y = 'citric acid')
plt.scatter(data = wine, x = 'residual sugar', y = 'pH')

#%%===========================================================================
fig, ax = plt.subplots()

ax.scatter(data = wine, 
           x = 'fixed acidity', 
           y = 'citric acid',
           s = 60, 
           color='magenta')

ax.set_title('Acidez vs contenido de acido citrico')
ax.set_xlabel('Acidez (g/dm3)', fontsize = 'medium')
ax.set_ylabel('Contenido citrico (g/dm3)', fontsize = 'medium')

#%%===========================================================================
arboles = pd.read_csv('clase1/arbolado-en-espacios-verdes.csv', index_col=2)

especies30 = arboles['id_especie'].value_counts()[:30].index

filtro = arboles['id_especie'].isin(especies30)

arboles30 = arboles[filtro]
#%%===========================================================================
fig, ax = plt.subplots()

ax.scatter(data = arboles30, 
           x = 'altura_tot', 
           y = 'diametro',
           s = 10, 
           color='magenta')

ax.set_title('Altura vs diametro')
ax.set_xlabel('Altura(m)', fontsize = 'medium')
ax.set_ylabel('Diametro(m)', fontsize = 'medium')
#%%===========================================================================
fig, ax = plt.subplots()

ax.scatter(data = arboles30, 
           x = 'long', 
           y = 'lat',
           s = 2, 
           color='magenta')

ax.set_title('Latitud vs longitud')
ax.set_xlabel('Longitud', fontsize = 'medium')
ax.set_ylabel('Latitud', fontsize = 'medium')
#%%===========================================================================
fig, ax = plt.subplots()

origenes = ['Exótico', 'Nativo/Autóctono','NO DETERMINADO']
colores = {'Exótico':'red', 'Nativo/Autóctono':'blue','NO DETERMINADO':'grey'}

for o in origenes:
    ax.scatter(data=arboles30[arboles30['origen'] == o],x='diametro',
               y = 'altura_tot', c=colores[o], alpha = 0.5, label = origenes)
    #terminar
#%%===========================================================================
fig, ax = plt.subplots()

TamanoBurbuja = 5

ax.scatter(data=wine, x = 'fixed acidity', y = 'citric acid', s = wine['residual sugar']*TamanoBurbuja)
ax.set_title('Relacion entre tres variablres')
ax.set_xlabel('Acidez (g/dm3)', fontsize = 'medium')
ax.set_ylabel('Contenido citrico (g/dm3)', fontsize = 'medium')
#%%===========================================================================
fig, ax = plt.subplots()

wine['type'].value_counts().plot(kind='pie', 
                                 ax = ax,
                                 autopct= '%1.1f%%', 
                                 colors=['grey', 'red'],
                                 startangle=90, 
                                 shadow = True, 
                                 explode=(0.1, 0), 
                                 legend=False)
ax.set_ylabel('')
ax.set_title('Distribucion de tipos de vino')
#%%===========================================================================
c = wine.columns

for columna in c:
    if columna != 'pH':
        fig, ax = plt.subplots()
    
        ax.scatter(data = wine, 
                   x = columna, 
                   y = 'pH',
                   s = 20, 
                   color='magenta')
    
        ax.set_title('pH vs ' + columna)
        ax.set_xlabel(columna, fontsize = 'medium')
        ax.set_ylabel('pH', fontsize = 'medium')

#%%===========================================================================
cheetah = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/cheetahRegion.csv')

fig, ax = plt.subplots()

ax.bar(data=cheetah, x='Anio', height='Ventas')
ax.set_title('Ventas de la compania cheetah sports')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas(millones de $)')
ax.set_xlim(0,11)
ax.set_ylim(0,250)

ax.set_xticks(range(1,11,1))
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
#%%===========================================================================
fig, ax = plt.subplots()

cheetah.plot(x='Anio',
            y = ['regionEste', 'regionOeste'],
            kind='bar',
            label = ['Region este', 'Region oeste'],
            ax=ax)
#%%===========================================================================
fig, ax = plt.subplots()

ax.plot('Anio', 'Ventas', data=cheetah, marker='o', color='orange')

ax.set_title('Ventas de la compania cheetah sports')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas(millones de $)')

ax.set_xlim(0,12)
ax.set_ylim(0,250)
#%%===========================================================================
fig, ax = plt.subplots()
ax.plot('Anio', 'regionEste', data=cheetah, 
        marker='o', 
        color='orange',
        linewidth=2,
        linestyle='--',
        label='Region Este')
ax.plot('Anio', 'regionOeste', data=cheetah, 
        marker='o', 
        label='Region Este')

ax.legend()
#%%===========================================================================
gaseosas = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/gaseosas.csv')

fig, ax = plt.subplots()

ax = gaseosas['Compras_gaseosas'].value_counts().plot.bar(ax = ax)
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)
ax.set_title('Frecuencia venta de gaseosas')
#%%===========================================================================
fig, ax = plt.subplots()

ax = gaseosas['Compras_gaseosas'].value_counts(normalize=True).plot.bar(ax = ax)
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)
ax.set_title('Frecuencia venta de gaseosas')

#%%===========================================================================
age = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/ageAtDeath.csv')

fig, ax = plt.subplots()

sns.histplot(data=age['AgeAtDeath'], bins = 17, color='red')
#%%===========================================================================
tips = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/tips.csv')

fig, ax = plt.subplots()

sns.histplot(data=tips, x= 'tip', hue= 'sex', palette='viridis')

#%%===========================================================================
prom = tips['tip'].mean()
med = tips['tip'].median()
mod = tips['tip'].mode()
info = tips['tip'].describe()
#%%===========================================================================
casas = pd.read_csv('visualizacion/Clase 11-12 - Archivos-20250213/ventaCasas.csv')

fig, ax = plt.subplots()

ax.boxplot(casas['PrecioDeVenta'], showmeans=True)

ax.set_yticks([])
ax.set_title('Precio de ventas de casas')
ax.set_ylabel('VPrecio venta ($)')
#%%===========================================================================
fig, ax = plt.subplots()

tips.boxplot(by=['sex'], column=['tip'], ax = ax, grid = False , showmeans= True)

fig.suptitle('')
ax.set_title('Propinas')
ax.set_xlabel('Sexo')
ax.set_ylabel('Valor de Propina($)')
#%%===========================================================================
fig, ax = plt.subplots()

ax = sns.boxplot(x='day',
                 y='tip',
                 hue='sex',
                 data=tips,
                 order=['Thur', 'Fri', 'Sat', 'Sun'])
#%%===========================================================================
fig, ax = plt.subplots()

ax = sns.violinplot(x='sex', y='tip', data=tips, 
                    palette = {'Female':'orange','Male': 'skyblue'})