import socket, pickle, struct,os, colorama

class Cliente():
    
    def __init__(self):
        self.hostname = '172.31.62.214'
        self.port = 5050 
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
        while(int(variable) < 4):
            print('Bienvenido a la central de control servidor-socket. En que le podemos ayudar hoy?''\n'+ '1)Crear bucket''\n' +'2)Eliminar un bucket''\n' +'3)Ver lista de todos los buckets''\n' +'4)Acabar con la conexión')
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
                self.dicc['bucket'] = " "
                self.enviar_archivo()
                self.recvallfile()
            if(variable == '4'):
                self.dicc['comando'] = '4'
                self.enviar_archivo()
                self.cerrar_conexion()

if __name__ == "__main__":
    c = Cliente()
    c.iniciar_conexion()
    c.inter_user()
    c.cerrar_conexion()
