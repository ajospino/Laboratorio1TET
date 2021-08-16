import pickle, socket, multiprocessing, struct, os,shutil

class Server():

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.dicc = {}
        self.connected = True
        
    def iniciar_conexion(self):
        # Iniciar servicio 
        try:
            print('Escuchando')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.hostname, self.port))
            if(os.path.isdir('Buckets') == False):
                os.mkdir('Buckets')
            self.sock.listen(1)
        except Exception as e:
            print(e)
            
    def aceptar_conexion(self):
        # Aceptar solicitudes 
        while True:
            self.conn, self.addr = self.sock.accept()
            print('conectado con %r', self.addr)
            # Manejo de procesos mediante el uso de un while y el manejo de un metodo
            proceso = multiprocessing.Process(target= self.recibir_datos, args=())
            # proceso.daemon = True
            proceso.start()
            print('Nuevo proceso inciado %r', proceso)
    
    def crear_bucket(self,datos):
        
        if(os.path.isdir('Buckets/' + datos['bucket']) == False):
            self.dicc['mensaje'] = f" La carpeta {datos['bucket']} fue creada"
            
            os.mkdir('Buckets/' + datos['bucket'])
        else:
            self.dicc['mensaje'] =f"La carpeta {datos['bucket']} no fue creada, ya existe"
        self.enviar_archivo()

    #Eliminacion de buckets y archivos
    def eliminar_bucket(self,datos):
        nombre = 'Buckets/' + datos['bucket']
        shutil.rmtree(nombre)
        self.dicc['mensaje'] =f"el bucket {datos['bucket']} ha sido eliminado"
        self.enviar_archivo()
   

    def eliminar_archivo(self,datos):
        if(os.path.isfile('Buckets/' + datos['bucket'] +'/'+ datos['nombreArchivo'])== False):
            self.dicc['mensaje'] =f"El archivo {datos['nombreArchivo']} no existe"
        else:
            nombre = 'Buckets/' + datos['bucket']+'/' + datos['nombreArchivo']
            os.remove(nombre)
            self.dicc['mensaje'] =f"el archivo {datos['nombreArchivo']} ha sido eliminado"
        self.enviar_archivo()
    

    def enviar_archivo(self):
        message = pickle.dumps(self.dicc)
        self.conn.sendall(message)
            
    def recibir_datos(self):
        datos = ''
        while self.connected:
            try:
                # Recibir datos del cliente.
                lengthbuf = self.recvall(self.conn, 4)
                length, = struct.unpack('!I', lengthbuf)
                print("Si recibo datos")
                datos = self.recvall(self.conn, length)              
                # self.conn.sendall(b'Se han recibido los datos')    
                self.organizar_datos(datos)
            except Exception:
                self.connected = False
            
    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf
    
    def guardar_archivo(self,datos):

        if(os.path.isdir('Buckets/' + datos['bucket']) == False):
            os.mkdir('Buckets/' + datos['bucket'])
        file = open('Buckets/' + datos['bucket']+'/'+datos['nombreArchivo'],'wb')
        file.write(datos['contenido'])
        file.close()
        self.dicc['mensaje'] =f"El archivo {datos['nombreArchivo']} ha sido guardado"
        self.enviar_archivo()

    def listar_archivos(self,datos):
        if(os.path.isdir('Buckets/' + datos['bucket']) == False):
            self.dicc['mensaje'] = f"No existe el bucket {datos['bucket']}"
        else:
            self.dicc['lista'] = os.listdir('Buckets/' + datos['bucket'])
            self.dicc['mensaje'] = f"Esta es la lista de archivos dentro de {datos['bucket']}"
        self.enviar_archivo()

    def organizar_datos(self,x):
        print("Esperando comando")
        # swicth para llamara los metodos necesarios que envia el cliente
        self.dicc['lista'] = os.listdir('Buckets')
        self.dicc['mensaje'] = "Esta es la lista de buckets"
        self.dicc['archivo'] = "no"
        datos = pickle.loads(x)
        if(datos['comando'] == '1'):
            self.crear_bucket(datos)
       
        if(datos['comando'] == '2'):
            self.eliminar_bucket(datos)
       
        if(datos['comando'] == '3'):
            self.enviar_archivo()
       
        if(datos['comando'] == '4'):
            self.guardar_archivo(datos)
       
        if(datos['comando'] == '5'):
            self.eliminar_archivo(datos)
       
        if(datos['comando'] == '6'):
            self.listar_archivos(datos)

        if(datos['comando'] == '7'):
            print("7")
            self.enviar_descargable(datos)

        if(datos['comando'] == '8'):
            print("Se esta cerrando el servidor.")
            self.connected = False
        
    def cerrar_con(self):
        # Cerrar conexión
        self.sock.close()
    
if __name__ == "__main__":
 # Probar conexion entre cliente y socket  
    s = Server( hostname = 'localhost', port = 5050)
    s.iniciar_conexion()
    s.aceptar_conexion()
    for proceso in multiprocessing.active_children():
        print('Terminando proceso %r', proceso)
        proceso.terminate()
        proceso.join()
    print('Listo')  
