import os
import json

"""
Las versiones de los ficheros, estan almacenadas en el fichero "versiones.json".
Cada clave es el nombre con guion bajo y la extension(sin punto), del fichero, y su valor, es el número
que representa la version.

Clave:     
        filename.ext -> filename_ext


Funcionalidades:
, lee el fichero,
obtiene la version de un fichero,
devuelve el nombre del fichero json,
y puede modificarlo.

Ejm:

versiones=Version()

versionactual=versiones.GetVersion('version')
print(f"version en el fichero: {versionactual}")

versiones.SetVersion("main.py",3)

"""

class Version:
    
    def __init__(self):
        
        self.fileVersiones='versiones.json'
        
        try:
            with open(self.fileVersiones, 'r') as f:
                self.versiones = json.load(f)
        except OSError:        
            print(f"No existe fichero {self.fileVersiones} en local, lo creamos.")
            self.versiones = {}  # Crear un diccionario vacío si el archivo no existe
            with open(self.fileVersiones, 'w') as f:
                json.dump(self.versiones, f)
        
    
    """
        Obtiene el valor de version de una clave, en este caso, nombre fichero con guion bajo en vez de punto.
        
        filename.ext -> filename_ext
        
        return:
            -1 clave no encontrada,
            [0,..] version fichero.
    """
    def GetVersion(self,clave):
        try:
            #print(f"Clave solicitada: {clave}")
            return int(self.versiones[clave])
        except KeyError:
            print(f"Clave no encontrada: {clave}")
            return -1


    """
        Guarda el valor de la clave indicada en el fichero de versiones.
        Sirve para actualizar el número de version.
        
        Clave: texto con el nombre del fichero.
        newversionvalor: Entero indicando el nuevo valor de la versión.
    """
    def SetVersion(self,clave,newversionvalor):
        self.versiones[clave]=newversionvalor
        # Guardar los cambios en el fichero.
        with open(self.fileVersiones, 'w') as f:
            json.dump(self.versiones, f)

    def FileNameVersiones(self):
        return self.fileVersiones