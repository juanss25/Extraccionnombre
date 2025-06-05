import streamlit as st
import os
import datetime

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
        Esta aplicación te permite listar todos los archivos y subcarpetas dentro de una ruta específica
        y guardar la lista en un archivo de texto.
    """)

    folder_path = st.text_input("Ingresa la ruta de la carpeta:", value="")

    if st.button("Analizar Carpeta"):
        if folder_path:
            if os.path.exists(folder_path):
                if os.path.isdir(folder_path):
                    st.write(f"Analizando la carpeta: `{folder_path}`")
                    contents = get_folder_contents(folder_path)

                    if contents:
                        st.subheader("Contenido Encontrado:")
                        for item in contents[:10]: # Mostrar solo los primeros 10 para evitar sobrecarga visual
                            st.write(f"- {item}")
                        if len(contents) > 10:
                            st.write(f"...y {len(contents) - 10} elementos más.")

                        # Generar el nombre del archivo de salida
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"lista_archivos_{timestamp}.txt"

                        # Crear el contenido del archivo de texto
                        output_content = "\n".join(contents)

                        st.download_button(
                            label="Descargar Lista de Archivos",
                            data=output_content,
                            file_name=output_filename,
                            mime="text/plain"
                        )
                        st.success(f"La lista de archivos se ha generado correctamente en '{output_filename}' y está lista para descargar.")
                    else:
                        st.warning("La carpeta seleccionada está vacía o no contiene elementos.")
                else:
                    st.error("La ruta proporcionada no es una carpeta. Por favor, ingresa una ruta de carpeta válida.")
            else:
                st.error("La ruta proporcionada no existe. Por favor, verifica la ruta e intenta de nuevo.")
        else:
            st.warning("Por favor, ingresa una ruta de carpeta antes de analizar.")

    st.markdown("---")
    st.markdown("Desarrollado con ❤️ y Streamlit")

if __name__ == "__main__":
    main()
