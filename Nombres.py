import streamlit as st
from pathlib import Path

st.title("Listado de archivos de una carpeta")

# Entrada de la ruta de la carpeta
folder_path = st.text_input("Introduce la ruta absoluta de la carpeta:")

def listar_archivos_recursivos(path_str):
    """Devuelve una lista de rutas relativas de todos los archivos en la carpeta y subcarpetas."""
    path = Path(path_str)
    if not path.exists() or not path.is_dir():
        return None, "La ruta no existe o no es una carpeta válida."
    archivos = [str(f.relative_to(path)) for f in path.rglob('*') if f.is_file()]
    return archivos, None

if folder_path:
    archivos, error = listar_archivos_recursivos(folder_path)
    if error:
        st.error(error)
    else:
        if archivos:
            st.success(f"Se encontraron {len(archivos)} archivos.")
            st.write(archivos)
            
            # Guardar en un archivo txt
            nombre_archivo = "lista_archivos.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                for archivo in archivos:
                    f.write(archivo + "\n")
            
            # Permitir descarga del archivo txt
            with open(nombre_archivo, "rb") as f:
                st.download_button(
                    label="Descargar lista como TXT",
                    data=f,
                    file_name=nombre_archivo,
                    mime="text/plain"
                )
        else:
            st.info("La carpeta no contiene archivos.")
else:
    st.info("Introduce una ruta para comenzar.")

