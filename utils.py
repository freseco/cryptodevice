#******************************************************
#
# Métodos comunes para el resto del proyecto.
# Autor: freseco@gmail.com
#
#********************************************************

import urequests as requests   # Para realizar solicitudes HTTP
import json                    # Manipular archivos Json
import config


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
def sendNotification(texto=""):
    
    url="https://api.pushover.net/1/messages.json"
    
    mydata = {
        "token": config.tokenPush,
        "user": config.userPush,
        "message": texto,
        "title":"SP32",
        "sound":"cashregister" #vibrate #None
      }
    
    x = requests.post(url, json=mydata)
    
    """
    Ejemplo devuelto: {
                        "status":1,
                        "request":"d22f94c0-40fc-466f-ad51-9eaa952705bf"
                        }
    """
    
    print(x.text)
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