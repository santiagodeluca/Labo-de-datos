import pandas as pd
import duckdb as dd

#%%===========================================================================

casos = pd.read_csv("C:/Users/santi/Labo de datos/clase5/Guía Práctica - SQL - Archivos adjuntos-20250205/casos.csv")
departamento = pd.read_csv("C:/Users/santi/Labo de datos/clase5/Guía Práctica - SQL - Archivos adjuntos-20250205/departamento.csv")
grupoetario = pd.read_csv("C:/Users/santi/Labo de datos/clase5/Guía Práctica - SQL - Archivos adjuntos-20250205/grupoetario.csv")
provincia = pd.read_csv("C:/Users/santi/Labo de datos/clase5/Guía Práctica - SQL - Archivos adjuntos-20250205/provincia.csv")
tipoevento = pd.read_csv("C:/Users/santi/Labo de datos/clase5/Guía Práctica - SQL - Archivos adjuntos-20250205/tipoevento.csv")

#%%===========================================================================
#EJERCICIO A 
#PUNTO a: Listar sólo los nombres de todos los departamentos que hay en la tabla departamento (dejando los registros repetidos).

consultaSQL = """
               SELECT descripcion
               FROM departamento
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO b: Listar sólo los nombres de todos los departamentos que hay en la tabla departamento (eliminando los registros repetidos).

consultaSQL = """
               SELECT DISTINCT descripcion
               FROM departamento
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO c: Listar sólo los códigos de departamento y sus nombres, de todos los departamentos que hay en la tabla departamento. 

consultaSQL = """
               SELECT DISTINCT id, descripcion
               FROM departamento
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#-?PUNTO d: Listar todas las columnas de la tabla departamento

consultaSQL = """
               SELECT *
               FROM departamento
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO e: Listar los códigos de departamento y nombres de todos los departamentos
#que hay en la tabla departamento. Utilizar los siguientes alias para las
#columnas: codigo_depto y nombre_depto, respectivamente.

consultaSQL = """
               SELECT DISTINCT id AS codigo_depto, descripcion AS nombre_depto
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO f: Listar los registros de la tabla departamento cuyo código de provincia es igual a 54

consultaSQL = """
               SELECT *
               FROM departamento
               WHERE id_provincia = 54;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO g: Listar los registros de la tabla departamento cuyo código de provincia es igual a 22, 78 u 86.


consultaSQL = """
               SELECT *
               FROM departamento
               WHERE id_provincia = 22
               OR id_provincia = 78
               OR id_provincia = 86;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO A 
#PUNTO h: Listar los registros de la tabla departamento cuyos códigos de provincia se encuentren entre el 50 y el 59 (ambos valores inclusive).

consultaSQL = """
               SELECT *
               FROM departamento
               WHERE id_provincia >= 50 
               AND id_provincia <= 59;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#FIN EJERCICIO A
#%%===========================================================================
#EJERCICIO B
#PUNTO a: Devolver una lista con los código y nombres de departamentos, asociados al
#nombre de la provincia al que pertenecen
consultaSQL = """
               SELECT departamento.id AS codigo, provincia.descripcion AS provincia
               FROM departamento
               INNER JOIN provincia
               ON departamento.id_provincia = provincia.id;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO B
#PUNTO c: Devolver los casos registrados en la provincia de “Chaco”.
codigos_depto = dd.sql("""
               SELECT departamento.id AS codigo, provincia.descripcion AS provincia
               FROM departamento
               INNER JOIN provincia
               ON departamento.id_provincia = provincia.id;
              """).df()

consultaSQL = """
               SELECT id, id_tipoevento, anio, semana_epidemiologica, id_depto, id_grupoetario, cantidad
               FROM casos
               INNER JOIN codigos_depto
               ON id_depto = codigo
               WHERE provincia = 'Chaco';
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO B
#PUNTO d: Devolver aquellos casos de la provincia de “Buenos Aires” cuyo campo
#cantidad supere los 10 casos.

codigos_depto = dd.sql("""
               SELECT departamento.id AS codigo, provincia.descripcion AS provincia
               FROM departamento
               INNER JOIN provincia
               ON departamento.id_provincia = provincia.id;
              """).df()

consultaSQL = """
               SELECT id, id_tipoevento, anio, semana_epidemiologica, id_depto, id_grupoetario, cantidad
               FROM casos
               INNER JOIN codigos_depto
               ON id_depto = codigo
               WHERE provincia = 'Buenos Aires'
               AND cantidad > 10;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#FIN EJERCICIO B
#%%===========================================================================
#EJERCICIO C
#-?PUNTO a: Devolver un listado con los nombres de los departamentos que no tienen
#ningún caso asociado.


consultaSQL = """
               SELECT descripcion
               FROM departamento
               LEFT OUTER JOIN casos
               ON departamento.id = id_depto
               WHERE cantidad IS NULL;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO C
#PUNTO b:  Devolver un listado con los tipos de evento que no tienen ningún caso
#asociado.


consultaSQL = """
               SELECT descripcion
               FROM tipoevento
               LEFT OUTER JOIN casos
               ON tipoevento.id = id_tipoevento
               WHERE cantidad IS NULL;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO a: Calcular la cantidad total de casos que hay en la tabla casos


consultaSQL = """
               SELECT COUNT(*) AS cantidad_total
               FROM casos;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO b: Calcular la cantidad total de casos que hay en la tabla casos para cada año y
#cada tipo de caso. Presentar la información de la siguiente manera:
#descripción del tipo de caso, año y cantidad. Ordenarlo por tipo de caso
#(ascendente) y año (ascendente).


consultaSQL = """
               SELECT tipoevento.descripcion, anio, SUM(cantidad) AS cantidad_casos
               FROM casos
               INNER JOIN tipoevento
               ON tipoevento.id = id_tipoevento
               GROUP BY anio, tipoevento.descripcion
               ORDER BY tipoevento.descripcion, anio;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO c: Misma consulta que el ítem anterior, pero sólo para el año 2019.



consultaSQL = """
               SELECT tipoevento.descripcion, anio, SUM(cantidad) AS cantidad_casos
               FROM casos
               INNER JOIN tipoevento
               ON tipoevento.id = id_tipoevento
               WHERE anio = 2019
               GROUP BY anio, tipoevento.descripcion
               ORDER BY tipoevento.descripcion, anio;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO d: Calcular la cantidad total de departamentos que hay por provincia. Presentar
#la información ordenada por código de provincia.

consultaSQL = """
               SELECT provincia.id AS identificacion, provincia.descripcion AS provincia, COUNT(*) AS cantidad_deptos
               FROM departamento
               INNER JOIN provincia
               ON id_provincia = provincia.id
               GROUP BY provincia.descripcion, identificacion
               ORDER BY provincia.id;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO e: Listar los departamentos con menos cantidad de casos en el año 2019.


consultaSQL = """
               SELECT departamento.id AS identificacion, descripcion AS nombre_depto, SUM(cantidad) AS cantidad_casos
               FROM departamento
               LEFT OUTER JOIN casos
               ON id_depto = departamento.id
               WHERE anio = 2019
               GROUP BY identificacion, nombre_depto
               ORDER BY cantidad_casos;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO f: Listar los departamentos con mayor cantidad de casos en el año 2020.


consultaSQL = """
               SELECT departamento.id AS identificacion, descripcion AS nombre_depto, SUM(cantidad) AS cantidad_casos
               FROM departamento
               LEFT OUTER JOIN casos
               ON id_depto = departamento.id
               WHERE anio = 2020
               GROUP BY identificacion, nombre_depto
               ORDER BY cantidad_casos DESC;
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#-??PUNTO g: Listar el promedio de cantidad de casos por provincia y año.

suma_casos = dd.sql("""
               SELECT provincia.descripcion AS prov, anio, SUM(cantidad) AS casos_anuales
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON provincia.id = departamento.id_provincia
               GROUP BY provincia.descripcion, anio
              """).df()

consultaSQL = """
               SELECT prov, AVG(casos_anuales) AS promedio_anual
               FROM suma_casos
               GROUP BY prov
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#???PUNTO h: Listar, para cada provincia y año, cuáles fueron los departamentos que más
#cantidad de casos tuvieron.


casos_depto_anio = dd.sql("""
               SELECT anio, provincia.descripcion AS prov, provincia.id AS prov_id, departamento.descripcion AS depto, departamento.id as depto_id, SUM(cantidad) AS cantidad_casos
               FROM departamento
               INNER JOIN provincia
               ON provincia.id = id_provincia
               INNER JOIN casos
               ON casos.id_depto = departamento.id
               GROUP BY anio, provincia.id, provincia.descripcion, departamento.descripcion, departamento.id
              """).df()
              
consultaSQL = """
               SELECT anio,prov, prov_id, depto,  MAX(cantidad_casos) AS maximos_casos
               FROM casos_depto_anio
               GROUP BY anio, prov, prov_id, depto_id,depto
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO i:Mostrar la cantidad de casos total, máxima, mínima y promedio que tuvo la
#provincia de Buenos Aires en el año 2019.

consultaSQL = """
               SELECT SUM(cantidad) AS casos, MAX(cantidad) AS maximo, MIN(cantidad) AS minimo, AVG(cantidad) AS promedio
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               WHERE provincia.descripcion = 'Buenos Aires'
               AND anio = 2019
               GROUP BY provincia.descripcion
               """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO j: Misma consulta que el ítem anterior, pero sólo para aquellos casos en que la
#cantidad total es mayor a 1000 casos.


consultaSQL = """
               SELECT provincia.descripcion, anio, SUM(cantidad) AS casos_totales, MAX(cantidad) AS maximo, MIN(cantidad) AS minimo, AVG(cantidad) AS promedio
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               GROUP BY provincia.descripcion, anio
               HAVING casos_totales > 1000
               """

dataframeResultado = dd.sql(consultaSQL).df()
#%%===========================================================================
#EJERCICIO D
#PUNTO K:Listar los nombres de departamento (y nombre de provincia) que tienen
#mediciones tanto para el año 2019 como para el año 2020. Para cada uno de
#ellos devolver la cantidad de casos promedio. Ordenar por nombre de
#provincia (ascendente) y luego por nombre de departamento (ascendente).

consultaSQL = """
               SELECT departamento.descripcion AS depto, provincia.descripcion AS provincia, AVG(cantidad) AS promedio
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               GROUP BY provincia.descripcion, departamento.descripcion
               ORDER BY provincia.descripcion, departamento.descripcion
               """

#%%===========================================================================
#EJERCICIO D
#PUNTO l: Devolver una tabla que tenga los siguientes campos: descripción de tipo de
#evento, id_depto, nombre de departamento, id_provincia, nombre de
#provincia, total de casos 2019, total de casos 2020.

casos_xdepto_19 = dd.sql("""
               SELECT departamento.id AS id, departamento.descripcion AS depto, provincia.descripcion AS provincia, SUM(cantidad) AS casos19, casos.id_tipoevento AS tipoevento
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               WHERE anio = 2019
               GROUP BY departamento.id, departamento.descripcion, provincia.descripcion, casos.id_tipoevento
              """).df()
casos_xdepto_20 = dd.sql("""
               SELECT departamento.id AS id, departamento.descripcion AS depto, provincia.descripcion AS provincia, SUM(cantidad) AS casos20, casos.id_tipoevento AS tipoevento
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               WHERE anio = 2020
               GROUP BY departamento.id, departamento.descripcion, provincia.descripcion, casos.id_tipoevento
              """).df()


consultaSQL = """
               SELECT casos_xdepto_20.tipoevento, departamento.id AS id_depto, departamento.descripcion AS depto, provincia.id AS id_prov, provincia.descripcion AS provincia, casos19, casos20
               FROM casos
               INNER JOIN departamento
               ON id_depto = departamento.id
               INNER JOIN provincia
               ON id_provincia = provincia.id
               INNER JOIN casos_xdepto_19
               ON casos_xdepto_19.id  = departamento.id AND casos_xdepto_19.tipoevento = casos.id_tipoevento
               INNER JOIN casos_xdepto_20
               ON casos_xdepto_20.id  = departamento.id AND casos_xdepto_20.tipoevento = casos.id_tipoevento
               GROUP BY casos_xdepto_20.tipoevento, departamento.id, departamento.descripcion, provincia.id, provincia.descripcion, casos19, casos20
               """

dataframeResultado = dd.sql(consultaSQL).df()
