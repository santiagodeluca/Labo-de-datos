import pandas as pd
import duckdb as dd


#%%===========================================================================

casos = pd.read_csv('calidad_de_datos/DatosDengueYZikaCorregida.csv')

#%%===========================================================================

depto_prov = dd.sql("""
               SELECT departamento_id, departamento_nombre, provincia_id, provincia_nombre
               FROM casos
               GROUP BY departamento_id, departamento_nombre, provincia_id, provincia_nombre;
              """).df()

consultaSQL = """
                SELECT * 
                FROM depto_prov as d1
                WHERE EXISTS
                    (SELECT *
                     FROM depto_prov AS d2
                     WHERE (d2.departamento_id != d1.departamento_id 
                            OR d2.provincia_id != d1.provincia_id)
                     AND d2.departamento_nombre = d1.departamento_nombre)
                ORDER BY departamento_nombre;
                """

dataframeResultado = dd.sql(consultaSQL).df()
