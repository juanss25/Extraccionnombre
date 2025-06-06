import streamlit as st
import os
import datetime
import zipfile # Para manejar archivos ZIP
import shutil # Para limpiar directorios

def get_folder_contents(folder_path):
    """
    Obtiene la lista de todos los archivos y subcarpetas dentro de una ruta dada.
    """
    contents = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            # Añadir subcarpetas
            for d in dirs:
                contents.append(os.path.join(root, d))
            # Añadir archivos
            for f in files:
                contents.append(os.path.join(root, f))
    return contents

def main():
    st.set_page_config(page_title="Extractor de Nombres de Carpeta", layout="centered")

    st.title("📂 Extractor de Nombres de Archivos y Carpetas")
    st.markdown("""
        Esta aplicación te permite listar todos los archivos y subcarpetas.
        Puedes seleccionar una carpeta local o subir un archivo ZIP con la carpeta.
    """)

    # Opción 1: Ingresar ruta de carpeta local (solo si se ejecuta el .exe)
    if not st.runtime.is_hello_app(): # Solo mostrar esta opción si no está en Streamlit Cloud
        st.subheader("Opción 1: Analizar una carpeta local")
        local_folder_path = st.text_input("Ingresa la ruta de la carpeta local:", value="")
        if st.button("Analizar Carpeta Local"):
            if local_folder_path:
                if os.path.exists(local_folder_path) and os.path.isdir(local_folder_path):
                    st.write(f"Analizando la carpeta local: `{local_folder_path}`")
                    contents = get_folder_contents(local_folder_path)
                    if contents:
                        # ... (código para mostrar y descargar, similar al anterior) ...
                        st.subheader("Contenido Encontrado (Local):")
                        for item in contents[:10]:
                            st.write(f"- {item}")
                        if len(contents) > 10:
                            st.write(f"...y {len(contents) - 10} elementos más.")

                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"lista_archivos_local_{timestamp}.txt"
                        output_content = "\n".join(contents)
                        st.download_button(
                            label="Descargar Lista de Archivos (Local)",
                            data=output_content,
                            file_name=output_filename,
                            mime="text/plain"
                        )
                        st.success(f"La lista de archivos se ha generado correctamente en '{output_filename}' y está lista para descargar.")
                    else:
                        st.warning("La carpeta local seleccionada está vacía o no contiene elementos.")
                else:
                    st.error("La ruta local proporcionada no es una carpeta válida o no existe.")
            else:
                st.warning("Por favor, ingresa una ruta de carpeta local.")
        st.markdown("---")

    # Opción 2: Subir un archivo ZIP
    st.subheader("Opción 2: Subir una carpeta comprimida (ZIP)")
    uploaded_zip = st.file_uploader("Sube un archivo ZIP de la carpeta a analizar:", type=["zip"])

    if uploaded_zip is not None:
        # Crear un directorio temporal para descomprimir
        temp_dir = "temp_uploaded_folder_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            st.success(f"Archivo ZIP '{uploaded_zip.name}' subido y descomprimido en '{temp_dir}'.")

            # Ahora, analiza el contenido del directorio temporal
            contents = get_folder_contents(temp_dir)

            if contents:
                st.subheader("Contenido Encontrado (del ZIP):")
                # Mostrar solo los primeros 10 elementos para no saturar la UI
                for item in contents[:10]:
                    # Mostrar la ruta relativa dentro del ZIP para mayor claridad
                    st.write(f"- {os.path.relpath(item, temp_dir)}")
                if len(contents) > 10:
                    st.write(f"...y {len(contents) - 10} elementos más.")

                # Preparar para la descarga
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"lista_archivos_{timestamp}_del_zip.txt"
                
                # Para el archivo de salida, es mejor que las rutas sean relativas al ZIP original
                relative_contents = [os.path.relpath(item, temp_dir) for item in contents]
                output_content = "\n".join(relative_contents)

                st.download_button(
                    label="Descargar Lista de Archivos (del ZIP)",
                    data=output_content,
                    file_name=output_filename,
                    mime="text/plain"
                )
                st.success(f"La lista de archivos del ZIP se ha generado correctamente en '{output_filename}' y está lista para descargar.")
            else:
                st.warning("El archivo ZIP está vacío o no contiene elementos reconocibles.")

        except zipfile.BadZipFile:
            st.error("El archivo subido no es un archivo ZIP válido.")
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo ZIP: {e}")
        finally:
            # Limpiar el directorio temporal después de procesar
            if os.path.exists(temp_dir):
                st.info(f"Limpiando directorio temporal: {temp_dir}")
                shutil.rmtree(temp_dir)

    st.markdown("---")


if __name__ == "__main__":
    main()
