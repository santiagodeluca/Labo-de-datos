import geopandas as gpd
import matplotlib.pyplot as plt

# Cargar el shapefile de Argentina (suponiendo que lo tengas)
# Asegúrate de tener el archivo .shp en el directorio adecuado.
argentina = gpd.read_file("ign_departamento.shp")

# Verificar la estructura del shapefile
print(argentina.head())