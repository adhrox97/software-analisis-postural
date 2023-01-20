# coding=utf-8
#include <QString>
"""
Created on Tue Dec  1 23:30:50 2020

@author: juan david, Adrian David
"""
import os # Importamos os
import sys
from datetime import date
from datetime import datetime
import string
import json
import numpy as np
from PyQt5.QtSql import *
import sqlite3

def db_connect(filename, server): # Recibe dos parametros: nombre de la base de datos, y el tipo.
        
        db = QSqlDatabase.addDatabase(server) # Creamos la base de datos
        db.setDatabaseName(filename) # Le asignamos un nombre

        if not db.open(): # En caso de que no se abra
            QMessageBox.critical(None, "Error al abrir la base de datos.\n\n"
                    "Click para cancelar y salir.", QMessageBox.Cancel)
            return False
        return True
    
def db_create():
        query = QSqlQuery() # Instancia de Query

        query.exec_("CREATE TABLE ADMINISTRADORES("
                    "USER VARCHAR(20), PASSWORD VARCHAR(20))")
        query.exec_("CREATE TABLE HISTORIAL("
                    "FECHA TEXT, CURVAS BLOB, ANGULOS BLOB, APUNTES TEXT, NOMBRE VARCHAR(100))")
        query.exec_("CREATE TABLE PACIENTE("
                    "NOMBRE VARCHAR(100), EDAD INTEGER)")
        query.exec_("CREATE TABLE TERAPEUTA("
                    "NOMBRE VARCHAR(100), EDAD INTEGER, USER VARCHAR(20), PASSWORD VARCHAR(20))")

if not os.path.exists('personas'):
    db_connect('personas', 'QSQLITE') 
    db_create() 
else:
    db_connect('personas', 'QSQLITE')

def ver_cuenta(h1,h2):
    
    query1 = QSqlQuery("SELECT USER,PASSWORD FROM terapeuta")
    query2 = QSqlQuery("SELECT USER,PASSWORD FROM administradores")
    
    flag = 0
    
    while (query1.next()):
                    
        username = query1.value(0)
        password = query1.value(1)
            
        if h1 == username and h2 == password:
        
            print ("Login!")
            tabla="terapeuta"
            l=1
            flag=1
            break
        
        else:
            
            continue
            
    while (query2.next()):
                    
        username = query2.value(0)
        password = query2.value(1)
            
        if h1 == username and h2 == password:
        
            print ("Login!")
            tabla="administradores"
            flag=2
            break
        
        else:
            
            continue
        
    return flag

def ob_clientes():
    
    connection = sqlite3.connect('personas')
    cursor = connection.execute('select nombre from paciente')
    
    names = list(map(lambda x: x[0], cursor.fetchall()))
    
    return names

def dato_cliente(n):
    
    nombre=usuario=clave=tabla=""
    edad=0
    
    query = QSqlQuery()
    query.exec_("""SELECT * FROM paciente WHERE nombre = '{0}'""".format(n.encode('utf-8')))
    tabla = "paciente"
    while query.next():
        
        nombre = query.value(0)
        edad = query.value(1)
        
    if nombre == "":
        
        query.exec_("""SELECT * FROM terapeuta WHERE nombre = '{0}'""".format(n.encode('utf-8')))
        tabla = "terapeuta"
        while query.next():
            
            nombre = query.value(0)
            edad = query.value(1)
            usuario = query.value(2)
            clave = query.value(3)
            
    return nombre,edad,usuario,clave,tabla

def insertarDatos(nombre1, edad1, usuario1, clave1, ID):
    
    t=0
    query = QSqlQuery() # Instancia de Query
    usernamecheck = query.exec_("""SELECT * FROM terapeuta WHERE user = '{0}'""".format(usuario1.encode('utf-8')))
  
    if ID == 'Terapeuta':
    
        while query.next():
            
            t += 1
            
            print(t)
            
        print(t)
        
        if t != 0:
    
            print("El usuario ya existe")
        
        else:
        
            query.exec_("INSERT INTO '{0}' VALUES('{1}', '{2}', '{3}', '{4}')".format(ID, nombre1.encode('utf-8'), edad1, usuario1, clave1))
    else:

        query.exec_("INSERT INTO '{0}' VALUES('{1}', '{2}')".format(ID, nombre1.encode('utf-8'), edad1))
        
def ob_CYT():
    
    connection = sqlite3.connect('personas')
    cursor = connection.execute('select nombre from terapeuta')
    
    names = list(map(lambda x: x[0], cursor.fetchall()))
    
    names = ob_clientes() + names
    
    return names

def eliminarDatos(user):

    query = QSqlQuery() # instancia de Query
    # Ejecutamos una sentencia. Eliminara toda fila cuyo
    # Valor de id sea igual al seleccionado
    query.exec_("DELETE FROM paciente WHERE nombre = '{0}'".format(user.encode('utf-8')))
    query.exec_("DELETE FROM terapeuta WHERE nombre = '{0}'".format(user.encode('utf-8')))
    query.exec_("DELETE FROM historial WHERE nombre = '{0}'".format(user.encode('utf-8')))
    
def update_usuario(nombre, edad, usuario, clave, tabla, nombre_an):
    
    query = QSqlQuery()
    
    if tabla == "terapeuta":
    
        query.exec_("""UPDATE {0} SET nombre = '{1}',edad = '{2}',user = '{3}',password = '{4}' 
                    WHERE nombre = '{5}'""".format(tabla,nombre,edad,usuario,clave,nombre_an.encode('utf-8')))
    
    else:

        query.exec_("""UPDATE {0} SET nombre = '{1}',edad = '{2}' 
                    WHERE nombre = '{3}'""".format(tabla,nombre,edad,nombre_an.encode('utf-8')))
                    
def G_Datos(captura,angulos,apunte,nombre):
    
    
    gg = np.reshape(captura,(76800))
    
    capactual = gg.tolist()
    
    now = datetime.now()
    fecha=str(now)
    
    profundidad = json.dumps(capactual)
    
    angulos_cod = json.dumps(angulos)
    
    query = QSqlQuery()
    
    query.exec_("INSERT INTO historial VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(fecha, profundidad, angulos_cod, apunte, nombre.encode('utf-8')))
    
def ult_paciente(nombre):
    
    fecha=curvas=angulos=apuntes=idnombre=""
    
    query = QSqlQuery()
    
    connection = sqlite3.connect('personas')
    
    cursor = connection.execute("SELECT * FROM historial WHERE nombre = '{0}' ORDER BY fecha DESC LIMIT 1".format(nombre.encode('utf-8')))
    
    h_date = list(map(lambda x: x[0], cursor.fetchall()))   
        
    query.exec_("""SELECT * FROM historial WHERE fecha = '{0}'""".format(h_date[0]))

    while query.next():
        
        fecha = query.value(0)
        curvas = query.value(1)
        angulos = query.value(2)
        apuntes = query.value(3)
        idnombre = query.value(4)
    
    d_curvas = json.loads(curvas)
    d_angulos = json.loads(angulos)
        
    matrizProf = np.zeros((240,320))
    vectProf = np.zeros(76800)
    jotaProf = 0
    
    array=np.array(d_curvas)
    
    for i in range (0,76800):
        
        vectProf[i] = array[i]
        
    #organizar la matriz de profundiad 320*240
    for filas in range (0,240):
        for columnas in range(0,320):
            matrizProf[filas,columnas] = vectProf[jotaProf]
            jotaProf = jotaProf + 1
    
    matrizProf[matrizProf==0] = None                              
    
    return fecha,matrizProf,d_angulos,apuntes
    
def hist_paciente(c1,c2,c3):
    
    fechas=(c1,c2,c3)
    
    fecha=curvas=angulos=apuntes=idnombre=""
    fecha1=["","",""]
    d_curvas=["","",""]
    d_angulos=["","",""]
    idnombre1=["","",""]
    apuntes1=["","",""]
    
    query = QSqlQuery()        
        
    for i in range(3):
        
        query.exec_("""SELECT * FROM historial WHERE fecha = '{0}'""".format(fechas[i]))
    
        while query.next():
            
            fecha=query.value(0)
            curvas=query.value(1)
            angulos=query.value(2)
            apuntes=query.value(3)
            idnombre=query.value(4)
    
        fecha1[i]=fecha
        d_curvas[i]=json.loads(curvas)
        d_angulos[i]=json.loads(angulos)
        apuntes1[i]=apuntes
        idnombre1[i]=idnombre
    
    return d_curvas,d_angulos,apuntes1

def hist_pacienteMax(Nfechas,fechas):
    
    fecha=curvas=angulos=apuntes=idnombre=""

    d_angulos=[None]*Nfechas
    
    query = QSqlQuery()        
        
    for i in range(Nfechas):
        
        query.exec_("""SELECT * FROM historial WHERE fecha = '{0}'""".format(fechas[i]))
    
        while query.next():
            
            fecha=query.value(0)
            curvas=query.value(1)
            angulos=query.value(2)
            apuntes=query.value(3)
            idnombre=query.value(4)
    
        d_angulos[i]=json.loads(angulos)
    
    return d_angulos

def fechas_paciente(nombre):
    
    connection = sqlite3.connect('personas')
    
    cursor = connection.execute("SELECT * FROM historial WHERE nombre = '{0}' ORDER BY fecha ASC".format(nombre.encode('utf-8')))
    
    h_date = list(map(lambda x: x[0], cursor.fetchall()))
    
    return h_date

def conteo_paciente(nombre):

    lista=[]
    
    connection = sqlite3.connect('personas')
    
    cursor = connection.execute("SELECT COUNT(*) FROM historial WHERE nombre = '{0}' ORDER BY fecha ASC".format(nombre.encode('utf-8')))
    
    h_conteo = list(map(lambda x: x[0], cursor.fetchall()))

    if h_conteo[0] > 10:

        lista.extend(range(1,11))

    else:

        lista.extend(range(1,h_conteo[0]+1))

    lista_str = map(str,lista)
    
    return lista_str