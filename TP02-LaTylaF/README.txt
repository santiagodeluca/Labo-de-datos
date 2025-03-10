# Trabajo practico N2

## Requisitos

Este código requiere Python y las siguientes librerías:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `sklearn`

Puedes instalarlas usando:
```sh
pip install pandas numpy matplotlib seaborn scikit-learn
```

Se incluyeron los módulos matplotlib.colors y matplotlib.cm no vistos en clase, con el único objetivo de generar un label del degradé en los colores del gráfico titulado "20 píxeles de mayor variación entre 0 y 1". 

## Estructura del Proyecto

- **Carga de datos**: Se carga el dataset y se filtran los dígitos 0 y 1.
- **Preprocesamiento**: Se dividen los datos en conjuntos de entrenamiento y prueba.
- **Entrenamiento con KNN**: Se entrena un modelo KNN sobre los datos.
- **Evaluación de importancia de píxeles**: Se eliminan píxeles uno por uno y se mide el impacto en la precisión.


## Descripción
Este proyecto implementa un modelo de **K-Nearest Neighbors (KNN)** para analizar la importancia de los píxeles en la clasificación de dígitos 0 y 1 en el dataset **MNIST con niebla** (`mnist_c_fog_tp.csv`).

El objetivo principal es determinar cuáles son los píxeles más relevantes para la clasificación, utilizando la métrica de importancia basada en el impacto de la eliminación de cada píxel en la precisión del modelo.
