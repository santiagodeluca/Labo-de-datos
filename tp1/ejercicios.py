import pandas as pd
import duckdb as dd
import matplotlib.pyplot as plt
import seaborn as sns

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
#%% Sacamos del padron las poblaciones                      
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
#%% Armamos la ultima tabla
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
                      SELECT id_depto, COUNT(*) AS cant>100
                      FROM cc_cap100 AS cc
                      GROUP BY id_depto;
                      """).df()    

cc_cap100_por_depto_y_prov = dd.sql("""
                      SELECT prov_nombre, depto_nombre, cant>100
                      FROM depto_y_prov AS d
                      INNER JOIN cc_cap100_por_depto AS cc
                      ON d.id_depto=cc.id_depto
                      ORDER BY prov_nombre, cant>100 DESC;
                      """).df()    

#%% ej iii)
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
                      SELECT prov_nombre, depto_nombre, dominio AS 'Dominio mas frecuente en CC'
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
           color='#A6CEE3', label='Jardines', s=10)
ax.scatter(ee_poblacion_por_depto_y_prov['Poblacion primaria'], 
           ee_poblacion_por_depto_y_prov['Primarias'], 
           color='#1F78B4', label='Primarias', s=10)
ax.scatter(ee_poblacion_por_depto_y_prov['Poblacion secundaria'], 
           ee_poblacion_por_depto_y_prov['Secundarias'], 
           color='#08306B', label='Secundarias', s=10)

ax.set_xlabel("Población")
ax.set_ylabel("Cantidad establecimientos educativos de tipo común")
ax.set_title("Cantidad de establecimientos educativos por población")
ax.set_xlim(0, 80000)
ax.set_ylim(0, 270)
ax.legend()
#%%ej iii)
#tal vez se puede sacar id_depto de aca
prov_depto_ee = dd.sql("""
                          SELECT d.id_depto, prov_nombre, Cant_EE AS cant
                          FROM depto_y_prov AS 
                          NATURAL JOIN ee_por_depto
                       """).df()
                       
medianas = prov_depto_ee.groupby('prov_nombre')['cant'].median()
provs_ordenadas = medianas.sort_values().index

fig, ax = plt.subplots()
prov_depto_ee.boxplot(by='prov_nombre', column='cant', ax=ax, 
                      order=provs_ordenadas)
"""
nombres_provincias = dd.sql(
                            SELECT DISTINCT nombre
                            FROM provincia
                            ).df()
for indice, valor in nombres_provincias['nombre'].iteritems():
"""