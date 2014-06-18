import os 
## Direcorio de instalación del API de python de freeling
directoriofreeling= (os.environ ['FREELING_PYTHON'] )
directorio = directoriofreeling +"/APIs/python"
import sys
sys.path.append( directorio  )
import freeling
import subprocess
import simplejson as json


DATA = directoriofreeling +"/data";
LANG="/es";
freeling.util_init_locale("default");
#Semantic Database Module
semantic = freeling.semanticDB (DATA + LANG +"/semdb.dat");

#Conjunto de ACCIONES
acciones = ['consultar', 'realizar', 'ayuda', 'devolver', 'pagar', 'modificar' ]
#acciones_sinonimos = ['consultar','ejecutar','realizar','causar','crear','hacer','realizar','organizar','realizar','efectuar','cumplir',' modificar','alterar','cambiar','','alterar','arreglar','pagar','avalar','subvencionar','abonar','liquidar','costear','dar','devengar','rendir','compensar','enmendarse',
#'expiar','ayudar','auxiliar','asistir','devolver','reponer','llevar_de_regreso','regresar','traer_de_regreso','reembolsar','volver_a_pagar','reembolsar']

#Conjunto de PRODUCTOS
productos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo' , 'contraseña', 'seguro']
productos_sinonimos = ['transferencia', 'tarjeta', 'movimiento' , 'recibo' , 'contraseña' ,'transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];
acciones_transferencia= ['transferir','transportar','trasladar','transferir','transportar','trasladar','transferir','transferir','pasar','transferir','pasar','transferir','transmitir','transferir','transmitir','entregar','presentar','transferir','traspasar','transferir'];


#Recupero el parámetro de entrada
entrada = sys.argv[1]
#print (" entrada " +entrada)
intencion= entrada.split("|");


# ANALIZO LA ACCION DE LA INTENCIÓN
accion= intencion[0].lower()
command= "echo \"" + "Yo voy a " +accion + "." + "\" | analyzer_client localhost:50006 "
respuesta = subprocess.check_output(command, shell=True)
r= str(respuesta)
respuesta=respuesta.decode("utf-8")
respuesta=respuesta.split('\n')
respuesta=respuesta[3]

inisen =respuesta.find('-')-8;
finsen =respuesta.find(')')-1
sentidosaccion = respuesta[inisen:finsen];
#print ("sentidosaccion: "+ sentidosaccion);
sentidosaccion=sentidosaccion.split(':0/')
sentidosproducto=""
producto_inferido=""
accion_inferida=""

contsen=0
while accion_inferida=="" and contsen<len(sentidosaccion):
  sen  = sentidosaccion[contsen]
  #print ("Sentido: "+ sen)
  #Obtengo la info del sentido
  senseinfo = semantic.get_sense_info (sen)
  #Obtengo los SINONIMOS
  sinos= senseinfo.words;
  #for sino in sinos:
    #print ("  sinonimo: " + sino)
  #Miro con cual de las acciones se corresponde la accion extraida
  #Comparo todas las acciones con todos los sinonimos
  contsin=0;
  while accion_inferida=="" and contsin<len(sinos):
    sino=sinos[contsin]
    for a in acciones:
      if a==sino:
        accion_inferida=a
        #print ("Accion inferida: " +accion_inferida)

    #Si no he encontrado una accion asociada, busco en las acciones sinonimos de transferencias
    contactra=0
    if accion_inferida=="":
      while producto_inferido=="" and contactra<len(acciones_transferencia):
        t=acciones_transferencia[contactra]
        if t==sino:
            producto_inferido="transferencia"
            #print ("Producto inferido: " + producto_inferido)
        contactra=contactra+1

    contsin=contsin+1

  contsen=contsen+1


# ANALIZO EL PRODUCTO DE LA INTENCIÓN
producto= intencion[1].lower()

#Compruebo si es plural
command= "echo \"" + producto + "." + "\" | analyzer_client localhost:50006 "
respuesta = subprocess.check_output(command, shell=True)
respuesta=respuesta.decode("utf-8")
respuesta=respuesta.split('\n')[0]
#print("respuestas " +respuesta)
if(respuesta.find('NCFP000')>=0):
  #print("entro " +producto[:len(producto)-2] )
  command= "echo \"" + producto[:len(producto)-2] + "." + "\" | analyzer_client localhost:50006 "
  respuesta = subprocess.check_output(command, shell=True)
  respuesta=respuesta.decode("utf-8")
  respuesta=respuesta.split('\n')[0]
  #print ("respuesta: "+ respuesta);
  inisen =respuesta.find('-')-8;
  finsen =respuesta.find(')')-1 ;
  sentidosproducto = respuesta[inisen:finsen];
  #print ("sentidosproducto: "+ sentidosproducto);
  sentidosproducto=sentidosproducto.split(':0/');
  if(sentidosproducto==""):
    command= "echo \"" + producto[:len(producto)-3] + "." + "\" | analyzer_client localhost:50006 "
    respuesta = subprocess.check_output(command, shell=True)
    r= str(respuesta)
    respuesta=respuesta.decode("utf-8")
    #print ("respuesta: "+ respuesta);
    inisen =respuesta.find('-')-8;
    finsen =respuesta.find(')')-1 ;
    sentidosproducto = respuesta[inisen:finsen];
    #print ("sentidosproducto: "+ sentidosproducto);
    sentidosproducto=sentidosproducto.split(':0/');
else:
  command= "echo \"" + producto + "." + "\" | analyzer_client localhost:50006 "
  respuesta = subprocess.check_output(command, shell=True)
  r= str(respuesta)
  respuesta=respuesta.decode("utf-8")
  #print ("respuesta: "+ respuesta);
  inisen =respuesta.find('-')-8;
  finsen =respuesta.find(')')-1 ;
  sentidosproducto = respuesta[inisen:finsen];
  #print ("sentidosproducto: "+ sentidosproducto);
  sentidosproducto=sentidosproducto.split(':0/');


contsen=0
while producto_inferido=="" and contsen<len(sentidosproducto):
  sen  = sentidosproducto[contsen]
  #print ("Sentido: "+ sen)
  #Obtengo la info del sentido
  senseinfo = semantic.get_sense_info (sen)
  #Obtengo los SINONIMOS
  sinos= senseinfo.words;
  #for sino in sinos:
    #print ("  sinonimo: " + sino)
  #Miro con cual de las acciones se corresponde la accion extraida
  #Comparo todas las acciones con todos los sinonimos
  contsin=0;
  while producto_inferido=="" and contsin<len(sinos):
    sino=sinos[contsin]
    for a in productos:
      if a==sino:
        producto_inferido=a
        #print ("Producto inferido: " + producto_inferido)

#Extraigo los parámetros, pero no hago nada con ellos
parametros=intencion[2].lower().replace(' ' ,'')


resultado = json.dumps({"accions" :accion_inferida, "producto": producto_inferido, "parametro": parametros} );
print (resultado)