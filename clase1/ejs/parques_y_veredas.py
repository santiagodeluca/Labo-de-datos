import pandas as pd

def crea_data_arboles_veredas(nombre_archivo):
    df = pd.read_csv(nombre_archivo)
    res = df.drop(['lat', 'long','manzana','nro_registro','tipo_activ','comuna','calle_nombre','calle_altura','calle_chapa','direccion_normalizada','ubicacion','estado_plantera','ubicacion_plantera','nivel_plantera'], axis = 1) 
    return res

data_arboles_veredas = crea_data_arboles_veredas(r'C:\Users\santi\Labo de datos\clase1\arbolado-publico-lineal-2017-2018.csv')
#data_arboles_veredas.info()

def crea_df_tipas_vereda():
    df = pd.read_csv(r'C:\Users\santi\Labo de datos\clase1\arbolado-publico-lineal-2017-2018.csv')
    solo_tipas = df[df.isin(['Tipuana tipu']).any(axis=1)].copy()
    res = solo_tipas[['diametro_altura_pecho','altura_arbol']].copy()
    res['ambiente'] = 'vereda'
    return res.rename(columns={"diametro_altura_pecho": "diametro", "altura_arbol": "altura"}).copy()

tipas_veredas = crea_df_tipas_vereda()

def crea_df_tipas_parques():
    df = pd.read_csv(r'C:\Users\santi\Labo de datos\clase1\arbolado-en-espacios-verdes.csv')
    solo_tipas = df[df.isin(['Tipuana Tipu']).any(axis=1)].copy()
    res = solo_tipas[['diametro','altura_tot']].copy()
    res['ambiente'] = 'parque'
    return res.rename(columns={"altura_tot": "altura"}).copy()

tipas_parques = crea_df_tipas_parques()

def concatena_y_busca_promedios(df_vereda,df_parque):
    df = pd.concat([df_parque, df_vereda])
    altura_promedio_parque = df.loc[df['ambiente'] == 'parque', 'altura'].mean()
    altura_promedio_vereda = df.loc[df['ambiente'] == 'vereda', 'altura'].mean()
    diametro_promedio_vereda = df.loc[df['ambiente'] == 'vereda', 'diametro'].mean()
    diametro_promedio_parque = df.loc[df['ambiente'] == 'parque', 'diametro'].mean()
    print('Parque: Altura promedio ' + str(altura_promedio_parque) + ', Diametro promedio ' + str(diametro_promedio_parque))
    print('Vereda: Altura promedio ' + str(altura_promedio_vereda) + ', Diametro promedio ' + str(diametro_promedio_vereda))

concatena_y_busca_promedios(tipas_veredas, tipas_parques)

'''
El resultado fue:
Parque: Altura promedio 19.100223269660134, Diametro promedio 57.99429421979658
Vereda: Altura promedio 15.056567180260748, Diametro promedio 54.14271917587724

La conclusión es que, por lo menos en el caso de las tipas, crecer en espacios verdes hace que sean más altas,
pero que estén más inclinadas.
'''