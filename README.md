# Laboratorio 1
### Uso de la aplicacion: ###
Servidor:
`python3 Servidor.py`
Este esperara conexiones desde `Cliente.py` y despues las solicitudes que estos hagan.

Cliente:
`python3 Cliente.py`
Este se conectara al `Servidor.py` y enviara solicitudes basadas en el menu que se ve en pantalla al ejecutar el archivo.
Se puede crear, eliminar y listar Buckets (carpetas), la cuarta opcion eliminara la conexion del cliente con el servidor, cerrando el socket pero no el cliente.
