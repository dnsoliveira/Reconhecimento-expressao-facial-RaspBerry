from __future__ import print_function
import cv2
import numpy as np
from ClassificarFrame import *
from imutils.video import VideoStream
import time
import imutils
import RPi.GPIO as gpio

def Frente():
    gpio.output(11, gpio.LOW)
    gpio.output(12, gpio.HIGH)
    
def Tras():
    gpio.output(12, gpio.LOW)
    gpio.output(11, gpio.HIGH)
    
def Parar():
    gpio.output(11, gpio.LOW)
    gpio.output(12, gpio.LOW)

# Playing video from file:
#cap = cv2.VideoCapture('video45.mp4')
# Capturing video from webcam:
cap = VideoStream(usePiCamera=True).start() #, resolution = (480,360)
classificarFrame = ClassificarFrame()
olhosDetectados = 0
zeraOlho = 0
sorrisosDetectados = 0
zeraBoca = 0
acionadoFrente = False
acionadoTras = False
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT)
Parar()
time.sleep(2.0)


currentFrame = 0
while(True):
    # Capture frame-by-frame
    frame = cap.read()
    #frame = imutils.resize(frame, width=400)
    classificarFrame.carregarImg(frame)

    frame, resultadoOlho, resultadoBoca = classificarFrame.classifica()

    if resultadoOlho == 'F':
        olhosDetectados += 1
        zeraOlho = 0
        print ("Sequencia de olhos fechados: %i" %olhosDetectados)

    elif resultadoOlho =='A' or zeraOlho > 5:
        olhosDetectados = 0
        
    else:
        zeraOlho += 1
        
    if resultadoBoca == 'S':
        sorrisosDetectados += 1
        zeraBoca = 0
        print ("Sequencia de Sorrisos: %i" %sorrisosDetectados)

    elif resultadoBoca =='B' or zeraBoca > 5:
        sorrisosDetectados = 0
        
    else:
        zeraBoca += 1

    if olhosDetectados > 10 and acionadoFrente == False:
        print ('Acionado Frente!')
        acionadoFrente = True
        acionadoTras = False
        Frente()
        olhosDetectados = 0

    if olhosDetectados > 10 and acionadoFrente == True:
        print ('Desacionado Frente!'),
        acionadoFrente = False
        acionadoTras = False
        Parar()
        olhosDetectados = 0
        
    
    if sorrisosDetectados > 10 and acionadoTras == False:
        print ('Acionado Tras!')
        acionadoTras = True
        acionadoFrente = False
        Tras()
        sorrisosDetectados = 0

    if sorrisosDetectados > 10 and acionadoTras == True:
        print ('Desacionado Tras!'),
        acionadoTras = False
        acionadoFrente = False
        Parar()
        sorrisosDetectados = 0

    # Display the resulting frame
    cv2.imshow('Frames',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
Parar()
cv2.destroyAllWindows()
cap.stop()
gpio.cleanup()