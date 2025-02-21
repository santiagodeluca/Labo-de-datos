import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error

# %%===========================================================================
# roundup
# =============================================================================
ru = pd.read_csv("clase16/datos_roundup.txt", delim_whitespace=' ')

# %% Aproximar recta
# Y = a + b*X
X = np.linspace(min(ru['RU']) ,max(ru['RU']))
a = 105
b = 0.038
Y = a + b*X

plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y,  'r')
plt.show()

#%% Obtener recta de cuadrados minimos
"""promx = sum(X) / len(X)
promy = sum(Y) / len(Y)


bnom = 0
bdem = 0
for i in range(len(X)* len(Y)):
    bnom += (X[i-1]*promx)*(Y[i-1]*promy)
    bdem += (X[i-1]*promx)*(X[i-1]*promx)

b1 = bnom/bdem
b0 = promy-b1*promx

Y = b0 + b1*X

"""

a, b =  np.polyfit(ru['RU'], ru['ID'], 1)
Y = b + a*X
plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y, 'k')
plt.show()

#%% Calcular score R²


r2 = r2_score(ru['ID'], b + a*ru['RU'])
print("R²: " + str(r2))
r2 = mean_squared_error(ru['ID'], b + a*ru['RU'])
print("R²: " + str(r2))
#%%

ru = pd.read_csv("datos_libreta_424.txt", delim_whitespace=' ')
a, b =  np.polyfit(ru['RU'], ru['ID'], 1)
Y = b + a*X
plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y,  'r')

r2 = r2_score(ru['ID'], b + a*ru['RU'])
print("R²: " + str(r2))
r2m = mean_squared_error(ru['ID'], b + a*ru['RU'])
print("R²: " + str(r2))



# %%===========================================================================
# Anascombe
# =============================================================================
df = sns.load_dataset("anscombe")


# %%===========================================================================
# mpg
# =============================================================================

mpg = pd.read_csv("auto-mpg.xls")

"""
mpg: miles per galon
displacement: Cilindrada

"""

print(mpg.dtypes)

# %% Comparar variables con graficos

def versus(col1, col2):
    plt.scatter(mpg[col1], mpg[col2])
    plt.title(col1 +' vs '+ col2)

    plt.show()
versus('weight', 'mpg')
versus('model year', 'mpg')

#%% Comparar variables y calcular recta de cuadrados minimos

def reg_lineal(col1, col2, grado):
    X = np.linspace(min(mpg[col1]), max(mpg[col1]))
    if grado == 1:
        a, b =  np.polyfit(mpg[col1], mpg[col2], grado)
        Y = b + a*X
    else:
        a, b, c =  np.polyfit(mpg[col1], mpg[col2], grado)
        Y = c + b*X + a*X*X
    plt.plot(X, Y, 'k')
    plt.scatter(mpg[col1], mpg[col2])
    plt.title(col1 +' vs '+ col2)

    plt.show()
    
reg_lineal('weight', 'mpg', 2)
reg_lineal('model year', 'mpg',1)
#%% Comparar variables, calcular recta de cuadrados minimos y calcular R²

def reg_lineal_r2(col1, col2, grado=1):
    X = np.linspace(min(mpg[col1]), max(mpg[col1]))
    if grado == 1:
        a, b =  np.polyfit(mpg[col1], mpg[col2], grado)
        Y = b + a*X
        r2 = r2_score(mpg[col2], b+ a*mpg[col1])
    else:
        a, b, c =  np.polyfit(mpg[col1], mpg[col2], grado)
        Y = c + b*X + a*X*X
        r2 = r2_score(mpg[col2], c + b*mpg[col1] + a*mpg[col1]*mpg[col1])

    plt.plot(X, Y, 'k')
    plt.scatter(mpg[col1], mpg[col2])

    plt.title("R²: " + str(r2))
    plt.show()
reg_lineal_r2('weight', 'mpg', 2)
reg_lineal_r2('model year', 'mpg',1)
