# Trabajo práctico 02

## Requisitos

Este código requiere Python y las siguientes librerías:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `sklearn`

Podes instalarlas usando:
```sh
pip install pandas numpy matplotlib seaborn scikit-learn
```

Se incluyeron los módulos matplotlib.colors y matplotlib.cm no vistos en clase, con el único objetivo de generar un label del degradé en los colores del gráfico titulado "20 píxeles de mayor variación entre 0 y 1". 

## Estructura del Proyecto

- **Carga de datos**: Se carga el dataset a un dataframe.
- **Análisis exploratorio**: Se observan algunos dígitos en particular y se generan gráficos.
- **Clasificación binaria**: Se entrenan diferentes modelos de KNN sobre los datos en su versión binaria.
- **Clasificación multiclase**: Se entrenan diferentes árboles de decisión sobre el dataset sin un conjunto held-out, que se separa antes de entrenarlos.

## Descripción
Este proyecto busca entrenar principalmente dos modelos: un modelo de **K-Nearest Neighbors (KNN)** para clasificar ceros y unos y un modelo de **Árboles de decisión**  para clasificar todo tipo de dígitos. Esto se hace sobre el dataset **MNIST con niebla** (`mnist_c_fog_tp.csv`).

## Aviso
Al entrenarse tantos modelos sobre tantos datos hay ciertos ciclos que tardan mucho en ejecutarse. Estos son los ciclos para decidir los modelos definitivos y tienen un comentario avisando que son muy costosos.