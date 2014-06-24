INTENCIÓN BBVA
==============

Módulo desarrollado en Python para la extracción de la intención de un usuario, es decir cual de las acciones disponibles en la Web del BBVA desea llevar a cabo.


Extracción de  intención
-------------------------

Análisis de las distintas partes de la oración para extraer la acción, producto y parámetros, asociados a la intención del usuario.
Para la obtención de la intención del usuario, se utiliza el análisis sintáctico realizado por Freeling. 

La acción sera el verbo principal identificado en la oración. También se puede identificar como acción un adverbio o adjetivo identificado como la parte principal de la oración.
El producto se asociará al sustantivo principal de la oración.
Los parámetros de la intención pueden ser el adjetivo, sintagma preposicional o sintagma nominal, que acompañan al sustantivo principal de la oración.


Proyección intención BBVA
-------------------------

A partir de la acción, producto y parámetros recuperados con el script anterior, se intenta obtener cual de las acciones disponibles en la web del BBVA es la que desea llevar a cabo el usuario.
Para proyectar la intención del usuario en las acciones del BBVA se compara el conjunto de sinónimos asociados a la acción/producto obtenido, con el conjunto de sinónimos asociados a las distintas acciones/productos disponibles en la Web de BBVA.
Para la obtención de los sinónimos de las distintas palabras se utiliza el modulo de Freeling 'Semantic Database Module'

En caso de  haber identificado el producto pero no la acción, las respuesta del sistema consistirá en un conjunto de intenciones con distintas probabilidades asociadas. Básicamente, se devolverá un intención por cada acción disponible para dicho producto. Las probabilidades asociada a cada acción del producto, se modificarán en función de al verificación de la intención real del usuario. Para ello será necesario la construcción de un módulo que reciba el par acción/producto llevado a acabo por el usuario y actualice la probabilidad correspondiente.

Instalación
-----------

Para la ejecución de este módulo es necesario:
- Instalar 'Freeling'
- Instalar la API para Python que incluye (versión 3.1 o superior)
- Definir la variable de entorno FREELING_PYTHON para que contenga el directorio de instalación de Freeling (ejecutar vi /etc/environment para crear la variable de entorno)
- Levantar el servidor de freeling para análisis morfológico: analyze -f es.cfg --outf tagged  –sense all --server --port 50006

