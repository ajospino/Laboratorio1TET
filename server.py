import os,socket,struct,multiprocessing

CHUNKSIZE = 1_000_000
class Centralnode():

    def __init__(self,hostname,port):
        self.hostname = hostname
        self.port = port
        self.connected = True

    def init_conec(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.hostname,self.port))
        self.sock.listen(1)
        self.accept_conex()
        
    def accept_conex(self):
        print('Waiting for a client...')
        self.client,self.claddress = self.sock.accept()


    def send_dir(self):
        slf = True
        while slf:
            
            
            
            print("Connected with %r",self.claddress)
            print(f'Client joined from {self.claddress}')
            with self.client:
                for path,dirs,files in os.walk('Buckets'):
                    for file in files:
                        filename = os.path.join(path,file)
                        relpath = os.path.relpath(filename,'Buckets')
                        filesize = os.path.getsize(filename)

                        print(f'Sending {relpath}')

                        with open(filename,'rb') as f:
                            self.client.sendall(relpath.encode() + b'\n')
                            self.client.sendall(str(filesize).encode() + b'\n')

                            # Send the file in chunks so large files can be handled.
                            while True:
                                data = f.read(CHUNKSIZE)
                                if not data: break
                                self.client.sendall(data)
                print('Done.')
                slf = False
                
    def recibir_datos(self):
        os.makedirs('client',exist_ok=True)
        print("Searching for data")
        client,address = self.sock.accept()
        datos = ''
        with client,client.makefile('rb') as clientfile:
            
            while True:
                
                raw = clientfile.readline()
                print(raw)
                if not raw: break # no more files, server closed connection.

                filename = raw.strip().decode()
                print("Entro en el while true")
                length = int(clientfile.readline())
                print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='')

                path = os.path.join('client',filename)
                os.makedirs(os.path.dirname(path),exist_ok=True)

                # Read the data in chunks so it can handle large files.
                with open(path,'wb') as f:
                    while length:
                        chunk = min(length,CHUNKSIZE)
                        data = clientfile.read(chunk)
                        if not data: print('no data')
                        f.write(data)
                        length -= len(data)
                    else: # only runs if while doesn't break and length==0
                        print('Complete')
                        continue
        

def main():
    CentralNode= Centralnode("localhost",5050)
    CentralNode.init_conec()
    # server.send_dir()
    # server.recibir_datos()

if __name__ == "__main__":
    main()