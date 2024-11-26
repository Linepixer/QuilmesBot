# Importo librerias
import email_module
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Printeo version
print("Notificador de turnos - QuilmesBot v1.3")

# Configuro opciones del navegador
options = Options()
options.binary_location = "chrome/chrome.exe"
options.add_argument("--disable-infobars")
options.add_argument('--no-sandbox')
options.add_argument('--headless=new')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service('chrome/chromedriver.exe')

while True:
    # Inicializo del navegador
    driver = webdriver.Chrome(service=service, options=options)
    
    # Cargo de la pagina
    driver.get("https://arquivirtual.quilmes.gov.ar/municipal/App/RegistroTurnos/Original.aspx")

    # Obtengo el boton de siguiente y le doy click
    next_button = driver.find_element(By.XPATH, '//a[@title="Ir al mes siguiente."]')
    next_button.click()

    # Comentar esto o multiplicar para seleccionar el mes
    # sleep(0.3)
    # next_button = driver.find_element(By.XPATH, '//a[@title="Ir al mes siguiente."]')
    # next_button.click()

    # Espero un momento
    sleep(0.3)

    # Busco el calendario
    calendar = driver.find_element(By.ID, "ContentPlaceHolder1_Calendar1")

    # Busco los turnos disponibles y printeo el numero de dia
    days_available = calendar.find_elements(By.XPATH, ".//a[@href and @style='color:Black']")

    if len(days_available) == 0:
        print("INFO: No hay fechas disponibles")
        driver.quit()
        sleep(300)
    else:
        print("INFO: Se encontraron las siguientes fechas disponibles:")
        data = ""
        for day in days_available:
            data = data + "- " + day.get_dom_attribute("title") + "\n"
            print("- " + day.get_dom_attribute("title"))
        data = data + "\n" + "Link para sacar turno: https://arquivirtual.quilmes.gov.ar/municipal/App/RegistroTurnos/Original.aspx"
        email_module.send_notification(data)
        driver.quit()
        print("INFO: Esperando 24 horas")
        sleep(86400)