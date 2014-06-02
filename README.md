ExtraerIntencion
================

Instalación
-----------

Script para la extracción de la intención de un usuario a partir del análisis sintáctico realizado por Freeling.
Para la ejecución de este script es necesario instalar 'Freeling', instalar la API para Python que incluye (versión 3.1 o superior) y definir la variable de entorno FREELING_PYTHON para que contenga el directorio de instalación de Freeling (ejecutar vi /etc/environment para crear la variable de entorno)


Funcionamiento
--------------

El script intencion.py analiza el resultado de ejecutar el análisis sintáctico de freeling sobre la cadena de texto, para extraer la intención del usuario. Lleva a cabo dos funciones:

- Obtención Acción y Producto
Análisis de las distintas partes de la oración para extraer la acción, producto y parámetros, asociados a la intención del usuario.
Para obtener la acción se busca la palabra con la etiqueta 'grup-verb'. Para la obtención del producto se busca la palabra con etiqueta 'sn' y también se buscan los verbos asociados con los distintos productos ( como por ejemplo de transferencia, transferir). Adicionalmente se extraen otros parámetros: el objeto indirecto que identifica a quien va dirigida la acción o los adjetivos asociados al producto extraido.

- Explorar sinónimos
Para comprobar si la acción/producto extraído, se corresponden con alguna accion/producto  del BBVA, se extraen los sinónimos tanto de la acción/producto extraido como del conjunto de acciones/produtos de BBVA. Para la obtención de los sinónimos de las distintas palabras se utiliza el modulo de Freeling 'Semantic Database Module'
