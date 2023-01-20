# coding=utf-8
#include <QString>
"""
Created on Tue Dec  1 18:32:50 2020

@author: juan david, Adrian David
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, util, measure
from stl import mesh
import trimesh
import pyrender
import math
def AjustarImagen(arr2d):
    npArr2d = np.zeros((240,320))
    Red = np.empty((320,240),np.uint8)
    matrizFiltros = np.empty((240,320,4),np.uint8)
    npArr2d = arr2d
    
    matrizFiltros[:,:,0] = npArr2d 
    matrizFiltros[:,:,1] = npArr2d
    matrizFiltros[:,:,2] = npArr2d
    
    FA0 = matrizFiltros[:,:,0]
    FA1 = matrizFiltros[:,:,1]
    FA2 = matrizFiltros[:,:,2] 
    
    #para ver los angulos
    FA1[FA1 < 140+15] = 0
    FA1[FA1 > 155+15] = 0 
    #para ver modelo 3D
    FA2[FA2 < 62] = 120
    FA2[FA2 > 62+15] = 120
    #Unir las 3 capas
    matrizFiltros[:,:,0] = FA0 
    matrizFiltros[:,:,1] = FA1
    matrizFiltros[:,:,2] = FA2 
    # #rotarYtrasladar
    # #Para Ver los Angulos
    cv2.line(matrizFiltros,(160,0),(160,240),(16,232,16),2)        #-----------------#
    cv2.rectangle(matrizFiltros,(120,20),(200,195),(16,232,16),2)  #-----------------#
    cv2.rectangle(matrizFiltros,(100,20),(220,195),(20,88,224),2)  #--------3D--------#
    return matrizFiltros

def Capturar(captura):
    captura = abs(captura)
    captura = captura/float(captura.max())
    captura2 = np.copy(captura)
    min = 0.25                                               #-----------------#
    max = min+0.08                                               #-----------------#
    captura[captura<min] = None                              #-----------------#
    captura[captura>max] = None                              #-----------------#
    captura2[captura2<min] = 0                               #-----------------#
    captura2[captura2>max] = 0                               #-----------------#
 
    rect = np.empty((240,320))                               #-----------------#
    rect[10:240,80:240] = 1                                #-----------------#
    captura2 = captura2*rect                                  #-----------------#
    np.save('capRec2.txt',captura2)                             #-----------------# 
    fig = plt.figure(0)

    plt.imshow(captura2)
    
    fig.savefig('temp.png')
    plt.close(0)
  
    return captura2

def mCurvas(captura):
    
    captura = np.flip(captura)
    captura = np.fliplr(captura)
    min = 0.25                                               #-----------------#
    max = min+0.08 
    colores = np.linspace(min+0.01,max-0.03,7*5)
    fig = plt.figure(0)
    plt.contourf(captura,colores
              ,colors=['#ffffff',
                        '#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                        '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                        '#51e014','#33e014','#14e01b','#14e047','#14e070',
                        '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                        '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                        '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                        '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0',
                        '#ffffff']
              ,extend='both')
    plt.show()
    
def mCurvasHistorial(c0,c1,c2):
    c0 = np.flip(c0)
    c1 = np.flip(c1)
    c2 = np.flip(c2)
    min = 0.25                                               #-----------------#
    max = min+0.08 
    colores = np.linspace(min+0.01,max-0.03,7*5)
    plt.subplot(1,3,1)
    plt.contourf(c0,colores
              ,colors=['#ffffff',
                        '#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                        '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                        '#51e014','#33e014','#14e01b','#14e047','#14e070',
                        '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                        '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                        '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                        '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0',
                        '#ffffff']
              ,extend='both')
    plt.subplot(1,3,2)
    plt.contourf(c1,colores
             ,colors=['#ffffff',
                       '#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                       '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                       '#51e014','#33e014','#14e01b','#14e047','#14e070',
                       '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                       '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                       '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                       '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0',
                       '#ffffff']
             ,extend='both')
    plt.subplot(1,3,3)
    plt.contourf(c2,colores
             ,colors=['#ffffff',
                       '#e02814','#e04014','#e05b14','#e07d14','#e0c814',
                       '#d9e014','#cce014','#b0e014','#95e014','#70e014',
                       '#51e014','#33e014','#14e01b','#14e047','#14e070',
                       '#14e08b','#14e0aa','#14e0be','#14e0cf','#14cfe0',
                       '#14bbe0','#14ade0','#149ce0','#1484e0','#146ce0',
                       '#1458e0','#143de0','#143de0','#2814e0','#4714e0',
                       '#5514e0','#7014e0','#8b14e0','#9914e0','#b714e0',
                       '#ffffff']
             ,extend='both')
    plt.show()
   
def Modelo3D(modelo):
    modelo[np.isnan(modelo)] = 0 
    file = modelo
    original = np.copy(file)
    matrizProf = np.copy(file)
    #Definir Maximos y Minimos
    file[file==0] = 2
    miin = file.min()
    file[file==2] = 0
    maax = file.max()
    #filtrar
    umbral = 255
    matrizProf[matrizProf<miin] = umbral
    matrizProf[matrizProf>maax] = umbral
    matrizProf[matrizProf!=umbral] = 0    
    #Convertir de float a int
    M = np.array(matrizProf,dtype = np.uint8)
    A = np.empty((240,320,3),np.uint8)
    #Adecuar Formato RGB
    A[:,:,0] = M
    A[:,:,1] = M
    A[:,:,2] = M
    #Grosor de los bordes
    grosor = 9
    #Encontrar bordes 
    contours,_ = cv2.findContours(M, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #dibujar todos los bordes
    inC2 = np.empty((240,320,3),np.uint8)
    for i in range(0,len(contours)):
          inC2 = cv2.drawContours(A,contours,i,(120,120,120),grosor)  
          
    #Sacar pixeles de Bordes
    contorno = np.copy(inC2[:,:,2])
    contorno[contorno != 0] = 3
    contorno[contorno == 3] = 2
    contorno[contorno == 0] = 1
    contorno[contorno != 1] = 0
    #Filtro mediana
    kernel = 6
    new_img = np.zeros((240,320))
    for i in range (0,(original.shape[0]-1-kernel+1)):
        j=0
        while j <= original.shape[1]-1-kernel+1:
            mask = original[i:i+kernel-1,j:j+kernel-1]
            new_img[i,j]= np.mean(mask)
            j=j+1
    
    new_img = new_img*contorno
    
    #Convertir matriz 2D a Volumen 
    capas = 60
    niveles = np.linspace(miin,maax,capas)
    volumen = np.zeros((240,320,capas))
    for fil in range (0,240):
        for col in range(0,320):
            for comp in range (0,capas):
                if (comp+1 >= capas):
                    break
                if (new_img[fil,col] >= niveles[comp] and new_img[fil,col] < niveles[comp+1]):
                    volumen[fil,col,comp] = new_img[fil,col]
                    ########################
    verts, faces, normals, values = measure.marching_cubes_lewiner(volumen,0)
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
                    ########################
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = verts[f[j],:]
    
    # Guardar Modelo 3D
    cube.save('Modelo3D.stl')
    
def mostrar3D():
    fuze_trimesh = trimesh.load('Modelo3D.stl')
    mes = pyrender.mesh.Mesh.from_trimesh(fuze_trimesh,smooth=True)
    escene = pyrender.scene.Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
    escene.add(mes)
    pyrender.viewer.Viewer(escene, use_raymond_lighting=True)
    
def screenModelo3D():
    
    x = -170
    y = -130
    z = 100
    camera_pose =np.array([
       [1, 0, 0, x],
       [0, 1, 0, y],
       [0, 0, 1, z],
       [0, 0, 0, 1],
       ])
    fuze_trimesh = trimesh.load('Modelo3D.stl')
    mes = pyrender.mesh.Mesh.from_trimesh(fuze_trimesh,smooth=True)
    translate = pyrender.node.Node(mesh = mes, rotation=np.array([90, -90, -1, 1.0]))
    escene = pyrender.scene.Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
    escene.add_node(translate)
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 2.0, aspectRatio=1.0)
    escene.add(camera,pose=camera_pose)
    light=pyrender.SpotLight(color=(255,255,255),intensity=10000.0,range=1,innerConeAngle=np.pi/3.0,outerConeAngle=np.pi/2.0)
    escene.add(light, pose=camera_pose)
    r = pyrender.OffscreenRenderer(400, 400)
    color, depth = r.render(escene)
    fig = plt.figure(0)
    plt.axis('off')
    plt.imshow(color)
    fig.savefig('temp2.png')
    plt.close(0)