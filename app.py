import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import QTable
import requests
import os

# URLs de los archivos en GitHub
URL_FITS = "https://cloud.iaa.es/index.php/s/KJpbwFtLAxxfD6b"
URL_NPY = "https://cloud.iaa.es/index.php/s/AjY3Jka936m5Cyx"

# Descargar archivos si no existen
fits_path = "input_file.fits"
npy_path = "cube_batchfile.npy"

if not os.path.exists(fits_path):
    with open(fits_path, "wb") as f:
        f.write(requests.get(URL_FITS).content)

if not os.path.exists(npy_path):
    with open(npy_path, "wb") as f:
        f.write(requests.get(URL_NPY).content)

# Leer archivos automáticamente
selected = QTable.read(fits_path)
cubos_imagenes = np.load(npy_path)

# Interfaz en Streamlit
st.title("Visualización Interactiva de Datos FITS y NPY")

# Seleccionar fila
fila_index = st.slider("Selecciona una fila", 0, len(selected)-1, 80)
st.write("Datos de la fila seleccionada:")
st.write(selected[fila_index])

# Normalizar los datos
xdata = np.arange(57)
max_flux = np.nanmax(selected['FLUX_APER_COR_3_0'][fila_index])
ydata = selected['FLUX_APER_COR_3_0'][fila_index] / max_flux if max_flux else np.zeros_like(selected['FLUX_APER_COR_3_0'][fila_index])

max_cube = np.nanmax(cubos_imagenes[fila_index])
cubo_imagenes_fila = cubos_imagenes[fila_index] / max_cube if max_cube else cubos_imagenes_fila[fila_index]

# Crear la figura con dos subgráficos en una fila
fig, (ax, ax_imagen) = plt.subplots(1, 2, figsize=(12, 6))

# Graficar flujo
sc = ax.scatter(xdata, ydata)
ax.plot(xdata, ydata)
ax.set_xlabel("Filtro")
ax.set_ylabel("Flujo")

# Mostrar la imagen inicial
selected_filter = st.slider("Selecciona un filtro", 0, 56, 0)
ax_imagen.imshow(cubo_imagenes_fila[selected_filter], cmap='viridis')
ax_imagen.axis('off')

# Añadir un punto rojo en el filtro seleccionado
ax.scatter([selected_filter], [ydata[selected_filter]], color='red', s=100, label='Filtro seleccionado')
ax.legend()

# Mostrar gráficos en Streamlit
st.pyplot(fig)
