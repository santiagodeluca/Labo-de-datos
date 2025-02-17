import pandas as pd
import duckdb as dd
import numpy as np
def establecimiento_educativo():
    ee = pd.read_excel("/home/fede/Escritorio/TP_LaboDatos/2022_padron_oficial_establecimientos_educativos.xlsx",skiprows=5)

    cueanexo = ee["Unnamed: 1"]
    jardin_1 = ee["Común"]
    jardin_2 = ee["Unnamed: 21"]
    primaria_1 = ee["Unnamed: 22"]
    secu_1= ee["Unnamed: 23"]
    secu_2= ee["Unnamed: 24"]
    secu_3= ee["Unnamed: 25"]
    secu_4= ee["Unnamed: 26"]
    codigo_depto = ee["Unnamed: 9"]

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

    encabezado_establecimiento_educativo = [cueanexo[0],"ID_Depto","Jardin","Primaria","Secundaria"]
    df_establecimiento_educativo = pd.DataFrame(establecimiento_educativo_data, columns=encabezado_establecimiento_educativo)
    return(df_establecimiento_educativo)

def centros_culturales():
    cc = pd.read_csv("/home/fede/Escritorio/TP_LaboDatos/centros_culturales.csv")
    mail = cc["Mail "]
    capacidad = cc["Capacidad"]
    nombre = cc["Nombre"]
    
    centro_cultural_data = []

    for i in range(len(nombre)):
        linea = []
        linea.append(i)
        linea.append(nombre[i])
        if np.isnan(capacidad[i]) or capacidad[i]==0:
            linea.append(np.nan)
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
        centro_cultural_data.append(linea)
    encabezado = ["Id","Nombre","Capacidad","Mail"]
    df_cc = pd.DataFrame(centro_cultural_data, columns = encabezado)
    return(df_cc)

#        distintos nulls 147,162, 213, 317, 319, 324,325,327,328,332,333,334,338,343,348,351,360, 369...372, 
#        dos mails 169, 175, 183, 203, 246, 252, 277, 287, 321
#        no valida 373
#        \n 942