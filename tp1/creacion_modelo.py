import pandas as pd
import duckdb as dd

#%% Nombramos columnas y agregamos i_depto
df = pd.read_csv('TablasOriginales/padron_poblacion.xlsX - Output.csv', skiprows=12)
df = df.drop('Unnamed: 0', axis=1)

df.columns = df.iloc[2]

df['id_depto'] = '00'
#%% Agregamos el codigo del departamento a cada fila y eliminamos los nombres de areas de filas

area = ''

for index, e in df.iterrows():
    if isinstance(e['Edad'], str) and e['Edad'].startswith('A'):
        area = e['Edad'][7:12]
    elif isinstance(e['Edad'], str) and e['Edad'].isnumeric():
        asdf = 1
        df.loc[index, 'id_depto'] = area

df = df.dropna()
df = df[df['id_depto'] != '00']
df = df.drop(['%', 'Acumulado %'], axis=1)
df['Edad'] = df['Edad'].astype(int)
df['Casos'] =  df['Casos'].str.replace(' ', '').astype(int)
#%% Renombramos y agrupamos por grupos etarios
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
                GROUP BY id_depto, grupo_etario
                """).df()
#padron.to_csv('TablasModelo') para agregar el archivo a la carpeta
