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

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local";
FREELINGDIR = (os.environ ['FREELING_PYTHON'] )  ;

DATA = FREELINGDIR+"/data";
LANG="/es";

freeling.util_init_locale("default");

#Semantic Database Module
semantic = freeling.semanticDB (DATA + LANG +"/semdb.dat");

#Conjunto de acciones
acciones = ['consultar', 'realizar', 'ayuda', 'devolver', 'pagar', 'modificar' ]
acciones_sustantivo= ['ayuda']
#acciones_sinonimos = ['consultar','ejecutar','realizar','causar','crear','hacer','realizar','organizar','realizar','efectuar','cumplir',' modificar','alterar','cambiar','','alterar','arreglar','pagar','avalar','subvencionar','abonar','liquidar','costear','dar','devengar','rendir','compensar','enmendarse',
#'expiar','ayudar','auxiliar','asistir','devolver','reponer','llevar_de_regreso','regresar','traer_de_regreso','reembolsar','volver_a_pagar','reembolsar']

#Conjunto de productos
productos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo' ,  'seguro', 'impuesto', 'cuenta']
productos_sinonimos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo'  ,'transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];
productos_verbo= ['transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];
productor_clave=['clave', 'contraseña']

fichero = open('../extractorIntencionSuperbuscador/analisis_freeling.txt')
linea=fichero.readline();
contador_lineas=1;

sinonimos=[]
accion_inferida=""
producto_inferido=""
parametros_inferidos=""
busqueda_OD=0;
encontrado_producto=0
busqueda_OI=0;
contador_lineas_OD=0;
contador_lineas_OI=0;
sin_accion=1;
flag_negacion=0;
linea_negacion=0;

#Obtengo los sinónimos de mis acciones

#Leo el fichero
while linea:
  #print (" LINEA: " + str(linea.find('sn/')) + " / " + linea)
  ini =linea.find('(')+1;
  fin =linea.find(')');
  lineainfo = linea[ini:fin];
  infoini= lineainfo.find(' ')
  infoini=lineainfo.find(' ', infoini+1)
  infofin=lineainfo.find(' ', infoini+1)
  etimorfo=lineainfo[infoini:infofin]
  #print (" Etiqueta norfologica " + etimorfo)

  ## Si la línea contiene una negación
  if linea.find('neg')>=0 :
    flag_negacion=1;
    linea_negacion=contador_lineas;

  #Compruebo si en la línea anterior había una negación, y en esta línea hay un participio
  #es que he detectado un adjetivo con negación
  elif flag_negacion==1 and (linea_negacion+1)==contador_lineas and (etimorfo.find('VMP')>=0) :
    #print ("Encontrado ADJETIVO, con NEGACION");
    ini =linea.find('(')+1;
    fin =linea.find('-',ini,len(linea))-8;
    directo = linea[ini:fin];
    find= directo.find(' ')
    parametros_inferidos = "no " + directo[:find]


  #Si la línea contiene un grupo verbal
  elif linea.find('grup-verb')>=0:
    #print ("Encontrado GRUPO VERBAL");
    ini =linea.find('(')+1;
    fin =linea.find('-',ini,len(linea))-8;
    accion = linea[ini:fin];
    ##print ("Accion: "+ str(accion));

    #Extraigo los sentidos
    finsen =linea.find(')');
    senses = linea[fin:finsen]
    pos = 0
    #print ("Sentidos: "+ str(senses));
    while senses.find(':0',pos,len(senses))>0 :
      sense=senses[pos-10:pos];
      #print ("Sentido: "+ str(sense));
      #Obtengo la info del sentido
      senseinfo = semantic.get_sense_info (sense);

      #Obtengo los SINONIMOS
      sinos= senseinfo.words;
      #for sino in sinos:
        #print ("  sinonimo: " + sino)

      #Miro con cual de las acciones se corresponde la accion extraida
      #Comparo todas las acciones con todos los sinonimos
      cont=0;
      while accion_inferida=="" and cont<len(sinos):
        sino=sinos[cont]
        for a in acciones:
          if a==sino:
            accion_inferida=a
            #print ("Accion inferida: " +accion_inferida)
        cont=cont+1;
      pos = senses.find(':0',pos+2,len(senses));

      #Si no he encontrado una accion asociada, busco en el listado de verbos asociados a los productos
      cont=0;
      while producto_inferido=="" and cont<len(sinos):
        sino=sinos[cont]
        for a in productos_verbo:
          if a==sino:
            producto_inferido="transferencia"
            encontrado_producto=1
            #print ("Accion inferida: " +accion_inferida)
        cont=cont+1;

      pos = senses.find(':0',pos+2,len(senses));


  #Si la línea es la del posible producto
   #O se ha identificado la línea del OD pero todavía no se ha localizado el SN
  elif linea.find('dobj')>=0 or (contador_lineas!=1 and (contador_lineas_OD+1 == contador_lineas)):
    #print ("Encontrado OBJETO DIRECTO");
    if linea.find('dobj')>=0 and (linea.find('sn'))<0:
      contador_lineas_OD = contador_lineas
    #Si la línea contiene el sintagma nominal del OD,
    elif ((linea.find('sn'))>=0 ):
      ini =linea.find('(')+1;
      fin =linea.find('-',ini,len(linea))-8;
      directo = linea[ini:fin];
      #print ("Objeto  Directo: "+ str(directo));
      # ya he encontrado el OD
       #Extraigo los sentidos
      finod =linea.find(')');
      senses = linea[fin:finod]
      pos = 0
      #print ("Sentidos: "+ str(senses));
      while senses.find(':0',pos,len(senses))>0 :
        sense=senses[pos-10:pos];
        #print ("Sentido: "+ str(sense));
        #Obtengo la info del sentido
        senseinfo = semantic.get_sense_info (sense);
        #Obtengo los sinonimos
        sinos= senseinfo.words;
        #for sino in sinos:
        #  print ("sinonimo: " + sino)
        #Miro con cual de las productos se corresponde la accion extraida
        #Comparo todos los productos con todos los sinonimos
        cont=0;
        while producto_inferido=="" and cont<len(sinos):
          sino=sinos[cont]
          for p in productos:
            if p==sino:
              producto_inferido=p
              encontrado_producto=1
              #print ("Producto inferido: " +producto_inferido)
          cont=cont+1;
        cont=0;
        while producto_inferido=="" and cont<len(sinos):
          sino=sinos[cont]
          for p in productor_clave:
            if p==sino:
              producto_inferido="clave"
              encontrado_producto=1
              #print ("Producto inferido: " +producto_inferido)
          cont=cont+1;

        pos = senses.find(':0',pos+2,len(senses));
      contador_lineas_OD= 0

  #Si hay un objeto indirecto
  #O se ha identificado la línea del OI pero todavía no se ha localizado el SN
  elif linea.find('iobj')>=0 or busqueda_OI==1:
    #print ("Encontrado OBJETO INDIRECTO");
    #Si la línea contiene el sintagma nominal del OI
    if(linea.find('sn'))>=0:
      ini =linea.find('(')+1;
      fin =linea.find('-',ini,len(linea))-8;
      indirecto = linea[ini:fin];
      #print("Objeto Indirecto: " +indirecto);
      # ya he encontrado el OI
      busqueda_OI = 0
    else:
      busqueda_OI=1;

  elif linea.find('sn/')>=0 :
    #print ("Encontrado SINTAGMA NOMINAL");
    #Si la línea contiene un sintagma nominal,
    ini =linea.find('(')+1;
    fin =linea.find('-',ini,len(linea))-8;
    directo = linea[ini:fin];
    #print ("Encontrado SINTAGMA NOMINAL: "+ str(directo));
    # ya he encontrado el OD
    #Extraigo los sentidos
    finod =linea.find(')');
    senses = linea[fin:finod]
    pos = 0
    #print ("Sentidos: "+ str(senses));
    while senses.find(':0',pos,len(senses))>0 :
      sense=senses[pos-10:pos];
      #print ("Sentido: "+ str(sense));
      #Obtengo la info del sentido
      senseinfo = semantic.get_sense_info (sense);
      #Obtengo los sinonimos
      sinos= senseinfo.words;
      #for sino in sinos:
        #print ("sinonimo: " + sino)
      #Miro con cual de las productos se corresponde la accion extraida
      #Comparo todos los productos con todos los sinonimos
      cont=0;
      while producto_inferido=="" and cont<len(sinos):
        sino=sinos[cont]
        for p in productos:
          if p==sino:
            producto_inferido=p
            encontrado_producto=1
            #print ("Producto inferido: " +producto_inferido)
        cont=cont+1;
      cont=0;
      while producto_inferido=="" and cont<len(sinos):
        sino=sinos[cont]
        for p in productor_clave:
          if p==sino:
            producto_inferido="clave"
            encontrado_producto=1
            #print ("Producto inferido: " +producto_inferido)
        cont=cont+1;
      
      #Compruebo si aunque el sustantivo no se haya correspondido con ningún producto
      #se corresponde con los sustantivos de las acciones
      cont=0;
      while accion_inferida=="" and cont<len(sinos):
        sino=sinos[cont]
        for a in acciones_sustantivo:
          if a==sino:
            accion_inferida=a
            encontrado_producto=1
            #print ("Accion inferida: " +accion_inferida)
        cont=cont+1;
      pos = senses.find(':0',pos+2,len(senses));
      pos = senses.find(':0',pos+2,len(senses));


  ##Si la línea contiene un adjetivo
  elif linea.find('adj')>=0 and encontrado_producto==1 :
    #print ("Encontrado ADJETIVO ");
    ini =linea.find('(')+1;
    fin =linea.find('-',ini,len(linea))-8;
    directo = linea[ini:fin];
    find= directo.find(' ')
    parametros_inferidos = directo[:find]


  elif linea.find('espec')>=0 :
    if accion_inferida =="" :
      ##Si la línea contiene un determinante posesivo (etiqueta DP), la acción es CONSULTAR
      if(etimorfo.find('DP')>=0) :
        accion_inferida="consultar"

  #print("siguiente línea")
  linea=fichero.readline();
  contador_lineas=contador_lineas+1;

fichero.close()
print ( accion_inferida + " " + producto_inferido + " " + parametros_inferidos)
     
    
