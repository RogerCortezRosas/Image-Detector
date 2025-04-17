from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import shutil
import os
from Modelo import model
import io


app = FastAPI()

UPLOAD_FOLDER = "imagenes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Montar la carpeta "imagenes" como estática (para acceder a las imágenes)
app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Verificar que el archivo sea una imagen JPG o PNG
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG o PNG")
    
    try:
       # Define la ruta donde se almacenará el archivo
        file_path = f"imagenes/{file.filename}"
        file_bytes = await file.read()
        file_content = io.BytesIO(file_bytes)
        
        # Guarda la imagen en el disco
        with open(file_path, "wb") as buffer:
           shutil.copyfileobj(file_content, buffer)

        obj_model = model(file_content)
        prediction = obj_model.prediction()
        
        return JSONResponse(content={"Resultado": prediction})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

#ejecutar 
#uvicorn main:app --reload
#main: Es el nombre del archivo (sin la extensión .py).

#app: Es el nombre de la variable que contiene la instancia de FastAPI en tu archivo main.py.
#si no esta en raiz entonces uvicorn model.api:app --reload