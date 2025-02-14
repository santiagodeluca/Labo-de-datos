import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb as dd

data = sns.load_dataset('penguins')

#%%===========================================================================
#ej 2 c) especies de pinguinos consideradas?

especies = dd.sql("""
                  SELECT DISTINCT species
                  FROM data 
                  """).df()
#%%===========================================================================
#ej 2 d) islas consideradas?
islas = dd.sql("""
                  SELECT DISTINCT island
                  FROM data 
                  """).df()
#%%===========================================================================
#ej 3
for i in islas['island']: 
    fig, ax = plt.subplots()
    
    data.loc[data['island']==i, 'species'].value_counts().plot(kind='pie', 
                                                               ax=ax,
                                                               autopct= '%1.1f%%')
    ax.set_title('Proporción de especies en la isla ' + i)
    ax.set_ylabel('')
    
fig, ax = plt.subplots()

sns.countplot(data=data, x="island", hue="species")
#%%===========================================================================
#ej 4
sns.histplot(data=data['bill_length_mm'], bins = 10, color='red')
plt.xlabel("Grosor de pico (mm)")
plt.ylabel("Cantidad")
plt.title("Distribución del grosor de pico")

plt.figure()
sns.histplot(data=data,x='bill_length_mm', hue='species', bins = 10)
plt.xlabel("Grosor de pico (mm)")
plt.ylabel("Cantidad")
plt.title("Distribución del grosor de pico por especie")


#%%===========================================================================
#ej 5
plt.figure()
sns.histplot(data=data,x='bill_depth_mm', hue='species', bins = 10)
plt.xlabel("Grosor de pico (mm)")
plt.ylabel("Cantidad")
plt.title("Distribución del profundidad de pico por especie")

plt.figure()
sns.histplot(data=data,x='flipper_length_mm', hue='species', bins = 10)
plt.xlabel("Grosor de pico (mm)")
plt.ylabel("Cantidad")
plt.title("Distribución del largo de aleta por especie")
#se puede ver que los Adelie siempre tienen aletas mas cortas y picos menos gruesos
#los gentoo tienen un pico poco profundo y una aleta mas larga
#los chinstrap tiene pico mas grueso
#se puede tener bastante seguridad a partir de un solo dato de que tipo de especie es
#%%===========================================================================
#ej 6

caracteristicas = data.columns[data.columns.str.contains('mm')]
sexo = ['Male', 'Female']

for c in caracteristicas:
    for s in sexo:
        plt.figure()
        sns.histplot(data=data[data['sex']==s],x=c, hue='species', bins = 10)
        plt.xlabel(c)
        plt.ylabel("Cantidad")
        plt.title("Distribución de " + c + " por especie y sexo " + s)
        
#No es tan claro a partir de uno de estos datos si el sexo es m o f, pero teniendo los tres juntos tal vez se podria hacer una buena aproximacion
#%%===========================================================================
#ej 7
c = caracteristicas
for s in sexo:
    plt.figure()
    plt.scatter(data = data[data['sex']==s], x = c[0], y = c[1])
    plt.title(c[0] + ' vs ' + c[1] + ' con sexo ' + s)
    plt.figure()
    plt.scatter(data = data[data['sex']==s], x = c[1], y = c[2])
    plt.title(c[1] + ' vs ' + c[2] + ' con sexo ' + s)
    plt.figure()
    plt.scatter(data = data[data['sex']==s], x = c[0], y = c[2])
    plt.title(c[0] + ' vs ' + c[2] + ' con sexo ' + s)
#no es claro que haya un par de variables en las que la diferencia de valores por sexo sea 
#tan grande como para asegurar el sexo a partir de ese par.
for s in sexo:
    plt.figure()
    sns.scatterplot(data = data[data['sex']==s], x = c[0], y = c[1], hue='species')
    plt.title(c[0] + ' vs ' + c[1] + ' con sexo ' + s)
    plt.figure()
    sns.scatterplot(data = data[data['sex']==s], x = c[1], y = c[2], hue='species')
    plt.title(c[1] + ' vs ' + c[2] + ' con sexo ' + s)
    plt.figure()
    sns.scatterplot(data = data[data['sex']==s], x = c[0], y = c[2], hue='species')
    plt.title(c[0] + ' vs ' + c[2] + ' con sexo ' + s)
#si se fija una especie en particular es mas facil ver la variacion de los pares de variables
#segun el sexo. no es muy preciso, pero se podria intentar hacer una conclusion a partir de algunos pares de datos
#%%===========================================================================
#ej 8
plt.figure()
sns.scatterplot(data = data, x = c[0], y = c[1], hue='species')
plt.title(c[0] + ' vs ' + c[1])
#Adelie y Gentoo presentan mas dispersion, mientras que chinstrap no.
#La relacion es similar entre las tres especias: en rangos generales, mas largo implica mas profundidad
#%%===========================================================================
#ej 9
todas_caracteristicas = data.columns[data.columns.str.contains('mm') | data.columns.str.contains('_g')]
for c in todas_caracteristicas:
    plt.figure()
    sns.histplot(data=data[data['sex']=='Female'],x=c, hue='species', bins = 10)
    plt.xlabel(c)
    plt.ylabel("Cantidad")
    plt.title("Distribución de " + c + " por especie en hembras")
#Con una sola caractristica se puede predecir bastante acerca de la especie Gentoo.
#Hay una clara superposicion entre Adelie y chinstrap en todas las caracteristicas menos en 
#longitu de pico. teniendo longitud de pico y cualquiera de los otros tres datos, se puede
#predecir con bastante seguridad la especie.
#%%===========================================================================
#ej 10
todas_caracteristicas = data.columns[data.columns.str.contains('mm') | data.columns.str.contains('_g')]
for c in todas_caracteristicas:
    plt.figure()
    sns.histplot(data=data[data['sex']=='Male'],x=c, hue='species', bins = 10)
    plt.xlabel(c)
    plt.ylabel("Cantidad")
    plt.title("Distribución de " + c + " por especie en machos")
#La idea de la prediccion anterior se mantiene, tambien para machos.
#%%===========================================================================
#ej 11
solo_adelie = data[data['species'] =='Adelie'].sort_values(by='bill_length_mm')

fig, ax = plt.subplots()
ax.plot('bill_length_mm', 'body_mass_g', data=solo_adelie, 
        marker='o', 
        color='orange',
        linewidth=1,
        linestyle='-',
        label='Peso')
ax.set_ylim(2000,5000)
#%%===========================================================================
#ej 12

male_data = data[data['sex'] == 'Male']
male_count = male_data['species'].value_counts()
female_data = data[data['sex'] == 'Female']
female_count = female_data['species'].value_counts()

fig, ax = plt.subplots()
ax.bar(male_count.index, male_count.values, label='Macho', color='skyblue')
ax.bar(female_count.index, female_count.values, bottom=male_count.values, label='Hembra', color='pink')
#%%===========================================================================
#ej 13
fig, ax = plt.subplots()
data.boxplot(by='sex', column='bill_length_mm', ax=ax)
ax.set_title('')
ax.set_xlabel('Sexo')
#En general, el largo del pico es mayor en los machos, la mediana esta por encima y en general
#el rango intercuartilico esta mas arriba para los machos.

#%%===========================================================================
#ej 14
fig, ax = plt.subplots()
data.boxplot(by='species', column='flipper_length_mm', ax=ax)
ax.set_title('')
ax.set_xlabel('Especie')
#gentoo es por mucho la especie con aletas mas largas, meintras que chinstrap tiene
#aletas mas largas que adelie pero por un margen mucho mas pequenio
#es importante notar que adelie tiene dos outliers, mientras que las demas no.

#%%===========================================================================
#ej 15
fig, ax = plt.subplots()

ax = sns.violinplot(x='sex', y='flipper_length_mm', data=data, 
                    palette = {'Female':'orange','Male': 'skyblue'})
ax.set_xlabel('Sexo')
ax.set_ylabel('Largo de aleta (mm)')
ax.set_title('Largo de aleta de pinguinos por sexo')

#%%===========================================================================
#ej 16
fig, ax = plt.subplots()

ax = sns.violinplot(x='species', y='body_mass_g', data=data, 
                    palette = {'Gentoo':'orange','Adelie': 'skyblue','Chinstrap':'pink'})
ax.set_xlabel('Especie')
ax.set_ylabel('Peso (g)')
ax.set_title('Peso de pinguinos por especie')





