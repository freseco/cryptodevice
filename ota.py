import network
import ubinascii #para mostrar MAC adreess
import urequests
import os
import gc
import json
import ujson
import machine
from time import sleep
from version import Version
import utils
import config


"""
This class handles OTA updates.
It checks for updates,
downloads and installs them, reseting devices.
"""
   
class OTAUpdater:       
    
    
    def __init__(self):                
        
        self.versiones=Version()
        
        self.resetear=False 
        
        #si hay un versiones.json para nosotros, añadimos la mac en la url de actualizacion
        self.check_for_myversionesJson()
                
        #Descarga los ficheros actualizados.        
        self.check_for_updates()
        
        
        if self.resetear:
            # Restart the device to run the new code.
            print('Restarting device...')
            machine.reset()  # Reset the device to run the new code.
          
        
    """
    Crea la url y descarga el fichero en  self.latest_code
    """
    def fetch_latest_file(self,filename)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        gc.collect()
        
        #Creamos la url del fichero que vamos a comprobar la version, sin extension
        urlfilename = updates_url +self.macInAddress+ filename
        print(f"URL para fetch file: {urlfilename}")
        
        # Fetch the latest code from the repo.
        response = urequests.get(urlfilename)
        
        #print(f"fetch file: {response.text}")
        print(f'Status code: {response.status_code}.')
        
        if response.status_code == 200:
            #print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
    
            # Save the fetched code to memory
            self.latest_code = response.text
            return True
        
        elif response.status_code == 404:
            print(f'file not found on server: {urlfilename}.')
            return False
        else:
            print(f'Status code: {response.status_code}.')
            return False
    """
    Crea un fichero auxiliar con el descargado, para luego renombrarlo por el que hay
    que actualizar.
    """
    def update_file(self,filename):
        """ Update the code without resetting the device."""

        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)    
               
        # free up some memory
        self.latest_code = None

        # Overwrite the old code. Changing the file extension _ for .
        os.rename('latest_code.py', filename.replace("_","."))
        
        
     
        

        """ Check if updates are available."""       
    def check_for_updates(self):  

        #Creamos la url del fichero de versiones en el servidor
        self.version_url_server = config.updates_url +self.macInAddress+ self.versiones.FileNameVersiones() 

        response = urequests.get(self.version_url_server)
        
        if response.status_code != 200:
            print("No existe fichero versiones.json, para actualizar en el servidor:", response.status_code)
            return False 
        
        data = ujson.loads(response.text)
        
        #Si no coinciden los versiones.json local y server
        diferenteVersionfile=False
        
        #recorremos las claves del fichero versiones.json en el servidor                
        for claveServer in data:
            try:
            
                #comparamos las versiones de las claves, que son los nombre de ficheros sin extension
                if data[claveServer]>self.versiones.GetVersion(claveServer):
                    print(f"Versión diferente: {claveServer} Local:{self.versiones.GetVersion(claveServer)} Server:{data[claveServer]}")
                    if self.fetch_latest_file(claveServer):
                        self.update_file(claveServer)                 
                        self.versiones.SetVersion(claveServer,data[claveServer])
                        self.resetear=True
            except KeyError:
                diferenteVersionfile=True
                print(f"Fichero {self.versiones.FileNameVersiones} es diferente entre local y server!")

        if diferenteVersionfile:
            #actualizar versiones.json local con la del servidor.
            with open('versiones.json', 'w') as f:
                f.write(response.text)



        """ Check if There are updates for mine.Adding my mac address to the url."""       
    def check_for_myversionesJson(self):  

        #Creamos la url del fichero de versiones en el servidor
        self.version_url_server = config.updates_url +config.MACaddress+ '/' +self.versiones.FileNameVersiones() 
        #print(f"URL de mi versiones.json {self.version_url_server}")
        response = urequests.get(self.version_url_server)
        
        if response.status_code == 200:
            print("Existe fichero versiones.json mi, me actualizo del servidor:", response.status_code)
            self.macInAddress= self.macAddress + "/"
        else:
            print("No existe fichero versiones.json para mi. Actualización normal.", response.status_code)
            self.macInAddress= ""
        
        gc.collect()
