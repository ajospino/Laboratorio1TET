import os,socket

CHUNKSIZE = 1_000_000
class Node():

    def __init__(self,hostname,port): #Inicializacion del Cliente
        self.hostname = hostname
        self.port = port

    def init_conec(self):#Inicio de conexion servidor cliente
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname,self.port))
        print(self.sock)
        
# Make a directory for the received files.

    def rec_dir(self):#Recibe la carpeta Buckets del servidor y la replica para ser examinada con la carpeta local
        os.makedirs('Buckets2',exist_ok=True)
        print(self.sock)
        with self.sock,self.sock.makefile('rb') as clientfile:
            while True:
                
                raw = clientfile.readline()
                
                if not raw: break # no more files, server closed connection.

                filename = raw.strip().decode()
                length = int(clientfile.readline())
                print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

                path = os.path.join('client',filename)
                os.makedirs(os.path.dirname(path),exist_ok=True)

                # Read the data in chunks so it can handle large files.
                with open(path,'wb') as f:
                    while length:
                        chunk = min(length,CHUNKSIZE)
                        data = clientfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
                    else: # only runs if while doesn't break and length==0
                        print('Complete')
                        continue

                # socket was closed early.
                print('Incomplete')
                break 

    def send_dir(self):
        slf = True
        print("Entro send dir")
        
        while slf:
            
            with self.sock:
                for path,dirs,files in os.walk('client'):
                    for file in files:
                        filename = os.path.join(path,file)
                        relpath = os.path.relpath(filename,'client')
                        filesize = os.path.getsize(filename)

                        print(f'Sending {relpath}')

                        with open(filename,'rb') as f:
                            self.sock.sendall(relpath.encode() + b'\n')
                            self.sock.sendall(str(filesize).encode() + b'\n')

                            # Send the file in chunks so large files can be handled.
                            while True:
                                data = f.read(CHUNKSIZE)
                                if not data: break
                                self.sock.sendall(data)
                print('Done.')
                slf = False

                
def main():
    node= Node("localhost",5050)
    a = input("Ingrese el numero")
    
    node.init_conec()
    # if a == "1":
    #     node.rec_dir()
    # else:
    #     node.send_dir()
    node.rec_dir()
    # node.send_dir()
if __name__ == "__main__":
    main()