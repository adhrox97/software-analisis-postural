# coding=utf-8
#include <QString>
"""
Created on Fri Nov 27 23:30:19 2020

@author: juan david, Adrian David
"""
import sys
import datetime
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QCompleter,QButtonGroup, QTableView,QLineEdit, \
    QTableWidget, QTableWidgetItem
from PyQt5.QtSql import *
from PyQt5 import uic,QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate,Qt,pyqtSlot, QObject
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
import numpy as np
import datetime
import pygame
from pykinect import nui
from pykinect.nui import JointId
from Funciones import AjustarImagen,Capturar,mCurvas,Modelo3D,mostrar3D,screenModelo3D,mCurvasHistorial
from Base_Datos import (ver_cuenta, ob_clientes, dato_cliente, insertarDatos, ob_CYT, eliminarDatos,
update_usuario,G_Datos,ult_paciente,hist_paciente,fechas_paciente)
import cv2
import qimage2ndarray
import math
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

bienvenida = resumen = nuevo = curv = 0
admins = borrar = historial = modelo3d = 1  
pantalla1 = editar = nRegistro = 2

nombre=usuario=clave=tb=""
edad=0

captura = np.zeros((240,320))
captura2 = np.zeros((240,320))
curvas = np.zeros((240,320))

# angulos = np.zeros((11,3))
n = 0
partesCuerpo = [4,8,3,2,0,12,13,14,16,17,18]
kinect = nui.Runtime() 

class Ventana(QMainWindow):
#---------------------------------------------------------------------------------------# Inicio de ventana 
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.MainWindow1=loadUi("mainWindow.ui",self)
        
        fecha = datetime.datetime.now().date()
        fecha = "Fecha : " + str(fecha)
        
        self.labelFecha0.setText(fecha)
        self.labelFecha1.setText(fecha)
        self.labelFecha2.setText(fecha)
        self.labelFecha3.setText(fecha)
        self.labelFecha4.setText(fecha)
        
        self.h1=""
        self.h2=""
        self.tabla=""
        
        self.screenShot = np.zeros((240,320))
        self.ajustarFinal = np.empty((320,240,4),np.uint8)
        self.ajustarFinalVisual = np.empty((320,240,4),np.uint8)
        self.video1 = np.empty((480,640,4),np.uint8)
#---------------------------------------------------------------------------------------#
        self.timer = QtCore.QTimer();
        self.timer.timeout.connect(self.Update)
        self.timer.start(40);
    def Update(self):
        global n
        global captura
        DEPTH_WINSIZE = 320,240
        tmp_s = pygame.Surface(DEPTH_WINSIZE, 0, 16)
        
        def depth_frame_ready(frame):
            # npArr2d = np.zeros((240,320))
            frame.image.copy_bits(tmp_s._pixels_address)
            arr2dVisual = (pygame.surfarray.pixels2d(tmp_s) >> 7) & 255
            arr2d = (pygame.surfarray.pixels2d(tmp_s)>>3) 
            #RotarYtrasladar
            rotaVisual = np.transpose(arr2dVisual)  
            rota = np.transpose(arr2d) 
            # self.ajustarFinal = AjustarImagen(arr2d)
            self.ajustarFinalVisual = AjustarImagen(rotaVisual)
            self.screenShot = rota
        captura = self.screenShot

        def video_frame_ready(frame):
            
            frame.image.copy_bits(self.video1.ctypes.data)
                  
        if n == 0:           


            kinect.video_frame_ready += video_frame_ready  
            kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)

            #nui.ImageResolution.Resolution640x480 <-- camara rgb

            n = 1
        else:
            #convertir formato
            
            #-------------------------------------------Rastreo--------------------------------------------#
            #frame=cv2.cvtColor(self.ajustarFinalVisual,cv2.COLOR_BGR2RGB)
            #frame=cv2.cvtColor(self.video1,cv2.COLOR_BGR2RGB)
            #frame=cv2.cvtColor(self.video1,cv2.COLOR_BGR2HSV)

            #copy_frame = self.video1.copy()


            def nothing(x):

                pass

            # named ites for easy reference
            barsWindow = 'Bars'
            hl = 'H Low'
            hh = 'H High'
            sl = 'S Low'
            sh = 'S High'
            vl = 'V Low'
            vh = 'V High'

            # set up for video capture on camera 0
            #cap = cv.VideoCapture(0)

            # create window for the slidebars
            cv2.namedWindow(barsWindow, flags = cv2.WINDOW_AUTOSIZE)

            # create the sliders
            cv2.createTrackbar(hl, barsWindow, 0, 179, nothing)
            cv2.createTrackbar(hh, barsWindow, 0, 179, nothing)
            cv2.createTrackbar(sl, barsWindow, 0, 255, nothing)
            cv2.createTrackbar(sh, barsWindow, 0, 255, nothing)
            cv2.createTrackbar(vl, barsWindow, 0, 255, nothing)
            cv2.createTrackbar(vh, barsWindow, 0, 255, nothing)

            # set initial values for sliders
            cv2.setTrackbarPos(hl, barsWindow, 0)
            cv2.setTrackbarPos(hh, barsWindow, 179)
            cv2.setTrackbarPos(sl, barsWindow, 0)
            cv2.setTrackbarPos(sh, barsWindow, 255)
            cv2.setTrackbarPos(vl, barsWindow, 0)
            cv2.setTrackbarPos(vh, barsWindow, 255)

            while(1):

                frame = self.video1.copy()
                frame = cv2.GaussianBlur(frame, (5, 5), 0)
                
                # convert to HSV from BGR
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # read trackbar positions for all
                hul = cv2.getTrackbarPos(hl, barsWindow)
                huh = cv2.getTrackbarPos(hh, barsWindow)
                sal = cv2.getTrackbarPos(sl, barsWindow)
                sah = cv2.getTrackbarPos(sh, barsWindow)
                val = cv2.getTrackbarPos(vl, barsWindow)
                vah = cv2.getTrackbarPos(vh, barsWindow)

                # make array for final values
                HSVLOW = np.array([hul, sal, val])
                HSVHIGH = np.array([huh, sah, vah])

                # apply the range on a mask
                mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
                maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

                # display the camera and masked images
                cv2.imshow('Masked', maskedFrame)
                cv2.imshow('Camera', frame)

                # check for q to quit program with 5ms delay
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break


            cap.release()

            cv2.destroyAllWindows()            

app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()