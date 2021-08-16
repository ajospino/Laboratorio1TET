import socket, pickle, struct,os, colorama

class Cliente():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port 
        self.dicc = {}
     
    def iniciar_conexion(self):
        # Iniciar servicio
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.hostname, self.port))
        except Exception as e:
            print(e)
    
    def leer_comando(self):
        x = input('ingrese comando')
        self.dicc[1] = x
    
    def leer_archivo(self, path):
        file = open(path, 'rb')
        self.dicc['contenido'] = file.read()
        file.read()
        self.dicc['nombreArchivo'] = os.path.split(path)[1]
        file.close()
    
    def enviar_archivo(self):
        # Enviar datos al servidor
        # print("pasa por aca ")
        x = pickle.dumps(self.dicc)
        length = len(x)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(x)
        # print(self.recvall(1024))
        # print(respuesta)
       
    def recvall (self):
        msg = self.sock.recv(17520)
        msgg = pickle.loads(msg)
        print(colorama.Back.BLUE+colorama.Fore.RED+ msgg['mensaje']+colorama.Style.RESET_ALL)
        if(msgg['archivo'] != "no"):
            f = open(msgg['nombreArchivo'],'wb')
            f.write(msgg['archivo'])
            f.close()

    def recvallfile(self):
        
        msg = self.sock.recv(17520)
        msgg = pickle.loads(msg)
        print(colorama.Back.BLUE+colorama.Fore.RED+ msgg['mensaje']+colorama.Style.RESET_ALL)
        if(msgg['mensaje'] != (f"No existe el bucket {self.dicc['bucket']}")):
            for fichero in msgg['lista']:
                print(fichero)    

    def cerrar_conexion(self):
        self.sock.close()
                
    def inter_user(self):
        variable = 1;
        colorama.init()
        while(int(variable) < 7):
            print('Bienvenido a la central de control servidor-socket. En que le podemos ayudar hoy?''\n'+ '1)Crear bucket''\n' +'2)Eliminar un bucket''\n' +'3)Ver lista de todos los buckets''\n' +'4)Subir un archivo a un bucket''\n5)Eliminar un archivo de un bucket \n6)Listar archivos de un bucket\n7) Descargar un archivo\n8) Acabar con la conexion')
            variable= input()
            if(variable == '1'):
                self.dicc['comando'] = '1'
                self.dicc['bucket'] = input('Ingrese el nombre del nuevo bucket \n')
                self.enviar_archivo()
                self.recvall()
            if(variable == '2'):
                self.dicc['comando'] = '2'
                self.dicc['bucket'] = input('Ingrese el nombre del bucket a eliminar\n')
                self.enviar_archivo()
                self.recvall()
            if(variable == '3'):
                self.dicc['comando'] = '3'
                self.enviar_archivo()
                self.recvallfile()
            if(variable == '4'):
                self.dicc['comando'] = '4'
                path = input('Ingrese el path del archivo a subir \n')
                bucket = input('Ingrese el bucket(Carpeta) donde quiere que el archivo se suba \n')
                self.dicc['bucket'] = bucket
                self.leer_archivo(path)
                self.enviar_archivo()
                self.recvall()
            if(variable == '5'):
                self.dicc['comando'] = '5'
                bucket = input('Ingrese el bucket(Carpeta) de donde quiere eliminar el archivo \n')
                path = input('Ingrese el nombre del archivo a eliminar (con extension) \n')
                self.dicc['bucket'] = bucket
                self.dicc['nombreArchivo'] = path
                self.enviar_archivo()
                self.recvall()
            if(variable == '6'):
                self.dicc['comando'] = '6'
                bucket = input('Ingrese el nombre del bucket donde quiere listar los archivos \n')
                self.dicc['bucket'] = bucket
                self.enviar_archivo()
                self.recvallfile()
            if(variable == '7'):
                self.dicc['comando'] = '7'
                self.dicc['bucket'] = input('Ingrese el nombre del bucket donde quiere descargar el archivo \n')
                self.dicc['nombreArchivo'] = input('Ingrese el nombre del archivo que quiere descargar\n')
                self.enviar_archivo()
                self.recvall()

            if(variable == '8'):
                self.dicc['comando'] = '8'
                self.enviar_archivo()
                self.cerrar_conexion()

if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5050)
    c.iniciar_conexion()
    c.inter_user()
    c.cerrar_conexion()
