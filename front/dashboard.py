import streamlit as st
from PIL import Image
import requests
import os

# URL de la API FastAPI
API_URL = "http://backend:8000/upload/"

# Obtener la ruta a la carpeta 'imagenes'
base_dir = os.path.dirname(os.path.abspath(__file__))  # directorio de api.py
imagenes_dir = os.path.join(base_dir, '..', 'model', 'imagenes')


# Asegurarse de que la carpeta 'imagenes' exista
if not os.path.exists(imagenes_dir):
    os.makedirs(imagenes_dir)

# Título de la aplicación
st.title("Ia images vs Humans images")

#Insertar imagen

st.image("IAvsHumans.png",caption="imagen" )
# Cargar la imagen
uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Abrir la imagen con PIL
    image = Image.open(uploaded_file)
    
    # Mostrar la imagen
    st.image(image, caption="Imagen subida")

     # Obtener el nombre del archivo
    file_name = uploaded_file.name

      # Guardar la imagen en la carpeta 'imagenes'
    file_path = os.path.join(imagenes_dir, file_name)
    
    #Guardar la imagen
    #with open(file_path, "wb") as f:
     #   f.write(uploaded_file.getbuffer())

        # Leer el archivo subido y crear un diccionario para enviarlo a la API
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    # Llamar a api upload para predecir la imagen

    if st.button("Predecir"):
        response = requests.post(API_URL,files=files)


        # Verifica que la respuesta sea exitosa  (código 200)
        if response.status_code == 200:
            # Parsea la respuesta JSON a un diccionario de Python
            respuesta_json = response.json()
            
            # Accede al campo "Resultado" (que contiene "prediction")
            prediction = respuesta_json["Resultado"]
            st.markdown(prediction)
        else:
            st.markdown("Error en la solicitud:", response.status_code)
            st.markdown("Detalles:", response.text)  # Muestra el mensaje de error del servidor