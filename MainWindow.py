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
update_usuario,G_Datos,ult_paciente,hist_paciente,fechas_paciente,conteo_paciente,hist_pacienteMax)
import cv2
import qimage2ndarray
import math
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

bienvenida = resumen = nuevo = curv = 0
admins = borrar = historial = modelo3d = 1  
pantalla1 = editar = historialmax = 2
nRegistro = 3

nombre=usuario=clave=tb=""
edad=0

captura = np.zeros((240,320))
captura2 = np.zeros((240,320))
curvas = np.zeros((240,320))

n = 0
partesCuerpo = [4,8,3,2,0,12,13,14,16,17,18]
kinect = nui.Runtime() 

def angulopuntos(colorx,colory):

    try:
            
        A=math.sqrt(math.fabs(colorx[1] - colorx[2])**2 + math.fabs(colory[1] - colory[2])**2)
        B=math.sqrt(math.fabs(colorx[0] - colorx[1])**2 + math.fabs(colory[0] - colory[1])**2)
        C=math.sqrt(math.fabs(colorx[2] - colorx[0])**2 + math.fabs(colory[2] - colory[0])**2)

        angulo1=np.rad2deg(np.arccos((B**2 + C**2 - A**2)/(2*B*C)))
        angulo2=np.rad2deg(np.arccos((A**2 + C**2 - B**2)/(2*C*A)))
        angulo3=np.rad2deg(np.arccos((A**2 + B**2 - C**2)/(2*A*B)))
        if math.isnan(angulo1) == True:
            angulo1 = 0
        elif math.isnan(angulo2) == True:
            angulo2 = 0
        elif math.isnan(angulo3) == True:
            angulo3 = 0
    
    except (TypeError,ZeroDivisionError):
        
        angulo1=angulo2=angulo3=0

    
    anguloF=max(angulo1,angulo2,angulo3)

    return anguloF

def distance(x1, y1, x2, y2):

    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

def angulo2p(color4_x,color4_y):

    hypotenuse = distance(color4_x[0], color4_y[0], color4_x[1], color4_y[1])
    horizontal = distance(color4_x[0], color4_y[0], color4_x[1], color4_y[0])
    vertical = distance(color4_x[1], color4_y[1], color4_x[1], color4_y[0])
    angulo = np.arcsin(vertical/hypotenuse)*180.0/math.pi

    return angulo

def find_color1(frame):
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([18, 173, 63]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([36, 255, 168])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx= [0,0,0]
    cy= [0,0,0]

    if len(cnts) > 0:
        maxcontour = sorted(cnts, key=cv2.contourArea)


        for i in range(1,4):

            M = cv2.moments(maxcontour[-i])

            if M['m00'] > 0 and cv2.contourArea(maxcontour[-i]) > 25:

                cx[i-1] = int(M['m10']/M['m00'])
                cy[i-1] = int(M['m01']/M['m00'])
              
            else:
                break

        if cx[2] > 0:
            return (cx, cy), True
        else:
            cx=[700,700,700]
            cy=[700,700,700]
            return (cx, cy), False #faraway point

    else:
        cx=[700,700,700]
        cy=[700,700,700]
        return (cx, cy), False #faraway point

def find_color2(frame):
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([100, 114, 0]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([134, 235, 111])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx= [0,0,0]
    cy= [0,0,0]

    if len(cnts) > 0:
        maxcontour = sorted(cnts, key=cv2.contourArea)
        for i in range(1,4):

            M = cv2.moments(maxcontour[-i])

            if M['m00'] > 0 and cv2.contourArea(maxcontour[-i]) > 25:

                cx[i-1] = int(M['m10']/M['m00'])
                cy[i-1] = int(M['m01']/M['m00'])

            else:
                break

        if cx[2] > 0:
            return (cx, cy), True
        else:
            cx=[700,700,700]
            cy=[700,700,700]
            return (cx, cy), False #faraway point
    else:
        cx=[700,700,700]
        cy=[700,700,700]
        return (cx, cy), False #faraway point

def find_color3(frame):
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([42, 89, 12]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([100, 189, 55])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx= [0,0,0]
    cy= [0,0,0]

    if len(cnts) > 0:
        maxcontour = sorted(cnts, key=cv2.contourArea)
        for i in range(1,4):

            M = cv2.moments(maxcontour[-i])

            if M['m00'] > 0 and cv2.contourArea(maxcontour[-i]) > 15:

                cx[i-1] = int(M['m10']/M['m00'])
                cy[i-1] = int(M['m01']/M['m00'])

            else:
                break

        if cx[2] > 0:
            return (cx, cy), True
        else:
            cx=[700,700,700]
            cy=[700,700,700]
            return (cx, cy), False #faraway point
    else:
        cx=[700,700,700]
        cy=[700,700,700]
        return (cx, cy), False #faraway point

def find_color4(frame):
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([152, 100, 0]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([179, 255, 164])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx= [0,0]
    cy= [0,0]

    if len(cnts) > 0:
        maxcontour = sorted(cnts, key=cv2.contourArea)
        for i in range(1,3):

            M = cv2.moments(maxcontour[-i])

            if M['m00'] > 0 and cv2.contourArea(maxcontour[-i]) > 15:

                cx[i-1] = int(M['m10']/M['m00'])
                cy[i-1] = int(M['m01']/M['m00'])

            else:
                break

        if cx[1] > 0:
            return (cx, cy), True
        else:
            cx=[700,700]
            cy=[700,700]
            return (cx, cy), False #faraway point
    else:
        cx=[700,700]
        cy=[700,700]
        return (cx, cy), False #faraway point


class Ventana(QMainWindow):
#---------------------------------------------------------------------------------------# Inicio de ventana 
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.MainWindow1=loadUi("mainWindow.ui",self)
        
        self.botonLogin.clicked.connect(self.EntrarPantalla1)
        self.botonLogout.clicked.connect(self.Salir2Bienvenida)
        self.botonLogout_2.clicked.connect(self.Salir2Bienvenida)
        
        self.botonBuscar.clicked.connect(self.Resumen)
        #self.botonAdmins.clicked.connect(self.EntrarAdmins)
        self.botonNuevoUsuario.clicked.connect(self.NuevoUsuario)
        self.botonBorraUsuario.clicked.connect(self.BorrarUsuario)
        self.botonEditarUsuario.clicked.connect(self.EditarUsuario)
        
        self.botonNuevo.clicked.connect(self.NuevoRegistro)
        self.botonNuevo.clicked.connect(self.Update)
        self.botonCaptura.clicked.connect(self.Captura)
        self.botonMostrarCurvas.clicked.connect(self.MostrarCurvas)
        self.botonCambiarCurvas.clicked.connect(self.Cambiar2Curvas)
        self.botonCambiar3d.clicked.connect(self.Cambiar2m3d)
        self.botonModelo3d.clicked.connect(self.mod3D)
        self.botonScreenModelo3d.clicked.connect(self.consModelo3D)
        self.botonScreenModelo3d.clicked.connect(self.Screen3D)
        self.botonCurvasHistorial.clicked.connect(self.CurvasHistorial)
        self.botonModeloHistorial.clicked.connect(self.mod3DHistorial)
        self.botoncambV.clicked.connect(self.videoC)
        self.botonAngulo.clicked.connect(self.CapAngulo)

        self.botonHistorial.clicked.connect(self.Historial)
        self.botonAtrasNuevoRegistro.clicked.connect(self.NuevoRegistroAtras)    #botonAtrasNuevoRegistro
        self.botonAtrasHistorial.clicked.connect(self.HistorialAtras)
        self.botonAtrasHistorialMax.clicked.connect(self.HistorialMaxAtras)
        self.botonBuscarFecha.clicked.connect(self.HistorialBuscarFecha)
        self.botonBuscarFecha_2.clicked.connect(self.HistorialBuscarFechaMax)
        self.botonMaxi.clicked.connect(self.HistorialAmp)
        
        self.botonAdminGuardar.clicked.connect(self.GuardarUsuario)
        self.botonEditarUsuario_3.clicked.connect(self.b_usuario)
        self.botonBuscar_3.clicked.connect(self.buscareditusuario)
        self.botonEditarUsuario_4.clicked.connect(self.edit_usuario)
        self.botonAdminGuardar_2.clicked.connect(self.GuardarDatos)
        
        self.radioBotonTerapeuta.toggled.connect(self.Seleccionado)
        self.radioBotonPaciente.toggled.connect(self.Seleccionado)
        
        self.radioBotonData.toggled.connect(self.S_historialdata)
        self.radioBotonData_2.toggled.connect(self.S_historialdata)
        self.radioBotonData_3.toggled.connect(self.S_historialdata)
        
        self.RadioGroup = QButtonGroup()
        self.RadioGroup.addButton(self.radioBotonTerapeuta)
        self.RadioGroup.addButton(self.radioBotonPaciente)
        
        self.RadioGroup2 = QButtonGroup()
        self.RadioGroup2.addButton(self.radioBotonData,0)
        self.RadioGroup2.addButton(self.radioBotonData_2,1)
        self.RadioGroup2.addButton(self.radioBotonData_3,2)
        
        self.resumenPaciente.setEnabled(False)
        self.nuevoRegistro.setEnabled(False)
        
        fecha = datetime.datetime.now().date()
        fecha = "Fecha : " + str(fecha)
        
        self.labelFecha0.setText(fecha)
        self.labelFecha1.setText(fecha)
        self.labelFecha2.setText(fecha)
        self.labelFecha3.setText(fecha)
        self.labelFecha4.setText(fecha)
        
        self.h1=""
        self.h2=""

        self.fechas=None
        
        self.screenShot = np.zeros((240,320))
        self.ajustarFinal = np.empty((320,240,4),np.uint8)
        self.ajustarFinalVisual = np.empty((320,240,4),np.uint8)
        self.video1 = np.empty((480,640,4),np.uint8)
        self.option=0
        self.indexH=0

        self.punto1x=self.punto1y=self.punto2x=self.punto2y=self.punto3x=self.punto3y=self.punto4x=self.punto4y= float(0)
        self.found_color1=self.found_color2=self.found_color3=self.found_color4=None
        self.angulo1=self.angulo2=self.angulo3=self.angulo4=float(0)

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
            
            frame.image.copy_bits(tmp_s._pixels_address)
            arr2dVisual = (pygame.surfarray.pixels2d(tmp_s) >> 7) & 255
            arr2d = (pygame.surfarray.pixels2d(tmp_s)>>3) 
            #RotarYtrasladar
            rotaVisual = np.transpose(arr2dVisual)  
            rota = np.transpose(arr2d) 
           
            self.ajustarFinalVisual = AjustarImagen(rotaVisual)
            self.screenShot = rota
        captura = self.screenShot

        def video_frame_ready(frame):
            
            frame.image.copy_bits(self.video1.ctypes.data)
                  
        if n == 0:

            if self.option == 0:
                
                kinect.depth_frame_ready += depth_frame_ready   
                kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)
            
            elif self.option == 1:
                
                kinect.video_frame_ready += video_frame_ready  
                kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
            
            n=1           

        else:

            if self.option == 0:
                
                frame=cv2.cvtColor(self.ajustarFinalVisual,cv2.COLOR_BGR2RGB)
                image = qimage2ndarray.array2qimage(frame)
                self.labelNuevoRegistroProf.setPixmap(QtGui.QPixmap.fromImage(image))
            
            elif self.option == 1:
                
                copy_frame = self.video1.copy()

                (color1_x, color1_y), self.found_color1 = find_color1(copy_frame)
                (color2_x, color2_y), self.found_color2 = find_color2(copy_frame)
                (color3_x, color3_y), self.found_color3 = find_color3(copy_frame)
                (color4_x, color4_y), self.found_color4 = find_color4(copy_frame)

                cv2.circle(copy_frame, (color1_x[0], color1_y[0]), 10, (0, 233, 255), -1)
                cv2.circle(copy_frame, (color1_x[1], color1_y[1]), 10, (0, 233, 255), -1)
                cv2.circle(copy_frame, (color1_x[2], color1_y[2]), 10, (0, 233, 255), -1)

                cv2.circle(copy_frame, (color2_x[0], color2_y[0]), 10, (255, 0, 0), -1)
                cv2.circle(copy_frame, (color2_x[1], color2_y[1]), 10, (255, 0, 0), -1)
                cv2.circle(copy_frame, (color2_x[2], color2_y[2]), 10, (255, 0, 0), -1)

                cv2.circle(copy_frame, (color3_x[0], color3_y[0]), 10, (0, 255, 0), -1)
                cv2.circle(copy_frame, (color3_x[1], color3_y[1]), 10, (0, 255, 0), -1)
                cv2.circle(copy_frame, (color3_x[2], color3_y[2]), 10, (0, 255, 0), -1)

                cv2.circle(copy_frame, (color4_x[0], color4_y[0]), 10, (0, 0, 255), -1)
                cv2.circle(copy_frame, (color4_x[1], color4_y[1]), 10, (0, 0, 255), -1)

                if self.found_color1:

                    self.punto1x,self.punto1y=color1_x,color1_y

                    #draw all 3 lines
                    cv2.line(copy_frame, (color1_x[0], color1_y[0]), (color1_x[1], color1_y[1]), (0, 233, 255), 2)
                    cv2.line(copy_frame, (color1_x[1], color1_y[1]), (color1_x[2], color1_y[2]), (0, 233, 255), 2)
                    cv2.line(copy_frame, (color1_x[2], color1_y[2]), (color1_x[0], color1_y[0]), (0, 233, 255), 2)

                if self.found_color2:

                    self.punto2x,self.punto2y=color2_x,color2_y

                    #draw all 3 lines
                    cv2.line(copy_frame, (color2_x[0], color2_y[0]), (color2_x[1], color2_y[1]), (255, 0, 0), 2)
                    cv2.line(copy_frame, (color2_x[1], color2_y[1]), (color2_x[2], color2_y[2]), (255, 0, 0), 2)
                    cv2.line(copy_frame, (color2_x[2], color2_y[2]), (color2_x[0], color2_y[0]), (255, 0, 0), 2)

                if self.found_color3:

                    self.punto3x,self.punto3y=color3_x,color3_y

                    #draw all 3 lines
                    cv2.line(copy_frame, (color3_x[0], color3_y[0]), (color3_x[1], color3_y[1]), (0, 255, 0), 2)
                    cv2.line(copy_frame, (color3_x[1], color3_y[1]), (color3_x[2], color3_y[2]), (0, 255, 0), 2)
                    cv2.line(copy_frame, (color3_x[2], color3_y[2]), (color3_x[0], color3_y[0]), (0, 255, 0), 2)

                if self.found_color4:

                    self.punto4x,self.punto4y=color4_x,color4_y

                    #draw all 3 lines
                    cv2.line(copy_frame, (color4_x[0], color4_y[0]), (color4_x[1], color4_y[1]), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color4_x[0], color4_y[0]), (color4_x[1], color4_y[0]), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color4_x[1], color4_y[1]), (color4_x[1], color4_y[0]), (0, 0, 255), 2)

                copy_frame=cv2.cvtColor(copy_frame,cv2.COLOR_BGR2RGB)

                image = qimage2ndarray.array2qimage(copy_frame)

                self.labelNuevoRegistroProf.setPixmap(QtGui.QPixmap.fromImage(image))
                
    def CapAngulo(self):

        if self.found_color1:

            self.angulo1 = angulopuntos(self.punto1x,self.punto1y)
            labelVR  = "Angulo 1: " + str(self.angulo1)
            self.labelAngulo1_2.setText(labelVR)

        if self.found_color2:

            self.angulo2 = angulopuntos(self.punto2x,self.punto2y)
            labelVL  = "Angulo 2: " + str(self.angulo2)
            self.labelAngulo2_2.setText(labelVL)

        if self.found_color3:

            self.angulo3 = angulopuntos(self.punto3x,self.punto3y)
            labelEsp = "Angulo 3: " + str(self.angulo3)
            self.labelAngulo3_2.setText(labelEsp)

        if self.found_color4:

            self.angulo4 = angulo2p(self.punto4x,self.punto4y)
            labelEsc = "Angulo 4: " + str(self.angulo4)
            self.labelAngulo4_2.setText(labelEsc)

        if self.angulo1 and self.angulo2 and self.angulo3 and self.angulo4 > 0:

            self.botonAdminGuardar_2.setEnabled(True)
        
        self.L_Angulos=[self.angulo1,self.angulo2,self.angulo3,self.angulo4]

    def videoC(self):
        
        global n
        self.option= not self.option
        n=0

    def Captura(self):
        global captura
        global captura2
        global curvas
     
        curvas = Capturar(captura)
        img = cv2.imread('temp.png')
        frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.labelScreenCurvas.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def consModelo3D(self):
        global curvas
        self.labelEstado1.setText("Modelo Cargado")
        Modelo3D(curvas)

    def MostrarCurvas(self):
        global curvas
        mCurvas(curvas)
    
    def mod3D(self):
        mostrar3D()
        
    def mod3DHistorial(self):
        
        self.labelEstado2.setText("Cargando Modelo")
        Modelo3D(self.curvaH[self.RadioGroup2.checkedId()])
        mostrar3D()
        self.labelEstado2.setText("Modelo Cargado")
          
    def Screen3D(self):
        screenModelo3D()
        img = cv2.imread('temp2.png')
        frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.labelScreen3D.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def Cambiar2Curvas(self):
        self.stackedWidgetCaptura.setCurrentIndex(curv)
        
    def Cambiar2m3d(self):
        self.stackedWidgetCaptura.setCurrentIndex(modelo3d)
        
    def GuardarDatos(self):
        
        global curvas
                
        apunte=self.plainTextEditApuntes_2.toPlainText()
        
        G_Datos(curvas,self.L_Angulos,apunte,self.usuario_b)
        
    def closeEvent(self,event):
        resultado = QMessageBox.question(self,"Salir...","Desea cerrar la aplicacion?",
                                         QMessageBox.Yes|QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else:
            event.ignore()

    def EntrarPantalla1(self):
        
        self.h1=self.MainWindow1.lineEditUsuario.text()
        self.h2=self.MainWindow1.lineEditClave.text()
        
        self.MainWindow1.labelNombrePaciente.setText("Nombre: ")
        self.MainWindow1.labelEdadPaciente.setText("Edad: ")
        self.MainWindow1.labelAngulo1.setText("Angulo 1: ")
        self.MainWindow1.labelAngulo2.setText("Angulo 2: ")
        self.MainWindow1.labelAngulo3.setText("Angulo 3: ")
        self.MainWindow1.labelAngulo4.setText("Angulo 4: ")
        self.MainWindow1.plainTextEditApuntes.clear()
        self.lineEditBuscar.clear()
        
        self.MplWidget.canvas.ax.clear()
        
        self.MplWidget.canvas.ax.axis("off")
        
        self.MplWidget.canvas.draw()
        
        self.MainWindow1.labelNombreUsuario_2.setText("Usuario: "+self.h1)
        self.MainWindow1.labelNombreUsuario.setText("Usuario: "+self.h1)
        
        if ver_cuenta(self.h1,self.h2) == 1:
            self.EntrarDoctor()
            
        elif ver_cuenta(self.h1,self.h2) == 2:
            self.EntrarAdmins()
            
        else:
            
            pass
        
    def EntrarDoctor(self):
                
        self.stackedWidgetHome.setCurrentIndex(pantalla1)
        self.stackedWidgetPantalla1.setCurrentIndex(resumen)
        
        completarID = QCompleter(ob_clientes())
        completarID.setCaseSensitivity(Qt.CaseInsensitive)
        self.MainWindow1.lineEditBuscar.setCompleter(completarID)
        
    def EntrarAdmins(self):
        self.stackedWidgetHome.setCurrentIndex(admins)
        self.tableAdminEditar.setColumnWidth(0,270) #codigo
        self.tableAdminEditar.setColumnWidth(1,80) #nombre
        self.tableAdminEditar.setColumnWidth(2,150) #cantidad
        self.tableAdminEditar.setColumnWidth(3,150) #precio
        self.stackedWidgetAdmin.hide()
    
    def NuevoUsuario(self):
        
        self.stackedWidgetAdmin.show()
        self.stackedWidgetAdmin.setCurrentIndex(nuevo)
        
        self.labelAdminAgregado.setText("Agregado : ")
        
        self.lineEditAdminNuevo_6.clear()
        self.lineEditAdminNuevo_3.clear()
        self.lineEditAdminNuevo.clear()
        self.lineEditAdminNuevo_2.clear()
        
        self.RadioGroup.setExclusive(False)
        self.radioBotonTerapeuta.setChecked(False)
        self.radioBotonPaciente.setChecked(False)
 
        self.RadioGroup.setExclusive(True)
        
        self.lineEditAdminNuevo_6.setEnabled(False)
        self.lineEditAdminNuevo_3.setEnabled(False)
        self.lineEditAdminNuevo.setEnabled(False)
        self.lineEditAdminNuevo_2.setEnabled(False)
        
        self.botonAdminGuardar.setEnabled(False)
        
    def BorrarUsuario(self):
        
        self.stackedWidgetAdmin.show()
        self.stackedWidgetAdmin.setCurrentIndex(borrar)
        
        self.lineEditAdminNuevo_4.clear()
        completarID = QCompleter(ob_CYT())
        completarID.setCaseSensitivity(Qt.CaseInsensitive)
        self.MainWindow1.lineEditAdminNuevo_4.setCompleter(completarID)
        
    def EditarUsuario(self):
        
        self.stackedWidgetAdmin.show()
        self.stackedWidgetAdmin.setCurrentIndex(editar)
        self.lineEditAdminNuevo_5.clear()
        self.tableAdminEditar.clear()
        completarID = QCompleter(ob_CYT())
        completarID.setCaseSensitivity(Qt.CaseInsensitive)
        self.MainWindow1.lineEditAdminNuevo_5.setCompleter(completarID)
        self.botonEditarUsuario_4.setEnabled(False)
        self.tableAdminEditar.setEnabled(False)
        
    def Seleccionado(self):
        
        self.radio_button = self.sender()
        self.botonAdminGuardar.setEnabled(True)
        if self.radio_button.text()=='Terapeuta':
            
            self.lineEditAdminNuevo_6.setEnabled(True)
            self.lineEditAdminNuevo_3.setEnabled(True)
            self.lineEditAdminNuevo.setEnabled(True)
            self.lineEditAdminNuevo_2.setEnabled(True)
            
        if self.radio_button.text()=='Paciente':
            self.lineEditAdminNuevo_6.setEnabled(True)
            self.lineEditAdminNuevo_3.setEnabled(True)
            self.lineEditAdminNuevo.setEnabled(False)
            self.lineEditAdminNuevo_2.setEnabled(False)
            
    def GuardarUsuario(self):
        
        nombre1=self.lineEditAdminNuevo_6.text()
        edad1=self.lineEditAdminNuevo_3.text()
        usuario1=self.lineEditAdminNuevo.text()
        clave1=self.lineEditAdminNuevo_2.text()
        ID=self.radio_button.text()
        
        insertarDatos(nombre1, edad1, usuario1, clave1, ID)
        
        self.labelAdminAgregado.setText("Agregado : "+str(nombre1))
        
    def b_usuario(self):        
        usuario=self.lineEditAdminNuevo_4.text()
        eliminarDatos(usuario)
        completarID = QCompleter(ob_CYT())
        completarID.setCaseSensitivity(Qt.CaseInsensitive)
        self.MainWindow1.lineEditAdminNuevo_4.setCompleter(completarID)
        
    def buscareditusuario(self):        
        self.identificador=self.lineEditAdminNuevo_5.text()
        nombre,edad,usuario,clave,self.tb = dato_cliente(self.identificador)
        
        self.tableAdminEditar.setItem(0, 0, QTableWidgetItem(nombre))
        self.tableAdminEditar.setItem(0, 1, QTableWidgetItem(str(edad)))
        self.tableAdminEditar.setItem(0, 2, QTableWidgetItem(usuario))
        self.tableAdminEditar.setItem(0, 3, QTableWidgetItem(clave))
        
        self.botonEditarUsuario_4.setEnabled(True)
        self.tableAdminEditar.setEnabled(True)
        
    def edit_usuario(self):    
        nombre=self.tableAdminEditar.item(0,0).text()
        edad=self.tableAdminEditar.item(0,1).text()
        usuario=self.tableAdminEditar.item(0,2).text()
        clave=self.tableAdminEditar.item(0,3).text()
        
        update_usuario(nombre,edad,usuario,clave,self.tb,self.identificador)
        
        self.botonEditarUsuario_4.setEnabled(False)
        self.tableAdminEditar.setEnabled(False)
        
        completarID = QCompleter(ob_CYT())
        completarID.setCaseSensitivity(Qt.CaseInsensitive)
        self.MainWindow1.lineEditAdminNuevo_5.setCompleter(completarID)
        
    def Resumen(self): 
        self.stackedWidgetPantalla1.setCurrentIndex(resumen)

        for i in reversed(range(self.Layout1.count())):

            self.Layout1.itemAt(i).widget().deleteLater()
        
        self.usuario_b = self.MainWindow1.lineEditBuscar.text()
        
        nombre,edad,usuario,clave,tb = dato_cliente(self.usuario_b)
        
        if nombre != "":
            
            self.resumenPaciente.setEnabled(True)
            
        else:
            
            pass
        
        fecha,curva,angulos,apunte = ult_paciente(self.usuario_b)
            
        self.MainWindow1.labelNombrePaciente.setText("Nombre: "+ nombre)
        self.MainWindow1.labelEdadPaciente.setText("Edad: "+ str(edad))
        self.MainWindow1.labelAngulo1.setText("Angulo 1: "+ str(angulos[0]))
        self.MainWindow1.labelAngulo2.setText("Angulo 2: "+ str(angulos[1]))
        self.MainWindow1.labelAngulo3.setText("Angulo 3: "+ str(angulos[2]))
        self.MainWindow1.labelAngulo4.setText("Angulo 4: "+ str(angulos[3]))
        self.MainWindow1.plainTextEditApuntes.setPlainText(apunte)
        
        self.MplWidget.canvas.ax.axis("off")
        
        colores = np.linspace(0.26,0.3,7*5)
        
        self.MplWidget.canvas.ax.contourf(np.flip(curva),levels=colores
                  ,colors=['#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                           '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                           '#51e014','#33e014','#14e01b','#14e047','#14e070',
                           '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                           '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                           '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                           '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0']
                            ,extend='both')
    
        self.MplWidget.canvas.draw()
        self.MplWidget.canvas.ax.clear()
        
        
    def NuevoRegistro(self):

        global curvas

        self.timer.start(40)
        self.botonAdminGuardar_2.setEnabled(False)

        curvas = np.zeros((240,320))

        self.labelScreenCurvas.clear()

        self.angulo1=self.angulo2=self.angulo3=self.angulo4=float(0)

        labelVR  = "Angulo 1: " + str(0)
        labelVL  = "Angulo 2: " + str(0)
        labelEsp = "Angulo 3: " + str(0)
        labelEsc = "Angulo 4: " + str(0)

        self.labelAngulo1_2.setText(labelVR)
        self.labelAngulo2_2.setText(labelVL)
        self.labelAngulo3_2.setText(labelEsp)
        self.labelAngulo4_2.setText(labelEsc)

        self.stackedWidgetPantalla1.setCurrentIndex(nRegistro)
        self.stackedWidgetCaptura.setCurrentIndex(curv)
        self.nuevoRegistro.setEnabled(True)
        self.plainTextEditApuntes_2.clear()
        
    def Historial(self):      
        self.comboBox_1.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        
        self.RadioGroup2.setExclusive(False)
        
        self.radioBotonData.setChecked(True)
        self.radioBotonData_2.setChecked(False)
        self.radioBotonData_3.setChecked(False)
 
        self.RadioGroup2.setExclusive(True)
        
        self.radioBotonData.setEnabled(False)
        self.radioBotonData_2.setEnabled(False)
        self.radioBotonData_3.setEnabled(False)
        
        self.botonModeloHistorial.setEnabled(False)
        self.botonCurvasHistorial.setEnabled(False)
        
        self.labelNombrePacienteHist.setText("paciente: "+ self.usuario_b)
        
        self.plainTextEditApuntes_3.clear()
        self.labelHistorialAngulo1.setText("Angulo 1: ")
        self.labelHistorialAngulo2.setText("Angulo 2: ")
        self.labelHistorialAngulo3.setText("Angulo 3: ")
        self.labelHistorialAngulo4.setText("Angulo 4: ")
        
        self.stackedWidgetPantalla1.setCurrentIndex(historial)
        self.historial.setEnabled(True)
        
        self.fechas=fechas_paciente(self.usuario_b)
        conteo=conteo_paciente(self.usuario_b)

        self.indexH=len(conteo)
        
        self.comboBox_1.addItems(self.fechas)
        self.comboBox_2.addItems(self.fechas)
        self.comboBox_3.addItems(self.fechas)
        self.comboBox_4.addItems(conteo)
        
        self.MplWidget1.canvas.ax1.clear()
        self.MplWidget1.canvas.ax2.clear()

        self.MplWidget2.canvas.ax.clear()
        
        self.MplWidget1.canvas.ax.axis("off")
        self.MplWidget1.canvas.ax1.axis("off")
        self.MplWidget1.canvas.ax2.axis("off")
        
        self.MplWidget1.canvas.draw()
        self.MplWidget2.canvas.draw()
        
    def S_historialdata(self):
        try:
            
            self.plainTextEditApuntes_3.setPlainText(self.h_apuntes[self.RadioGroup2.checkedId()])
            self.labelHistorialAngulo1.setText("Angulo 1: "+ str(self.h_angulos[self.RadioGroup2.checkedId()][0]))
            self.labelHistorialAngulo2.setText("Angulo 2: "+ str(self.h_angulos[self.RadioGroup2.checkedId()][1]))
            self.labelHistorialAngulo3.setText("Angulo 3: "+ str(self.h_angulos[self.RadioGroup2.checkedId()][2]))
            self.labelHistorialAngulo4.setText("Angulo 4: "+ str(self.h_angulos[self.RadioGroup2.checkedId()][3]))
        
        except AttributeError:
            
            pass
        
    def NuevoRegistroAtras(self):

        self.timer.stop()
        self.stackedWidgetPantalla1.setCurrentIndex(resumen)
        self.Resumen()
        
    def HistorialAtras(self):
        self.stackedWidgetPantalla1.setCurrentIndex(resumen) 
        
    def HistorialBuscarFecha(self):

        self.curvaH=["","",""]
                                                         
        select1=self.comboBox_1.currentText()           
        select2=self.comboBox_2.currentText()          
        select3=self.comboBox_3.currentText()
        
        self.radioBotonData.setEnabled(True)
        self.radioBotonData_2.setEnabled(True)
        self.radioBotonData_3.setEnabled(True)
        
        self.botonModeloHistorial.setEnabled(True)
        self.botonCurvasHistorial.setEnabled(True)
        
        h_curvas,self.h_angulos,self.h_apuntes=hist_paciente(select1,select2,select3)
        self.curvaH[0] = np.array(h_curvas[0])
        self.curvaH[1] = np.array(h_curvas[1])
        self.curvaH[2] = np.array(h_curvas[2])
        
        self.curvaH[0] = np.reshape(self.curvaH[0],(240,320))
        self.curvaH[1] = np.reshape(self.curvaH[1],(240,320))
        self.curvaH[2] = np.reshape(self.curvaH[2],(240,320))
        
        self.curvaH[0][self.curvaH[0]==0] = None       
        self.curvaH[1][self.curvaH[1]==0] = None     
        self.curvaH[2][self.curvaH[2]==0] = None   
        
        self.S_historialdata()
                
        self.MplWidget1.canvas.ax.axis("off")
        self.MplWidget1.canvas.ax1.axis("off")
        self.MplWidget1.canvas.ax2.axis("off")
        
        colores = np.linspace(0.26,0.3,7*5)
        
        self.MplWidget1.canvas.ax.contourf(np.flip(self.curvaH[0]),levels=colores
                  ,colors=['#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                           '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                           '#51e014','#33e014','#14e01b','#14e047','#14e070',
                           '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                           '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                           '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                           '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0']
                            ,extend='both')
        
        self.MplWidget1.canvas.ax1.contourf(np.flip(self.curvaH[1]),levels=colores
                  ,colors=['#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                           '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                           '#51e014','#33e014','#14e01b','#14e047','#14e070',
                           '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                           '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                           '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                           '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0']
                            ,extend='both')
    
        self.MplWidget1.canvas.ax2.contourf(np.flip(self.curvaH[2]),levels=colores
                  ,colors=['#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                           '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                           '#51e014','#33e014','#14e01b','#14e047','#14e070',
                           '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                           '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                           '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                           '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0']
                            ,extend='both')
    
    
        self.MplWidget1.canvas.draw()
        
        self.MplWidget1.canvas.ax.clear()
        self.MplWidget1.canvas.ax1.clear()
        self.MplWidget1.canvas.ax2.clear()
       
    def HistorialAmp(self):

        for i in range(int(self.comboBox_4.currentText())):

            self.comboBox = QtWidgets.QComboBox(self.historialmaxi)
         
            font = QtGui.QFont()
            font.setPointSize(12)
            self.comboBox.setFont(font)
            self.comboBox.setObjectName("comboBox_{}".format(str(i+5)))
        
            self.Layout1.addWidget(self.comboBox)
            self.comboBox.addItems(self.fechas)


        self.stackedWidgetPantalla1.setCurrentIndex(historialmax)

    def HistorialBuscarFechaMax(self):

        fechaMax=[None]*self.Layout1.count()

        for i in (range(self.Layout1.count())):

            fechaMax[i]=self.Layout1.itemAt(i).widget().currentText()

        self.angulosMax=hist_pacienteMax(self.Layout1.count(),fechaMax)

        Num = ["1","2","3","4"]

        for i in (range(self.Layout1.count())):

            self.MplWidget2.canvas.ax.plot(Num, self.angulosMax[i], marker = 'o', label = fechaMax[i][:10])

        self.MplWidget2.canvas.ax.set_xlabel("Angulos", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
        self.MplWidget2.canvas.ax.set_ylabel("Grados", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})

        self.MplWidget2.canvas.ax.legend(loc = 'upper right')

        self.MplWidget2.canvas.ax.set_xlim([0,4])

        self.MplWidget2.canvas.draw()

        self.MplWidget2.canvas.ax.clear()

    def CurvasHistorial(self):
         
        mCurvasHistorial(self.curvaH[0],self.curvaH[1],self.curvaH[2])
        
    def Salir2Bienvenida(self):
        self.stackedWidgetHome.setCurrentIndex(bienvenida)
        self.resumenPaciente.setEnabled(False)
        self.lineEditUsuario.clear()
        self.lineEditClave.clear()

        for i in reversed(range(self.Layout1.count())):

            self.Layout1.itemAt(i).widget().deleteLater()

    def HistorialMaxAtras(self):

        self.MplWidget2.canvas.ax.clear()

        self.MplWidget2.canvas.draw()

        self.stackedWidgetPantalla1.setCurrentIndex(historial)

        for i in reversed(range(self.Layout1.count())):

            self.Layout1.itemAt(i).widget().deleteLater()

      
app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()