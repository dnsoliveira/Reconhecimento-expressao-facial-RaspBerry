import os
from PIL import Image
import numpy as np

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator

from scipy.ndimage import imread
from scipy.misc import imresize, imsave

#self.tamanhoImg = 24

class ConsultarCNN(object):
    def __init__(self):
        self.tamanhoImg = 24

    def carregarModelo(self, modelo):
        json_modelo = open('%s.json' %modelo, 'r')
        modelo_carregado_json = json_modelo.read()
        json_modelo.close()
        modelo_carregado = model_from_json(modelo_carregado_json)
        # load weights into new model
        modelo_carregado.load_weights("%s.h5" %modelo)
        modelo_carregado.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return modelo_carregado

    def predict(self, img, model, olho):
        img = Image.fromarray(img)#.convert('L')
        img = imresize(img, (self.tamanhoImg,self.tamanhoImg)).astype('float32')
        img /= 255
        img = img.reshape(1,self.tamanhoImg,self.tamanhoImg,1)
        prediction = model.predict(img)
        if olho:
            if prediction < 0.16:
                prediction = 'F'
            elif prediction > 0.8:
                prediction = 'A'
            else:
                #print (prediction)
                prediction = 'idk'
        else:
            if prediction < 0.16:
                prediction = 'B'
            elif prediction > 0.8:
                prediction = 'S'
            else:
                #print (prediction)
                prediction = 'idk'
        return prediction

