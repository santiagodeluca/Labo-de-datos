# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase SQL. Script clase. 
Autor  : Pablo Turjanski
Fecha  : 2025-02-03
"""

# Importamos bibliotecas
import pandas as pd
import duckdb as dd


#%%===========================================================================
# Importamos los datasets que vamos a utilizar en este programa
#=============================================================================

carpeta = "~/Labo-de-datos/clase5/Clases 05-07 - SQL - Archivos clase (template script + datos)-20250204/"

# Ejercicios AR-PROJECT, SELECT, RENAME
empleado       = pd.read_csv(carpeta+"empleado.csv")
# Ejercicios AR-UNION, INTERSECTION, MINUS
alumnosBD      = pd.read_csv(carpeta+"alumnosBD.csv")
alumnosTLeng   = pd.read_csv(carpeta+"alumnosTLeng.csv")
# Ejercicios AR-CROSSJOIN
persona        = pd.read_csv(carpeta+"persona.csv")
nacionalidades = pd.read_csv(carpeta+"nacionalidades.csv")
# Ejercicios ¿Mismos Nombres?
se_inscribe_en=pd.read_csv(carpeta+"se_inscribe_en.csv")
materia       =pd.read_csv(carpeta+"materia.csv")
# Ejercicio JOIN múltiples tablas
vuelo      = pd.read_csv(carpeta+"vuelo.csv")    
aeropuerto = pd.read_csv(carpeta+"aeropuerto.csv")    
pasajero   = pd.read_csv(carpeta+"pasajero.csv")    
reserva    = pd.read_csv(carpeta+"reserva.csv")    
# Ejercicio JOIN tuplas espúreas
empleadoRol= pd.read_csv(carpeta+"empleadoRol.csv")    
rolProyecto= pd.read_csv(carpeta+"rolProyecto.csv")    
# Ejercicios funciones de agregación, LIKE, Elección, Subqueries 
# y variables de Python
examen     = pd.read_csv(carpeta+"examen.csv")
# Ejercicios de manejo de valores NULL
examen03 = pd.read_csv(carpeta+"examen03.csv")



#%%===========================================================================
# Ejemplo inicial
#=============================================================================

print(empleado)

consultaSQL = """
               SELECT DISTINCT DNI, Salario
               FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()

print(dataframeResultado)


#%%===========================================================================
# Ejercicios AR-PROJECT <-> SELECT
#=============================================================================
# a.- Listar DNI y Salario de empleados 
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Listar Sexo de empleados 
consultaSQL = """
               SELECT Sexo
               FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
#c.- Listar Sexo de empleados (sin DISTINCT)
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios AR-SELECT <-> WHERE
#=============================================================================
# a.- Listar de EMPLEADO sólo aquellos cuyo sexo es femenino
consultaSQL = """
                    SELECT DISTINCT DNI, Nombre, Sexo, Salario
                    FROM empleado
                    WHERE Sexo='F';
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
#b.- Listar de EMPLEADO aquellos cuyo sexo es femenino y su salario es mayor a $15.000
consultaSQL = """
                    SELECT DISTINCT DNI, Nombre, Sexo, Salario
                    FROM empleado
                    WHERE Sexo='F' AND Salario>15000;

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios AR-RENAME <-> AS
#=============================================================================
#a.- Listar DNI y Salario de EMPLEADO, y renombrarlos como id e Ingreso
consultaSQL = """
                    SELECT DISTINCT DNI AS Id, Salario AS Ingreso
                    FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 01                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#%%===========================================================================
# EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 01
#=============================================================================
# Ejercicio 01.1.- Retornar Codigo y Nombre de los aeropuertos de Londres
consultaSQL = """
                SELECT DISTINCT Codigo, Nombre
                FROM aeropuerto
                WHERE Ciudad = 'Londres';
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.2.- ¿Qué retorna 
#                       SELECT DISTINCT Ciudad AS City 
#                       FROM aeropuerto 
#                       WHERE Codigo='ORY' OR Codigo='CDG'; ?
consultaSQL = """
                       SELECT DISTINCT Ciudad AS City 
                       FROM aeropuerto 
                       WHERE Codigo='ORY' OR Codigo='CDG'; 

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.3.- Obtener los números de vuelo que van desde CDG hacia LHR
consultaSQL = """
                SELECT DISTINCT Numero
                FROM vuelo
                WHERE Origen= 'CDG' AND Destino='LHR'
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.4.- Obtener los números de vuelo que van desde CDG hacia LHR o viceversa
consultaSQL = """
                SELECT DISTINCT Numero
                FROM vuelo
                WHERE (Origen= 'CDG' AND Destino='LHR') OR (Origen= 'LHR' AND Destino='CDG')

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.5.- Devolver las fechas de reservas cuyos precios son mayores a $200
consultaSQL = """
                SELECT DISTINCT Fecha
                FROM reserva
                WHERE Precio > 200;
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 01                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
#=============================================================================
# Ejercicios AR-UNION, INTERSECTION, MINUS <-> UNION, INTERSECTION, EXCEPT
#=============================================================================
# a1.- Listar a los alumnos que cursan BDs o TLENG

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% -----------
# a2.- Listar a los alumnos que cursan BDs o TLENG (usando UNION ALL)

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# b.- Listar a los alumnos que cursan simultáneamente BDs y TLENG

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# c.- Listar a los alumnos que cursan BDs y no cursan TLENG 

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 02                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#=============================================================================
#  EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 02
#=============================================================================
# Ejercicio 02.1.- Devolver los números de vuelo que tienen reservas generadas (utilizar intersección)
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 02.2.- Devolver los números de vuelo que aún no tienen reservas
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 02.3.- Retornar los códigos de aeropuerto de los que parten o arriban los vuelos
consultaSQL = """

              """
              
dataframeResultado = dd.sql(consultaSQL).df()



#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 02                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#=============================================================================
# Ejercicios AR-... JOIN <-> ... JOIN
#=============================================================================
# a1.- Listar el producto cartesiano entre las tablas persona y nacionalidades

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# a2.- Listar el producto cartesiano entre las tablas persona y nacionalidades (sin usar CROSS JOIN)

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% --------------------------------------------------------------------------------------------
# Carga los nuevos datos del dataframe persona para los ejercicios de AR-INNER y LEFT OUTER JOIN
# ----------------------------------------------------------------------------------------------
persona        = pd.read_csv(carpeta+"persona_ejemplosJoin.csv")
# ----------------------------------------------------------------------------------------------
# b1.- Vincular las tablas persona y nacionalidades a través de un INNER JOIN

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b2.- Vincular las tablas persona y nacionalidades (sin usar INNER JOIN)

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# c.- Vincular las tablas persona y nacionalidades a través de un LEFT OUTER JOIN

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - ¿Mismos Nombres?
#=============================================================================
# a.- Vincular las tablas Se_inscribe_en y Materia. Mostrar sólo LU y Nombre de materia

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

    
#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 03                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#%%===========================================================================
# EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 03
#=============================================================================
# Ejercicio 03.1.- Devolver el nombre de la ciudad de partida del vuelo número 165

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 03.2.- Retornar el nombre de las personas que realizaron reservas a un valor menor a $200

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 03.3.- Obtener Nombre, Fecha y Destino del Viaje de todos los pasajeros que vuelan desde Madrid

vuelosAMadrid = dd.sql("""

              """).df()

dniPersonasDesdeMadrid = dd.sql("""

              """).df()

consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 03                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    
#%%===========================================================================
# Ejercicios SQL - Join de varias tablas en simultáneo
#=============================================================================
# a.- Vincular las tablas Reserva, Pasajero y Vuelo. Mostrar sólo Fecha de reserva, hora de salida del vuelo y nombre de pasajero.
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

    
#%%===========================================================================
# Ejercicios SQL - Tuplas espúreas
#=============================================================================
# a.- Vincular (JOIN)  EmpleadoRol y RolProyecto para obtener la tabla original EmpleadoRolProyecto
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - Funciones de agregación
#=============================================================================
# a.- Usando sólo SELECT contar cuántos exámenes fueron rendidos (en total)
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# b1.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# b2.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia (ordenado por instancia)
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# b3.- Ídem ejercicio anterior, pero mostrar sólo las instancias a las que asistieron menos de 4 Estudiantes
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# c.- Mostrar el promedio de edad de los estudiantes en cada instancia de examen
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - LIKE")
#=============================================================================
# a1.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial.
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# a2.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial. Esta vez usando LIKE.
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - Eligiendo
#=============================================================================
# a1.- Listar a cada alumno que rindió el Parcial-01 y decir si aprobó o no (se aprueba con nota >=4).
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# a2.- Modificar la consulta anterior para que informe cuántos estudiantes aprobaron/reprobaron en cada instancia.
    
consultaSQL = """

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - Subqueries
#=============================================================================
#a.- Listar los alumnos que en cada instancia obtuvieron una nota mayor al promedio de dicha instancia

promedio_instancia = dd.sql("""
                            SELECT Instancia, AVG(Nota) AS promedio
                            FROM examen
                            GROUP BY Instancia
              """).df()


consultaSQL = """
                SELECT Nombre, examen.Instancia, Nota
                FROM examen
                INNER JOIN promedio_instancia
                ON promedio_instancia.Instancia = examen.Instancia
                WHERE  Nota > promedio
              """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# b.- Listar los alumnos que en cada instancia obtuvieron la mayor nota de dicha instancia

consultaSQL = """
                SELECT Nombre, Instancia, Nota
                FROM examen AS e1
                WHERE e1.Nota = (
                    SELECT MAX(Nota)
                    FROM examen AS e2 
                    WHERE e2.Instancia = e1.Instancia 
                    )
                ORDER BY Nombre
              """
              
OtraconsultaSQL = """
                SELECT Nombre, Instancia, Nota
                FROM examen AS e1
                WHERE e1.Nota >= ALL (
                    SELECT e2.Nota
                    FROM examen AS e2 
                    WHERE e2.Instancia = e1.Instancia 
                    )
                ORDER BY Nombre
              """
              
              

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# c.- Listar el nombre, instancia y nota sólo de los estudiantes que no rindieron ningún Recuperatorio

consultaSQL = """
                SELECT Nombre, Instancia, Nota
                FROM examen AS e1
                WHERE e1.Nombre <> ALL (
                    SELECT Nombre
                    FROM examen AS e2 
                    WHERE e2.Instancia LIKE 'Recu%'
                    )
                ORDER BY Nombre

              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - Integrando variables de Python
#=============================================================================
# a.- Mostrar Nombre, Instancia y Nota de los alumnos cuya Nota supera el umbral indicado en la variable de Python umbralNota

umbralNota = 7

consultaSQL = f"""
                SELECT Nombre, Instancia, Nota
                FROM examen 
                WHERE Nota > {umbralNota}
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - Manejo de NULLs
#=============================================================================
# a.- Listar todas las tuplas de Examen03 cuyas Notas son menores a 9

consultaSQL = """
                SELECT * 
                FROM examen03
                WHERE Nota < 9;
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Listar todas las tuplas de Examen03 cuyas Notas son mayores o iguales a 9

consultaSQL = """
                SELECT * 
                FROM examen03
                WHERE Nota >= 9;

              """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# c.- Listar el UNION de todas las tuplas de Examen03 cuyas Notas son menores a 9 y las que son mayores o iguales a 9

consultaSQL = """
                SELECT * 
                FROM examen03
                WHERE Nota < 9
                UNION
                SELECT * 
                FROM examen03
                WHERE Nota >= 9;

                """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# d1.- Obtener el promedio de notas

consultaSQL = """
                SELECT AVG(Nota) AS promedio
                FROM examen03
              """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# d2.- Obtener el promedio de notas (tomando a NULL==0)

consultaSQL = """
                SELECT AVG(CASE WHEN Nota IS NULL THEN 0 ELSE Nota END) AS prom
                FROM examen03;
              """


dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - Mayúsculas/Minúsculas
#=============================================================================
# a.- Consigna: Transformar todos los caracteres de las descripciones de los roles a mayúscula

consultaSQL = """
                SELECT empleado, UPPER(rol) AS rol
                FROM empleadoRol
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Consigna: Transformar todos los caracteres de las descripciones de los roles a minúscula

consultaSQL = """
                SELECT empleado, LOWER(rol) AS rol
                FROM empleadoRol

              """

dataframeResultado = dd.sql(consultaSQL).df()




#%%===========================================================================
# Ejercicios SQL - Reemplazos
#=============================================================================
# a.- Consigna: En la descripción de los roles de los empleados reemplazar las ñ por ni

consultaSQL = """
                SELECT empleado, REPLACE(rol, 'ñ', 'ni') AS rol
                FROM empleadoRol
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
# Ejercicios SQL - Desafío
#=============================================================================
# a.- Mostrar para cada estudiante las siguientes columnas con sus datos: Nombre, Sexo, Edad, Nota-Parcial-01, Nota-Parcial-02, Recuperatorio-01 y , Recuperatorio-02

# ... Paso 1: Obtenemos los datos de los estudiantes

nota1parcial = dd.sql("""
                SELECT Nombre, Edad, Nota AS Parcial_01
                FROM examen 
                WHERE Instancia='Parcial-01'
                """).df()
nota2parcial = dd.sql("""
                SELECT Nombre, Edad, Nota AS Parcial_02
                FROM examen 
                WHERE Instancia='Parcial-02'
                """).df()
nota1recu = dd.sql("""
                SELECT Nombre, Edad, Nota AS Recuperatorio_01
                FROM examen 
                WHERE Instancia='Recuperatorio-01'
                """).df()
nota2recu = dd.sql("""
                SELECT Nombre, Edad, Nota AS Recuperatorio_02
                FROM examen 
                WHERE Instancia='Recuperatorio-02'
                """).df()


join1parcial = dd.sql("""
                SELECT examen.Nombre, Sexo, examen.Edad, Parcial_01
                FROM examen
                LEFT OUTER JOIN nota1parcial
                ON examen.Nombre=nota1parcial.Nombre AND examen.Edad = nota1parcial.Edad
              """).df()
join2parcial = dd.sql("""
                SELECT join1parcial.Nombre, Sexo, join1parcial.Edad, Parcial_01, Parcial_02
                FROM join1parcial
                LEFT OUTER JOIN nota2parcial
                ON join1parcial.Nombre=nota2parcial.Nombre AND join1parcial.Edad = nota2parcial.Edad
              """).df()
join1recu = dd.sql("""
                SELECT join2parcial.Nombre, Sexo, join2parcial.Edad, Parcial_01, Parcial_02, Recuperatorio_01
                FROM join2parcial
                LEFT OUTER JOIN nota1recu
                ON join2parcial.Nombre=nota1recu.Nombre AND join2parcial.Edad = nota1recu.Edad
              """).df()
              
consultaSQL = """
                SELECT DISTINCT join1recu.Nombre, Sexo, join1recu.Edad, Parcial_01, Parcial_02, Recuperatorio_01, Recuperatorio_02
                FROM join1recu
                LEFT OUTER JOIN nota2recu
                ON join1recu.Nombre=nota2recu.Nombre AND join1recu.Edad = nota2recu.Edad
                ORDER BY join1recu.Nombre
"""


desafio_01 = dd.sql(consultaSQL).df()



#%% -----------
# b.- Agregar al ejercicio anterior la columna Estado, que informa si el alumno aprobó la cursada (APROBÓ/NO APROBÓ). Se aprueba con 4.

consultaSQL = """
                 SELECT *, 
                     CASE WHEN (Parcial_01 >=4 AND (Parcial_02>=4 OR Recuperatorio_02 >= 4))
                            OR (Parcial_02 >=4 AND Recuperatorio_01 >= 4)
                            OR (Recuperatorio_01 >=4 AND Recuperatorio_02 >=4) THEN
                            'APROBÓ'
                            ELSE 
                            'NO APROBÓ' 
                            END AS Estado
                FROM desafio_01
              """

desafio_02 = dd.sql(consultaSQL).df()



#%% -----------
# c.- Generar la tabla Examen a partir de la tabla obtenida en el desafío anterior.

parcial1 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Parcial_01' AS Instancia, Parcial_01 AS Nota
                FROM desafio_02
                WHERE Parcial_01 IS NOT NULL
                """).df()
parcial2 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Parcial_02' AS Instancia, Parcial_02 AS Nota
                FROM desafio_02
                WHERE Parcial_02 IS NOT NULL
                """).df()
recuperatorio1 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Recuperatorio_01' AS Instancia, Recuperatorio_01 AS Nota
                FROM desafio_02
                WHERE Recuperatorio_01 IS NOT NULL
                """).df()
recuperatorio2 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Recuperatorio_02' AS Instancia, Recuperatorio_02 AS Nota
                FROM desafio_02
                WHERE Recuperatorio_02 IS NOT NULL
                """).df()


consultaSQL = """
                SELECT * 
                FROM parcial1
                UNION
                SELECT * 
                FROM parcial2
                UNION
                SELECT * 
                FROM recuperatorio1
                UNION
                SELECT * 
                FROM recuperatorio2
              """

desafio_03 = dd.sql(consultaSQL).df()
