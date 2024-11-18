import qrcode

#Genera un código qr, en archivo png, para conexión wifi, con los parametros configurados abajo.


def generate_wifi_qrcode(
        ssid: str,
        password: str,
        security_type: str,
        qr_code_file: str = "qrcode.png") -> None:

    wifi_data = f"WIFI:T:{security_type};S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )

    qr.add_data(wifi_data)
    qr.make(fit=True)

    qr_code_image = qr.make_image(
        fill_color="black", back_color="white"
    )

    # Create and save the QR Code
    qr_code_image.save(qr_code_file)


wifi_name     = "WifiManager"   #input("Enter the Wifi name : ")
wifi_password = "1234567890"    #input("Enter the Wifi password : ")
security_type = "WPA2"          #input("Enter the security type : ")

if not security_type:
   security_type = "WPA"
   
generate_wifi_qrcode(wifi_name, wifi_password, security_type)