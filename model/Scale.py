import cv2
import os
import numpy as np

class reScale():

    def __init__(self,image):
        self.image = image
    
    def changeScale(self):
       
        try:
            # Convertir BytesIO a array NumPy con OpenCV
            self.image.seek(0)  # Reinicia el cursor al inicio del "archivo" (BytesIO)
            image_np = cv2.imdecode(np.frombuffer(self.image.read(), np.uint8),cv2.IMREAD_COLOR ) # o cv2.IMREAD_GRAYSCALE para escala de grises)

        
            img = cv2.cvtColor(image_np,cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))  
            imagenes = np.array(img)  

            return imagenes
           
        except Exception as e:
            return (f"Error al procesar la imagen clase Scale: {str(e)}")
        

