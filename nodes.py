from os import error, system


class Nodo():

    def __init__(self,dato,siguiente = None):
        self.dato = dato
        self.siguiente = siguiente


n1 = Nodo({})
o = 2


def ver_lengh(key):
    global n1
    nodo = n1
    
    while nodo != None:
        num = len(nodo.dato)
        print(nodo.siguiente)
        if key in nodo.dato:
            if nodo.siguiente == None:
                print("entre 1")
                return True
            else:
                    nodo = nodo.siguiente
        else:
            no1 = nodo
            nres = nodo
            while no1 != None:
                if(no1.siguiente != None and num >= len(no1.siguiente.dato)):
                    if key in nodo.siguiente.dato:
                        return nodo
                else:
                     nodo = nodo.siguiente

            if  nodo.siguiente != None and num >= len(nodo.siguiente.dato):
                
            return nodo
    

    

def crear_nodo(vare,key,valor):
    global o
    name  = "n" + str(vare)
    var2 = o - 1
    
    name_b = "n" + str(var2)
    
    print(ver_lengh(key))
    if ver_lengh(key) == True:
        globals()[name] = Nodo({},None)
        globals()[name_b].siguiente = globals()[name]
        
        o = o+1
        
    agregar_valor(ver_lengh(key),key,valor)
    







def agregar_valor(nodo,key,valor):
    
    nodo.dato[key] = valor
    noss = n1 
    while noss != None:
        print(noss.dato)
        noss = noss.siguiente

def recorrer():
    global o
    key = ""
    value = ""
    while key == "":
        key = input("Ingrese la key\n")
        if key == "":
            print("Ingrese una key valida\n")
    while value == "":
        value = input("Ingrese la value\n")
        if value == "":
            print("Ingrese un value valida\n")
    
    if len(n1.dato) == 0:
        agregar_valor(n1,key,value)
    else:
        crear_nodo(o,key,value)
    
    # Key is not present
            
       

def quest():
    global o
    print(len(n1.dato))
    valor = input("Ingrese exit para salir o unda enter para continuar:\n")
    while valor != "exit":
        recorrer()
      
        valor = input("Ingrese exit para salir o unda enter para continuar:\n")
      


def main():
    quest()


if __name__ == "__main__":
    main()
