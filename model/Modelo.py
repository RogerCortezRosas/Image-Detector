import tensorflow as tf
from tensorflow.keras.layers import  Dropout , Flatten , Dense ,GlobalAveragePooling2D,Lambda,Input
from tensorflow.keras import models , optimizers , regularizers
from tensorflow.keras.applications.resnet import ResNet50, preprocess_input
from PIL import Image
from tensorflow.keras.models import Sequential
import numpy as np
#import nbimporter
#from Rescale import reScale
from Scale import reScale

class model():

    def __init__(self,image):
        self.image = image

    def creationModel(self):
        # Creation of a instance of pre-train model ResNet50
        ResNet50_conv_base  = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        #Do not retrain layers that are already trained
        for layer in ResNet50_conv_base.layers:
            layer.trainable = False

        # CNN Model
        model = Sequential([

        # Input Layer
        Input(shape=(224,224,3)),

        # ResNet Preprocessing (applied during training & inference)
        Lambda(preprocess_input),

        ResNet50_conv_base,    
        
        GlobalAveragePooling2D(),
            
        Flatten(),

        Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        Dropout(0.3),
        Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),

        # The final `Dense` layer with the number of classes.
        Dense(1, activation ='sigmoid')
        ])

        return model
    
    def loadModel(self):
        # Optimizer
        opt = optimizers.AdamW(learning_rate=0.0001, weight_decay=1e-5)

        #Copy architecture of the model
        model_best = self.creationModel()

        #Charge the best weigths to model_best
        model_best.load_weights('weights/Best_Model.keras')

        #Compile the model
        model_best.compile(optimizer=opt,loss='binary_crossentropy',metrics=['accuracy'])

        return model_best
    
    def prediction(self):

        try:
            model_best = self.loadModel() #charge the best weight and architercture
            obj_imagen = reScale(self.image) # instance of the class reScale
            imagen = obj_imagen.changeScale() # call the function and return the rescale image
            imagen = tf.expand_dims(imagen, axis=0) # Agregar dimensión de batch -> (1, 224, 224, 3)
            y_predict = model_best.predict(imagen)# image prediction
            y_predict = np.where(y_predict>0.5,1,0)# 1-> AI , 0->Human Image

            y_predict = int(y_predict[0][0])

            if y_predict == 0:
                return 'La imagen fue hecha por humanos'            
            else:
                return 'La imagen fue hecha por inteligencia artificial'
            
        except Exception as e:
            
                return f"Error al realizar prediccion: {str(e)}"

        


