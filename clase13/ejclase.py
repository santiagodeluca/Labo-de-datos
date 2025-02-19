import pandas as pd
import numpy as np
import duckdb as dd
import matplotlib.pyplot as plt
import seaborn as sns
#%%
data = pd.read_csv("clase13/DatosTiemposDeReaccion-DerechaIzquierda - Hoja 1.csv")
fig, ax = plt.subplots()

sns.histplot(data=data, x='Tiempo', hue= 'Mano', palette='viridis')
ax.set_ylabel('Cantidad de tiempos')

datar = pd.read_csv("clase13/DatosTiemposDeReaccion-HabilNoHabil - Hoja 1.csv")

datar['resta'] = datar['mano_no_habil'] - datar['mano_habil'] 

fig, ax = plt.subplots()

sns.histplot(data=datar['resta'],bins=26,color='red')
ax.set_ylabel('Registros')
ax.set_xlabel('Diferencia mano no habil - mano habil (s)')

ax.set_xlim(-2,4)

fig, ax = plt.subplots()

ax.boxplot(datar['resta'], showmeans=True)
ax.set_ylabel('Diferencia mano no habil - mano habil (s)')
ax.set_ylim(-2,3)

