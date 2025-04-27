# Refac_Microservicio
Propuestas de refactorización para el proyecto de microservicios implementando Docker y Flask

## Propuesta 01 Compatibilidad de Versiones

Al ejecutar el proyecto de microservicios empleando Docker y Flask por primera vez, se encontraron diversos problemas en la ejecución del mismo. Uno de estos problemas fue la compatibilidad de versiones de las librerías utilizadas. Puesto que al ejecutar el proyecto se mostraba en pantalla que no era posible importar dichas librerías. 

Para resolver el problema se modificó el archivo requirements.pip (encargado de especificar las dependencias de Python a emplear), actualizando las versiones de la librerías empleadas.

## Propuesta 02 Implementación de Traefik

Al analizar el estado inicial del proyecto se detectó que no contaba con un enrutamiento centralizado, lo que obliga tanto al desarrollador como al cliente conocer en que puerto se haya cada servicio. Además, no contaba con una forma integrada de distribuir el tráfico.

Para solucionar dicho problema se implementó la tecnología de Traefik. Siendo Traefik una herramienta que facilita el despliegue de microservicios. Lo que facilita el enrutamiento, puesto que todas las peticiones pasan por una ruta central. También se debe tomar en cuenta que es muy fácil de utilizar puesto que reconoce cada uno de los contenedores de nuestra aplicación y los enruta automáticamente.
