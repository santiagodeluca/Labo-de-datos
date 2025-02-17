import pandas as pd
import numpy as np
import duckdb as dd
import matplotlib.pyplot as plt
import seaborn as sns

#%% ARMAMOS CENTROS_CULTURALES
def centros_culturales():
    cc = pd.read_csv("tp1/TablasOriginales/centros_culturales.csv", dtype={'ID_DEPTO': str})
    mail = cc["Mail "]
    capacidad = cc["Capacidad"]
    nombre = cc["Nombre"]
    id_depto = cc["ID_DEPTO"]
    
    centro_cultural_data = []

    for i in range(len(nombre)):
        linea = []
        linea.append(i)
        linea.append(nombre[i])
        if np.isnan(capacidad[i]) or capacidad[i]==0:
            # cuando no hay datos de capacidad, asignamos 0 
            linea.append(0)
        else:
            linea.append(int(capacidad[i]))
        if mail[i] == "s/d" or mail[i] == "-" or type(mail[i])==float:
            linea.append(np.nan)
        else:
            linea_mail=''
            listo = False
            j=0
            while j in range(len(mail[i])) and listo==False: 
                if mail[i][j]==" ":
                    linea.append(linea_mail)
                    listo=True
                    j=0
                else:
                    linea_mail = linea_mail + mail[i][j]
                    j=j+1
            if listo==False:
                linea.append(linea_mail)
        linea.append(id_depto[i])
        centro_cultural_data.append(linea)
    encabezado = ["id","nombre","capacidad","mail","id_depto"]
    df_cc = pd.DataFrame(centro_cultural_data, columns = encabezado)
    return(df_cc)

centro_cultural = centros_culturales()
#        distintos nulls 147,162, 213, 317, 319, 324,325,327,328,332,333,334,338,343,348,351,360, 369...372, 
#        dos mails 169, 175, 183, 203, 246, 252, 277, 287, 321
#        no valida 373
#        \n 942
#%% ARMAMOS ESTABLECIMIENTO_EDUCATIVO
def establecimiento_educativo():
    e = pd.read_excel("tp1/TablasOriginales/2022_padron_oficial_establecimientos_educativos.xlsx",skiprows=5)

    cueanexo = e["Unnamed: 1"]
    jardin_1 = e["Común"]
    jardin_2 = e["Unnamed: 21"]
    primaria_1 = e["Unnamed: 22"]
    secu_1= e["Unnamed: 23"]
    secu_2= e["Unnamed: 24"]
    secu_3= e["Unnamed: 25"]
    secu_4= e["Unnamed: 26"]
    codigo_depto = e["Unnamed: 9"]

    establecimiento_educativo_data = []

    for i in range(1,len(jardin_1)):
        linea = []    
        linea.append(cueanexo[i])
        linea.append(str(codigo_depto[i])[:5])
        if jardin_1[i] != " " or jardin_2[i] != " ":
            linea.append("1")
        else: 
            linea.append("0")
        if secu_1[i] != " " or secu_2[i] != " " or secu_3[i] != " " or secu_4[i] != " ":
            linea.append("1")
        else: 
            linea.append("0")
        if primaria_1[i] != " ":
            linea.append("1")
        else: 
            linea.append("0")
        establecimiento_educativo_data.append(linea)

    encabezado_establecimiento_educativo = ["id","id_depto","jardines","primarias","secundarias"]
    df_establecimiento_educativo = pd.DataFrame(establecimiento_educativo_data, columns=encabezado_establecimiento_educativo)
    df_establecimiento_educativo['jardines'] = df_establecimiento_educativo['jardines'].astype(int)
    df_establecimiento_educativo['primarias'] = df_establecimiento_educativo['primarias'].astype(int)
    df_establecimiento_educativo['secundarias'] = df_establecimiento_educativo['secundarias'].astype(int)

    df_establecimiento_educativo.loc[df_establecimiento_educativo['id_depto'].str.startswith('02'), 'id_depto'] = '02000'
    return(df_establecimiento_educativo)

establecimiento_educativo = establecimiento_educativo()
#%% ARMAMOS PADRON
#Nombramos columnas y agregamos id_depto
df = pd.read_csv('tp1/TablasOriginales/padron_poblacion.xlsX - Output.csv', skiprows=12)
df = df.drop('Unnamed: 0', axis=1)

df.columns = df.iloc[2]

df['id_depto'] = '00'
# Eliminamos el resumen final de la tabla
df = df.iloc[:-119]
# Agregamos el codigo del departamento a cada fila y eliminamos los nombres de areas de filas

area = ''

for index, e in df.iterrows():
    if isinstance(e['Edad'], str) and e['Edad'].startswith('A'):
        area = e['Edad'][7:12]
    elif isinstance(e['Edad'], str) and e['Edad'].isnumeric():
        df.loc[index, 'id_depto'] = area

df = df.dropna()
df = df[df['id_depto'] != '00']
df = df.drop(['%', 'Acumulado %'], axis=1)
df['Edad'] = df['Edad'].astype(int)
df['Casos'] =  df['Casos'].str.replace(' ', '').astype(int)
df.loc[df['id_depto'].str.startswith('02'), 'id_depto'] = '02000'

# Renombramos y agrupamos por grupos etarios
df = df.rename(columns={"Edad": "edad", "Casos": "habitantes"})
padron = dd.sql("""
                SELECT id_depto,
                CASE 
                    WHEN edad <= 5 THEN '0-5'
                    WHEN edad > 5 AND edad <= 11 THEN '6-11'
                    WHEN edad>11 AND edad <=18 THEN '12-18'
                    WHEN edad>18 AND edad <=65 THEN '18-65'
                    ELSE '>65'
                END AS grupo_etario,
                SUM(habitantes) AS habitantes
                FROM  df
                GROUP BY id_depto, grupo_etario;
                """).df()
                
            
#padron.to_csv('TablasModelo') para agregar el archivo a la carpeta
#%% ARMAMOS PROVINCIA Y DEPARTAMENTO
df = pd.read_csv('tp1/TablasOriginales/centros_culturales.csv', dtype={'ID_PROV': str, 
                                                                       'ID_DEPTO': str})
provincia = dd.sql("""
                   SELECT DISTINCT ID_PROV AS id, Provincia AS nombre
                   FROM df
                   """).df()
df = df.dropna(subset=['Departamento'])
departamento = dd.sql("""
                   SELECT DISTINCT ID_DEPTO as id_depto, 
                                   Departamento AS nombre_depto,
                                   ID_PROV AS id_prov
                   FROM df 
                   """).df()
                   
#%% Analisis de datos
#ej i)
# A cada depto le agregamos provincia y total de ee
# El siguiente dataframe (depto_y_prov) es utilizado varias veces en otros puntos tambien
depto_y_prov = dd.sql("""
                      SELECT id_depto, p.nombre AS prov_nombre, d.nombre_depto AS depto_nombre
                      FROM departamento AS d
                      INNER JOIN provincia AS p
                      ON p.id = d.id_prov;
                      """).df()

ee_por_depto_niveles = dd.sql("""
                      SELECT id_depto, SUM(jardines) AS jardines,
                                       SUM(primarias) AS primarias,
                                       SUM(secundarias) AS secundarias
                      FROM establecimiento_educativo AS ee
                      GROUP BY id_depto;
                      """).df()
ee_por_depto_niveles_y_prov = dd.sql("""
                      SELECT d.id_depto, prov_nombre, depto_nombre, jardines, primarias, secundarias
                      FROM depto_y_prov AS d
                      INNER JOIN ee_por_depto_niveles AS ee
                      ON d.id_depto=ee.id_depto;
                      """).df()
# Sacamos del padron las poblaciones                      
pob_jardin = dd.sql("""
                      SELECT id_depto, habitantes AS poblacion_jardin
                      FROM padron AS p
                      WHERE grupo_etario = '0-5';
                      """).df()
pob_primaria = dd.sql("""
                      SELECT id_depto, habitantes AS poblacion_primaria
                      FROM padron AS p
                      WHERE grupo_etario = '6-11';
                      """).df()
pob_secundaria = dd.sql("""
                      SELECT id_depto, habitantes AS poblacion_secundaria
                      FROM padron AS p
                      WHERE grupo_etario = '12-18';
                      """).df()
poblaciones = dd.sql("""
                      SELECT id_depto, poblacion_jardin, 
                                       poblacion_primaria, 
                                       poblacion_secundaria
                      FROM pob_jardin
                      NATURAL JOIN pob_primaria 
                      NATURAL JOIN pob_secundaria;
                      """).df()
# Armamos la ultima tabla
ee_poblacion_por_depto_y_prov = dd.sql("""
                      SELECT prov_nombre AS Provincia, depto_nombre AS Departamento, 
                             jardines AS Jardines, 
                             poblacion_jardin AS "Poblacion jardin", 
                             primarias AS Primarias, 
                             poblacion_primaria AS "Poblacion primaria",
                             secundarias AS Secundarias, 
                             poblacion_secundaria AS "Poblacion secundaria"
                      FROM ee_por_depto_niveles_y_prov AS ee
                      INNER JOIN poblaciones AS p
                      ON ee.id_depto = p.id_depto
                      ORDER BY prov_nombre, primarias DESC;
                      """).df()    
#%% ej ii)
cc_cap100 = dd.sql("""
                      SELECT *
                      FROM centro_cultural AS cc
                      WHERE capacidad > 100;
                      """).df()    
cc_cap100_por_depto = dd.sql("""
                      SELECT id_depto, COUNT(*) AS cant
                      FROM cc_cap100 AS cc
                      GROUP BY id_depto;
                      """).df()    

cc_cap100_por_depto_y_prov = dd.sql("""
                      SELECT prov_nombre, depto_nombre, cant
                      FROM depto_y_prov AS d
                      NATURAL JOIN cc_cap100_por_depto AS cc
                      ORDER BY prov_nombre, cant DESC;
                      """).df()    

#%% ej iii)
#FALTA UN DEPTO
cc_por_depto = dd.sql("""
                      SELECT id_depto, COUNT(*) AS Cant_CC
                      FROM centro_cultural AS cc
                      GROUP BY id_depto;
                      """).df()
ee_por_depto = dd.sql("""
                      SELECT id_depto, COUNT(*) AS Cant_EE
                      FROM establecimiento_educativo AS ee
                      GROUP BY id_depto;
                      """).df()
                     
poblacion_por_depto = dd.sql("""
                      SELECT id_depto, SUM(habitantes) AS Poblacion
                      FROM padron AS p
                      GROUP BY id_depto;
                      """).df()
prov_depto_ee_cc_pob = dd.sql("""
                      SELECT prov_nombre, depto_nombre, Cant_EE, Cant_CC, Poblacion
                      FROM depto_y_prov
                      NATURAL JOIN cc_por_depto
                      NATURAL JOIN ee_por_depto
                      NATURAL JOIN poblacion_por_depto
                      ORDER BY Cant_EE DESC, Cant_CC DESC, prov_nombre ASC, depto_nombre ASC;
                      """).df()
#%% ej iv)
dominio_mail_por_depto = dd.sql("""
                      SELECT id_depto, 
                             LOWER(SUBSTRING(mail, CHARINDEX('@', mail) + 1, 
                                       CHARINDEX('.', mail, CHARINDEX('@', mail))
                                       - CHARINDEX('@', mail) - 1))
                             AS dominio
                      FROM centro_cultural;
                      """).df()
cant_dominio_depto = dd.sql("""
                      SELECT id_depto, dominio, COUNT(*) AS cant
                      FROM dominio_mail_por_depto
                      GROUP BY id_depto, dominio;
                      """).df()
dominio_mas_frecuente = dd.sql("""
                      SELECT id_depto, dominio
                      FROM cant_dominio_depto AS d1
                      WHERE d1.cant = (
                                       SELECT MAX(cant)
                                       FROM cant_dominio_depto AS d2
                                       WHERE d1.id_depto=d2.id_depto
                                       );
                      """).df()
dominio_mas_frecuente_depto_y_prov = dd.sql("""
                      SELECT prov_nombre, depto_nombre, dominio AS 'Dominio más frecuente en CC'
                      FROM depto_y_prov 
                      NATURAL JOIN dominio_mas_frecuente;
                      """).df()
#%% Visualizacion de datos
#ej i)
#DUDAS
cc_por_prov = dd.sql("""
                      SELECT prov_nombre AS prov, SUM(Cant_CC) AS cant
                      FROM prov_depto_ee_cc_pob 
                      GROUP BY prov_nombre
                      ORDER BY cant DESC;
                      """).df()

fig, ax = plt.subplots()
ax.bar(cc_por_prov['prov'], cc_por_prov['cant'], color='skyblue')

ax.set_xlabel("Provincias")
ax.set_ylabel("Cantidad de centros culturales")
ax.set_title("Cantidad de centros culturales por provincia (Ordenado)")
#%%ej ii)
fig, ax = plt.subplots()

ax.scatter(ee_poblacion_por_depto_y_prov['Poblacion jardin'], 
           ee_poblacion_por_depto_y_prov['Jardines'], 
           color='#1F77B4', label='Jardines', s=14)
ax.scatter(ee_poblacion_por_depto_y_prov['Poblacion primaria'], 
           ee_poblacion_por_depto_y_prov['Primarias'], 
           color='#FF7F0E', label='Primarias', s=14)
ax.scatter(ee_poblacion_por_depto_y_prov['Poblacion secundaria'], 
           ee_poblacion_por_depto_y_prov['Secundarias'], 
           color='#2CA02C', label='Secundarias', s=14)

ax.set_xlabel("Población")
ax.set_ylabel("Establecimientos educativos(tipo común)")
ax.set_title("Establecimientos educativos vs. población")
#ax.set_xlim(0, 80000)
#ax.set_ylim(0, 270)
ax.legend()
#%%ej iii)
prov_depto_ee = dd.sql("""
                          SELECT prov_nombre, Cant_EE AS cant
                          FROM depto_y_prov AS d
                          NATURAL JOIN ee_por_depto;
                       """).df()
 
# Acortamos nombres para mejorar la visualizacion
prov_depto_ee.loc[
    prov_depto_ee['prov_nombre'] == 'Tierra del Fuego, Antártida e Islas del Atlántico Sur',
    'prov_nombre'] = 'Tierra del F.' 
prov_depto_ee.loc[
    prov_depto_ee['prov_nombre'] == 'Santiago del Estero',
    'prov_nombre'] = 'Sant. del Est.' 
#DUDA aca habria que eliminar caba...
prov_depto_ee.loc[
    prov_depto_ee['prov_nombre'] == 'Ciudad Autónoma de Buenos Aires',
    'prov_nombre'] = 'CABA' 
                      
# Calculamos medianas y ordenamos 
#DUDA : no vimos group by...
medianas = prov_depto_ee.groupby('prov_nombre')['cant'].median()
provs_ordenadas = medianas.sort_values().index

fig, ax = plt.subplots()
sns.boxplot(x='prov_nombre', y='cant', data=prov_depto_ee, order=provs_ordenadas, ax=ax)

ax.set_xlabel("Provincia")
ax.set_ylabel("Cantidad establecimientos educativos(tipo común)")
ax.set_title("Establecimientos educativos por departamento")
ax.set_ylim(0, 750)
plt.xticks(rotation=80)
"""
nombres_provincias = dd.sql(
                            SELECT DISTINCT nombre
                            FROM provincia
                            ).df()
for indice, valor in nombres_provincias['nombre'].iteritems():
"""
#%%ej iv)
cc_cada_1000 = dd.sql("""
                          SELECT c.id_depto AS id_depto, 
                                 CASE 
                                     WHEN p.Poblacion = 0 THEN 0
                                     ELSE (c.Cant_CC / p.Poblacion)*1000
                                 AS cant_cc
                          FROM cc_por_depto AS c
                          NATURAL JOIN poblacion_por_depto AS p;
                       """).df()
ee_cada_1000 = dd.sql("""
                          SELECT e.id_depto AS id_depto, 
                                 CASE 
                                     WHEN p.Poblacion = 0 THEN 0
                                     ELSE (e.Cant_EE / p.Poblacion)*1000
                                 AS cant_ee
                          FROM ee_por_depto AS e
                          NATURAL JOIN poblacion_por_depto AS p;
                       """).df()
ee_y_cc_cada_1000 = dd.sql("""
                          SELECT e.id_depto AS id_depto, 
                                 cant_ee, cant_cc
                          FROM cc_cada_1000 AS c
                          NATURAL JOIN ee_cada_1000;
                       """).df()
                       
fig, ax = plt.subplots()
ax.scatter(ee_y_cc_cada_1000['cant_ee'], 
           ee_y_cc_cada_1000['cant_cc'], 
           color='pink', s=10)

ax.set_ylabel("Centros culturales cada 1000 habitantes")
ax.set_xlabel("Establecimientos educativos cada 1000 habitantes")
ax.set_title("Centros culturales vs. establecimientos educativos")
