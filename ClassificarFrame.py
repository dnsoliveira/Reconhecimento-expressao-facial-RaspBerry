import numpy as np
import cv2 as cv
from ConsultarCNN import *

class ClassificarFrame(object):
    def __init__(self):
        self.azul=(255,0,0)
        self.verde = (0,255,0)
        self.vermelho = (0,0,255)
        self.rosa = (255,0,255)
        self.face_cc = cv.CascadeClassifier('haars/haarcascade_frontalface_default.xml')#('haars/haarcascade_frontalface_alt.xml')#
        self.olhos_oculos_cc = cv.CascadeClassifier('haars/haarcascade_eye_tree_eyeglasses.xml')
        self.olho_esquerdo_cc = cv.CascadeClassifier('haars/haarcascade_lefteye_2splits.xml')
        self.olho_direito_cc = cv.CascadeClassifier('haars/haarcascade_righteye_2splits.xml')
        self.sorriso_cc = cv.CascadeClassifier('haars/haarcascade_smile.xml')
        self.consultarCNN = ConsultarCNN() 
        self.modeloOlhos = self.consultarCNN.carregarModelo('modelos/modelOlho')
        self.modeloBoca = self.consultarCNN.carregarModelo('modelos/modelBoca')
        self.resultado = 'idk'
        #self.i = 3
        
    def carregarImg(self,img):
        #self.img = cv.imread(img)
        #print (type(self.img))
        self.img = img #descomentar para utilizar camera
        #self.img = cv.resize(self.img, (0, 0), fx=0.7, fy=0.7)
        #self.img = cv.flip(self.img,1)
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        #self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)

    def detectarFace(self):
        #Detecta faces na imagem
        self.faces = self.face_cc.detectMultiScale(
            self.img_gray,
            scaleFactor=1.2,
            minNeighbors=5
            #minSize=(50, 50)
        )
        #print (type(self.faces))

    def varrerImg(self):
        for (x,y,w,h) in self.faces:
            cv.rectangle(self.img,(x,y),(x+w,y+h),self.azul,2)
            self.face_gray = self.img_gray[y:y+h, x:x+w]
            self.face_cor = self.img[y:y+h, x:x+w]
            self.olhosAbertos = self.detectarOlho(self.face_gray,self.olhos_oculos_cc)
            self.boca = self.detectarBoca(self.face_gray, self.sorriso_cc)
            self.marcarBoca(self.face_cor, self.face_gray,self.boca,self.rosa,True)
            if len(self.olhosAbertos) == 2:
                self.marcarOlho(self.face_cor, self.face_gray,self.olhosAbertos,self.verde,True)
                #print ('A')
                self.resultadoOlho = 'A'
            else:
                #Separa a face em lado esquerdo
                self.faceEsq = self.img[y:y+h, x+int(w/2):x+w]
                self.faceEsq_gray = self.img_gray[y:y+h, x+int(w/2):x+w]
                #Separa a face em lado direito
                self.faceDir = self.img[y:y+h, x:x+int(w/2)]
                self.faceDir_gray = self.img_gray[y:y+h, x:x+int(w/2)]
                self.olhosSeparados()


    def marcarOlho(self,face,face_gray,olho,cor,consultar):
        for (x,y,w,h) in olho:
            cv.rectangle(face,(x,y),(x+w,y+h),cor,2)
            if consultar:
                olho_gray = face_gray[y:y+h, x:x+w]
                resultado = self.consultarCNN.predict(olho_gray,self.modeloOlhos,True)
                if resultado == 'F':
                    #print(resultado)
                    self.resultadoOlho = 'F'
                cv.putText(face, resultado, (x, y), cv.FONT_HERSHEY_SIMPLEX,0.75, cor, 2)

    def marcarBoca(self,face,face_gray,boca,cor,consultar):
        for (x,y,w,h) in boca:
            cv.rectangle(face,(x,y),(x+w,y+h),cor,2)
            if consultar:
                boca_gray = face_gray[y:y+h, x:x+w]
                resultado = self.consultarCNN.predict(boca_gray,self.modeloBoca,False)
                if resultado == 'S':
                    #print(resultado)
                    self.resultadoBoca = 'S'
                elif resultado == 'B':
                    self.resultadoBoca = 'B'
                cv.putText(face, resultado, (x, y), cv.FONT_HERSHEY_SIMPLEX,0.75, cor, 2)


    def olhosSeparados(self):
        #detecta olho esquerdo
        self.olhoEsq = self.detectarOlho(self.faceEsq_gray,self.olho_esquerdo_cc)
        #detecta olho direito
        self.olhoDir = self.detectarOlho(self.faceDir_gray,self.olho_direito_cc)
        self.marcarOlho(self.faceEsq,self.faceEsq_gray,self.olhoEsq,self.vermelho,True)
        #self.ConsultarIA(self.faceEsq,self.olhoEsq)
        self.marcarOlho(self.faceDir,self.faceDir_gray,self.olhoDir,self.vermelho,True)
        #self.ConsultarIA(self.faceDir,self.olhoDir)

    def detectarOlho(self,face_gray,cc):
        #Detecta olhos na face
        olhos = cc.detectMultiScale(
            face_gray,
            scaleFactor=1.1,
            minNeighbors=5
        )
        return olhos

    def detectarBoca(self,face_gray,cc):
        #Detecta olhos na face
        boca = cc.detectMultiScale(
            face_gray,
            scaleFactor=1.2, #1.2
            minNeighbors=12,
            minSize=(20, 30) #20,30
        )
        return boca

    def ConsultarIA(self,olho,face):
        resultado = self.consultarCNN.predict(olho,self.modeloOlhos)
        print(resultado)
        #cv.putText(face, resultado, (x, y), cv.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

    def classifica(self):
        #self.i = self.i+1
        self.resultadoOlho = 'idk'
        self.resultadoBoca = 'idk'
        self.detectarFace()
        self.varrerImg() 
        #cv.imwrite('fotos/analisadasrgb/%i_%i.jpg' %(self.i,self.i), self.img_gray)
        return self.img, self.resultadoOlho, self.resultadoBoca


if __name__ == '__main__':
    #imagens = ('two_people.jpg','red6.jpg','red3.jpg','7.jpeg','renan3.jpg', '10.jpg', 'dns.jpg', 'dns1.jpg',
    #'1.jpg', 'red.jpg', 'red5.jpg', 'red10.jpg', '2.jpg', '12.jpg', 'anne.jpg', 'emma.jpg', 'miley.jpg', 'miley2.jpg')
    #imagens = ('d1.jpg','d2.jpg','d3.jpg','d4.jpg','d5.jpg','d6.jpg')
    #imagens = ('dn0.jpg','dn1.jpg','dn2.jpg','dn3.jpg','dn4.jpg','dn5.jpg','dn6.jpg','dn7.jpg','dn8.jpg','dn9.jpg','dn10.jpg',
    #'dn11.jpg','dn12.jpg','dn13.jpg','dn14.jpg','dn15.jpg','dn16.jpg','dn17.jpg','dn18.jpg','dn19.jpg')#'dn20.jpg','dn21.jpg','dn22.jpg','dn23.jpg')
    #imagens = ('dn1.jpg','dn2.jpg','dn3.jpg','dn4.jpg','dn5.jpg','dn6.jpg','dn7.jpg','dn8.jpg','dn9.jpg','dn10.jpg', 'dn11.jpg')
    
    
    classificarOlhos = ClassificarFrame()
    """
    for i in imagens:
        classificarOlhos.carregarImg('fotos/%s' %i)
        img, resultado = classificarOlhos.classifica()
        cv.imwrite('fotos/testola/%s' %i, img)
    """

    for i in range(1,9):
        classificarOlhos.carregarImg('fotos/sorrisos/teste (%i).jpg' %i)
        img, resultadoOlho, resultadoBoca = classificarOlhos.classifica()
        cv.imwrite('fotos/analisadasboca2/%ia.jpg' %i, img)
        #img = cv.imshow('teste',img)
        #cv.waitKey(0)
        #cv.destroyAllWindows()

