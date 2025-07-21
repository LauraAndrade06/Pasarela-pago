import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from dotenv import load_dotenv
from utils.urls import get_product_url

# Importa tus page objects aquí
from pages.products.queplan.page import QueplanPage
# from pages.colsanitas_page import ColsanitasPage # Ejemplo si hay otro producto

def before_all(context):
    load_dotenv()
    context.product = os.getenv('PRODUCT', 'queplan')
    context.environment = os.getenv('ENVIRONMENT', 'qa')
    context.base_url = get_product_url(context.product, context.environment)
    if not context.base_url:
        raise Exception(f"No se encontró URL para producto {context.product} en entorno {context.environment}")

def before_scenario(context, scenario):
    chrome_options = Options()
    
    # Configuración de opciones de Chrome
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Deshabilitar mensajes de consola de Chrome
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Configuración del servicio de ChromeDriver
    service = ChromeService(
        executable_path='/usr/local/bin/chromedriver',
        service_args=['--verbose', '--log-path=chromedriver.log']
    )
    
    try:
        # Inicializar el navegador
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configurar tiempo de espera implícito
        context.driver.implicitly_wait(10)
        
        # Configurar el tamaño de la ventana
        context.driver.set_window_size(1920, 1080)
        
    except Exception as e:
        print(f"Error al inicializar el WebDriver: {str(e)}")
        print("Verifica que ChromeDriver esté correctamente instalado en /usr/local/bin/chromedriver")
        print("Puedes verificar la instalación con: which chromedriver")
        print("Puedes instalar/actualizar con: brew install --cask chromedriver")
        raise

    # Instancia el Page Object correcto según el producto
    if context.product == 'queplan':
        context.queplan_page = QueplanPage(context.driver)
        context.page = context.queplan_page
    # elif context.product == 'colsanitas':
    #     context.colsanitas_page = ColsanitasPage(context.driver)
    #     context.page = context.colsanitas_page
    # Agrega más productos aquí

    context.driver.get(context.base_url)

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()