#! /usr/bin/python3

### REQUIRES python 3 !!!!

## Run:  ./sample.py
## Reads from stdin and writes to stdout
## For example:
##     ./sample.py <test.txt >test_out.txt

import os 
## Direcorio de instalación del API de python de freeling
directorio = (os.environ ['FREELING_PYTHON'] ) +"/APIs/python"
import sys
sys.path.append( directorio  )
import freeling

## Modify this line to be your FreeLing installation directory
FREELINGDIR = (os.environ ['FREELING_PYTHON'] );
DATA = FREELINGDIR+"/data";
LANG="/es";
freeling.util_init_locale("default")


def palabra(linea):
  global oracion;
  #print("la palabra " + pal)
  ini =linea.find('(')+1;
  fin =linea.find(')');
  lineainfo = linea[ini:fin];
  infoinipal= lineainfo.find(' ')
  pal=lineainfo[:infoinipal]
  oracion = oracion+ " " + pal
  return pal

def resultado():
  global accion_inferida;
  global producto_inferido;
  global parametros_inferidos;
  global accion_inferida_aux
  global producto_inferido_aux
  global parametros_inferidos_aux
  global oracion

  ## Si no he encontrado acción, prueba ha inlcuir "Quiero" en la oración y vuelvo a analizar
  if(accion_inferida==""):
    accion_inferida_aux=accion_inferida
    producto_inferido_aux=producto_inferido
    parametros_inferidos_aux=parametros_inferidos
    accion_inferida =""
    producto_inferido=""
    parametros_inferidos=""
    oracion = "Quiero " + oracion.lower()
    #print(oracion)
    os.system("echo \"" + oracion + "\" | analyzer_client localhost:50005 > aux.txt")
    ficheroaux = open('../extractorIntencionSuperbuscador/aux.txt')
    analisis(ficheroaux)
  else:
    ## Cuando tengo acción compruebo si la acción es "Quiero"
    ## Si es quiero, me quedo con el resultado del análisis sin incluir "Quiero"
    if( accion_inferida== "Quiero"):
      accion_inferida=accion_inferida_aux
      producto_inferido=producto_inferido_aux
      parametros_inferidos=parametros_inferidos_aux
    #print ("Accion : " + accion_inferida.upper() +" | " + "Producto : " + producto_inferido.upper() + " | Parametro : " + parametros_inferidos.upper())
    print ( accion_inferida.upper() +" | " + producto_inferido.upper() + " | " + parametros_inferidos.upper())  
    accion_inferida =""
    producto_inferido=""
    parametros_inferidos=""
    oracion=""


## ----------------------------------------------
## ------   ENCUENTRO UN SINTAGMA NOMINAL -------
## ----------------------------------------------
def sintagmanominal(fichero):
  global linea
  global producto_inferido
  global parametros_inferidos
  global fin_objdirec
  global fin_oracion
  global oracion

  while fin_objdirec==0 and fin_oracion==0:
    linea=fichero.readline();
    #print (" LINEA en SintagmaNominal: " + linea)
    pal=palabra(linea)
    if linea.find(']')>=0:
      fin_objdirec = 1;
    elif linea.find('F-term')>=0:
      fin_oracion = 1;
      resultado()
    elif linea.find('adj-mod')>=0:
      #print (" PAL: " + pal)
      parametros_inferidos= parametros_inferidos + " " + pal
    elif linea.find('obj-prep')>=0:
      parametros_inferidos= parametros_inferidos + " " + pal
    elif linea.find('sn-mod')>=0:
      parametros_inferidos= parametros_inferidos + " " + pal


def analisis(fichero):

  global linea
  global sinonimos
  global accion_inferida
  global producto_inferido
  global parametros_inferidos
  global fin_oracion 
  global fin_sn
  global fin_objdirec
  global oracion

 
  linea=fichero.readline();

  sinonimos=[]
  accion_inferida=""
  producto_inferido=""
  parametros_inferidos=""
  fin_oracion =0
  fin_sn=0
  fin_objdirec=0
  oracion=""

  #Leo el fichero
  while linea:
    fin_objdirec=0
    #print (" LINEA: " + linea)
    pal=palabra(linea)
    #Si la línea contiene un grupo verbal
    if linea.find('grup-verb')>=0 or linea.find('s-adj/top/')>=0 or linea.find('sadv/top/')>=0:
      accion_inferida = pal
      #print (" ACCION " + accion_inferida)
    elif linea.find('sn/')>=0 and producto_inferido=="" :

      ini =linea.find('(')+1;
      fin =linea.find(')');
      lineainfo = linea[ini:fin];
      infoinipal= lineainfo.find(' ')
      pal=lineainfo[:infoinipal]
      producto_inferido= pal;
      #print (" SINTAGMA NOMINAL " + producto_inferido);
      sintagmanominal(fichero);

    elif linea.find('F-term')>=0 :
      resultado()

    fin_oracion=0;
    fin_sn=0;
    fin_objdirec=0;
    linea=fichero.readline();

  fichero.close()


## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------
;
#Semantic Database Module
semantic = freeling.semanticDB (DATA + LANG +"/semdb.dat");

global oracion
global fin_oracion 
global fin_sn
global fin_objdirec
global linea
global sinonimos
global accion_inferida
global producto_inferido
global parametros_inferidos
global accion_inferida_aux
global producto_inferido_aux
global parametros_inferidos_aux

fichero = open('../extractorIntencionSuperbuscador/analisis_freeling.txt')
analisis(fichero)



