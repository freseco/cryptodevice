#******************************************************
#
# Métodos comunes para el resto del proyecto.
# Autor: freseco@gmail.com
#
#********************************************************

import urequests as requests   # Para realizar solicitudes HTTP
import json                    # Manipular archivos Json
import config
import ubinascii #para mostrar MAC adreess

def ObtenerCidudadFromIP(ip):
    
    url = f"https://ipapi.co/{ip}/city/"
    
    try:
        response = requests.request("GET", url)
        ciudad=response.text
        #print(f"(ObtenerCidudadFromIP) Ciudad: {ciudad}")        
        
        return ciudad
        
    except Exception as e:
        print(f"(ObtenerCidudadFromIP) Error al obtener la ciudad: {e}")
        #mostrarText("Error:",10,0,borrar=True,centrado=True)
#ObtenerCidudadFromIP
    
    
    
    
    
    


"""Llevar a Utils.py"""
def obtener_nombre_y_extension(ruta_archivo):
    # Obtener el nombre del archivo a partir de la ruta
    nombre_archivo = ruta_archivo.split('/')[-1]  # Divide la ruta y toma el último elemento
    # Separar el nombre del archivo y la extensión
    nombre, extension = nombre_archivo.rsplit('.', 1) if '.' in nombre_archivo else (nombre_archivo, '')
    return nombre, extension

def printMACaddress(sta_if):
    #obtenemos la mac address
    wlan_mac = sta_if.config('mac')
    config.MACaddress=ubinascii.hexlify(wlan_mac).decode()
    print(f"My mac Address: {config.MACaddress}")
    return macaddress

#Obtiene nuestra ip publica
def ObtenerPublicIP():
    url = "https://api.myip.com/"
    try:
        response = requests.request("GET", url)
        config.IPpublic = json.loads(response.text)
        print(f"(ObtenerPublicIP) Ip Public: {config.IPpublic['ip']}")
        print(f"(ObtenerPublicIP) Pais:      {config.IPpublic['country']}")
        
        return config.IPpublic
        
    except Exception as e:
        print(f"(ObtenerPublicIP) Error al obtener la ip publica: {e}")
        #mostrarText("Error:",10,0,borrar=True,centrado=True)
        #mostrarText(e,20,0,borrar=False,centrado=True)
#ip pública


#Porsche
def Obtenerprecioporsche():
    url = "https://freseco.net/personal/precio"
    try:
        response = requests.request("GET", url)
        precios = json.loads(response.text)
        config.porschecarvalue=precios
        
        #print(config.porschecarvalue)        
        
    except Exception as e:
        print(f"(Obtenerprecioporsche) Error al obtener precios porsche: {e}")
    

#Porsche





#Obtiene time from ip publica
def ObtenerTimePublicIP():
    url = f"https://timeapi.io/api/time/current/ip?ipAddress={config.IPpublic['ip']}"
    try:
        response = requests.request("GET", url)
        time = json.loads(response.text)
        #print(f"(ObtenerTimePublicIP) time: {time['date']}-{time['time']}")        
        
        
        
        return f"{time['day']}/{time['month']} {time['time']}" or ""
        
    except Exception as e:
        print(f"(ObtenerTimePublicIP) Error al obtener el tiempo de la ip publica: {e}")
        #mostrarText("Error:",10,0,borrar=True,centrado=True)
        #mostrarText(e,20,0,borrar=False,centrado=True)
#get time


#Formatea un número, poniendo punto a los miles y coma a los decimales.
def formatear_numero(numero):
    # Convertir el número a string con hasta 8 decimales
    partes = f"{numero:.8f}".split('.')
    entero = partes[0]
    decimal = partes[1] if len(partes) > 1 else None

    # Formatear la parte entera con puntos como separadores de miles
    entero_formateado = ""
    for i, digit in enumerate(reversed(entero)):
        if i > 0 and i % 3 == 0:
            entero_formateado = "." + entero_formateado
        entero_formateado = digit + entero_formateado

    # Unir la parte entera y decimal si existe
    if decimal is not None:
        # Eliminar ceros innecesarios en los decimales
        decimal = decimal.rstrip('0')
        if decimal:  # Solo añadir si hay decimales
            return f"{entero_formateado},{decimal}"
    return entero_formateado
#Formatear un número.

#Envia una notificación por pushOver.net
def sendNotification(texto="",titulo="SP32"):
    
    url="https://api.pushover.net/1/messages.json"
    #print(f"texto notificación: {texto}")
    mydata = {
        "token": config.tokenPush,
        "user": config.userPush,
        "message": texto,
        "title":titulo,
        "ttl":300,            #caducidad de la notificación
        "html":1,
        "sound":"none"        #"cashregister" #"vibrate" #
      }
    try:
        x = requests.post(url, json=mydata)
    except Exception as e:
        print(f"Error al enviar notificación: {e}")
    
    """
    Ejemplo devuelto: {
                        "status":1,
                        "request":"d22f94c0-40fc-466f-ad51-9eaa952705bf"
                        }
    """
    
    #print(f"respuesta pushover:{x.text}")
#Enviar notificación


#Obtiene la información meteorologica de la AEMET. problema con el formato de los datos en iso, pero solo se puede leer utf-8
def ObtenerWeather():
    madrid="28079"
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{madrid}/?api_key={config.api_key}"
   
    headers = {
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)
    
    # Convertir la cadena JSON a un diccionario de Python
    datosMeteo = json.loads(response.text)   
    
    print(f"Datos meteorologicos: {datosMeteo}")
    if int(datosMeteo["estado"])==200:
        url=datosMeteo["datos"]#url con los datos meteorologicos.
        
        datosMeteoMunicipio=requests.request("GET",url)     
        
        print("")
        print((datosMeteoMunicipio.__dict__))
        print("")
        print(str(bytes(datosMeteoMunicipio.content,'utf-8').replace(b'\n', b'')))
        print("")
        #print(f"Datos meteorológicos: {response.text}")