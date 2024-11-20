import network,time
from machine import Pin, SPI, I2C
#from ssd1306 import SSD1306_I2C    #pantalla pequeña
from sh1106  import SH1106_I2C      #pantalla grande
import gc       # Para recolección de basura
import urequests as requests   # Para realizar solicitudes HTTP
import json                    # Manipular archivos Json
import config
import wifimgr  #Web service para configurar la wifi.
import utils
import framebuf
import sys

# Limpiar la memoria
gc.collect()


#-------Inicializamos la pantalla---------
i2c = I2C(0,scl=Pin(22),sda=Pin(21))
#oled_sh= SSD1306_I2C(128,64,i2c)          #pantalla pequeña
oled_sh= SH1106_I2C(128,64,i2c,rotate=180) #pantalla grande
#-----------------------------------------



coin_info = {"coins": ["bitcoin", "ethereum", "solana", "cardano","the-graph","stellar"],
             "coin_vs": config.moneda,
             "include_market_cap": False,
             "include_24hr_change": False,
             "include_24hr_vol": False,
             }

maxvaluecoin={
    "bitcoin"  :0.0,
    "ethereum" :0.0,
    "solana"   :0.0,
    "cardano"  :0.0,
    "the-graph":0.0,
    "stellar"  :0.0
    }


#Configuramos el pin GPIO donde esta el led del sp32
pin_led=Pin(2,Pin.OUT)

def encender_led():
    pin_led.value(1)

def apagar_led():
    pin_led.value(0)
#Led de la placa
    


    


def infoIcon(nombre):
    with open(f"icons/{nombre}.pbm","rb") as file:
        file.readline()
        xy=file.readline()
        ancho= int(xy.split()[0])
        alto = int(xy.split()[1])
        icon = bytearray(file.read())
        
        icon_array=framebuf.FrameBuffer(icon,ancho,alto,framebuf.MONO_HLSB)
        
    return [ancho,alto,icon_array]



#Escribe texto en la pantalla:
# centrado: Indica si hay que centrar horizontalmente el texto en la pantalla.
# borrar:   Indica si hay que borrar la pantalla antes de escribir
def mostrarText(texto,columna,fila,centrado=False,borrar=False):
    
    desplazamiento=0
    
    if centrado==True:
        longitud = len(texto)
        libre    = (16-longitud)*8
        desplazamiento=int(libre/2)
    
    
    global oled_sh
    
    if borrar==True:
        oled_sh.fill(0)#borra la pantalla
        oled_sh.show() #ejecuta la acción en la pantalla
    
    oled_sh.text(texto,desplazamiento+fila,columna)
    oled_sh.show()






#Obtiene los valores de las criptomonedas
def fetch_api_simple_price(coin_info_list: dict):

    url_base= config.URL_BASE
    api_key = config.API_KEY

    timeout=15

    # Encabezados de la solicitud con la clave API
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key
               }

    # URL base para este tipo de splicitud
    url = url_base + "/simple/price?ids="

    # Agrega las monedas a consultar
    for index, coin in enumerate(coin_info_list['coins']):
        if index == 0:
            url += coin.lower()
        else:
            url += f'%2C{coin.lower()}'

    # Incluye la comparación (Por el momento solo admite una comparación)
    url += f'&vs_currencies={coin_info_list["coin_vs"].lower()}'

    parameters = coin_info_list.items()

    for key, value in parameters:
        if isinstance(value, bool):
            if value:
                url += f'&{key}={str(value).lower()}'

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('Error en la solicitud. Código de respuesta HTTP:',
                  response.status_code)
            return None

    except Exception as e:
        print('Error en la solicitud:', str(e))
        return None

#si el valor de la moneda, es un máximo, lo guardamos y enviamos notificación.
def encontrarmaximode(moneda,valor):
    #print(f"valor: {valor}")
    if float(valor)>maxvaluecoin[moneda]:
        print(f"máximo: {valor}>{maxvaluecoin[moneda]}")
        maxvaluecoin[moneda]=float(valor)
        texto=f"Máximo para {moneda}:{valor}"
        print(texto)
        utils.sendNotification(f"Maximo: {valor} %E2%82%AC",f"{moneda}")
        return True
            




#Intentamos conectarnos a una wifi conocida o crea un AP.
wlan = wifimgr.get_connection(oled_sh,infoIcon("qrcode")[2])

if wlan is not None:
    wifi=wlan.ifconfig()
    print(f"Datos de la red (IP/netmask/gw/DNS):{wifi}")
    mostrarText("Connected!",00,0,centrado=True,borrar=True)
    
    mostrarText("IP:",10,0)
    mostrarText(wifi[0],20,0,centrado=True)
    
    mostrarText("DNS:",30,0)
    mostrarText(wifi[3],39,0,centrado=True)
    
    #mostrarText("Gateway:",42,0)
    #mostrarText(wifi[2],50,0)
    publicIP = utils.ObtenerPublicIP()
    mostrarText("Ip public:",48,0)
    mostrarText(publicIP['ip'],56,0,centrado=True)
    
    #utils.sendNotification("ESP32 conectado!")
    
    #Desplazamiento pantalla
    for i in range(0,64):
        oled_sh.scroll(0,-1)
        oled_sh.show()
        encender_led()
        time.sleep(0.02)
        apagar_led()
        
        
    
    #ObtenerWeather() #falta formatear los datos devueltos.
    
    
    textoinfo=f"Moneda: {config.moneda}"
    
    while True:
        encender_led()
        valores = fetch_api_simple_price(coin_info)
        
        
        if valores is None:
            textoinfo=f"No actualizado"
            time.sleep(30) #esperamos un minuto.
            continue
        else:
            textoinfo=f"Moneda: {config.moneda}"
            data=valores
            
# Imprimir la respuesta en pantalla
        
        mostrarText(   f"BTC:",0,0,borrar=True)
        value=data['bitcoin'][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode("bitcoin",value) else ""            
        mostrarText(f"{alcanzado}{valor}",0,47)       
        
        
        
        mostrarText(f"ADA:",10,0)
        value=data['cardano'  ][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode("cardano",value) else ""
        mostrarText(f"{alcanzado}{valor}",10,47)
        
        mostrarText(f"ETH:",20,0)
        value=data['ethereum'  ][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode("ethereum",value) else ""
        mostrarText(f"{alcanzado}{valor}",20,47)
        
        mostrarText(f"SOL:",30,0)
        value=data['solana'  ][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode("solana",value) else ""
        mostrarText(f"{alcanzado}{valor}",30,47)
        
        mostrarText(f"GRT:",40,0)
        value=data['the-graph'  ][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode('the-graph',value)  else ""
        mostrarText(f"{alcanzado}{valor}",40,47)
        
        mostrarText(f"XLM:",50,0)
        value=data['stellar'  ][config.moneda]
        valor=utils.formatear_numero(value)        
        alcanzado=">" if encontrarmaximode("stellar",value) else ""
        mostrarText(f"{alcanzado}{valor}",50,47)

        mostrarText(textoinfo,57,0,centrado=True)

        # Imprimir la respuesta en consola
        print(f"Bitcoin:   {utils.formatear_numero(data['bitcoin']['eur'])} €")
        print(f"Cardano:   {utils.formatear_numero(data['cardano']['eur'])} €")
        print(f"Ethereum:  {utils.formatear_numero(data['ethereum']['eur'])} €")
        print(f"Solana:    {utils.formatear_numero(data['solana']['eur'])} €")
        print(f"the-graph: {utils.formatear_numero(data['the-graph']['eur'])} €")
        print(f"XLM:       {utils.formatear_numero(data['stellar']['eur'])} €")
        print(f"------------------------------------------------------------------")
        apagar_led()
        time.sleep(10)
        