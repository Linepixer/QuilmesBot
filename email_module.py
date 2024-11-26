import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification(turns_data):
    # Levanto los datos del json de configuracion del smtp
    with open('smtp.json', 'r') as json_file:
        smtp_setup = json.load(json_file)
        smtp_server = smtp_setup["smtp_server"]
        smtp_port = smtp_setup["smtp_port"]
        smtp_user = smtp_setup["smtp_user"]
        smtp_password = smtp_setup["smtp_password"]

    # Levanto los emails a los que enviare la notificacion
    with open('addresses.json', 'r') as json_file:
        addresses = json.load(json_file)

    # Bucleo en cada uno de los emails
    for address in addresses:
        # Armo lo basico del email
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['Subject'] = 'Turnos encontrados para licencia de conducir'

        # Pongo los datos obtenidos
        body = "Se encontraron las siguientes fechas disponibles:\n" + turns_data
        msg.attach(MIMEText(body, 'plain'))

        # Envio el email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            msg['To'] = address
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("INFO: Email enviado a {}".format(address))

if __name__ == "__main__":
    pass