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
    # La URL base se establecerá en before_scenario para tener acceso a los tags
    # Se mantiene esta función para configuración global

def before_scenario(context, scenario):
    chrome_options = Options()
    
    # Configuración de opciones de Chrome
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Opciones adicionales para evitar cierres inesperados
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    
    # Deshabilitar mensajes de consola de Chrome
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)  # Evita que Chrome se cierre al finalizar el script
    
    # Configuración del servicio de ChromeDriver usando webdriver_manager
    # Configuración para permitir cualquier versión de Chrome
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Usar el ChromeDriver local descargado manualmente
    import os
    # Buscar primero en la carpeta del proyecto
    chromedriver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chromedriver.exe")
    
    # Si no existe en la carpeta del proyecto, buscar en la carpeta actual
    if not os.path.exists(chromedriver_path):
        chromedriver_path = "chromedriver.exe"
        if not os.path.exists(chromedriver_path):
            print("\n\nERROR: No se encontró chromedriver.exe")
            print("Por favor, descarga ChromeDriver 138.0.7204.157 desde:")
            print("https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/win64/chromedriver-win64.zip")
            print("Extrae el archivo y coloca chromedriver.exe en la carpeta del proyecto.\n\n")
            raise FileNotFoundError("ChromeDriver no encontrado. Descárgalo manualmente.")
    
    print(f"Usando ChromeDriver local desde: {chromedriver_path}")
    service = ChromeService(executable_path=chromedriver_path)
    
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
    
    # Convertir los tags a una lista de strings para pasarlos a get_product_url
    tags_list = [tag for tag in scenario.tags]
    print(f"Tags del escenario: {tags_list}")
    
    # Obtener la URL según los tags del escenario
    context.base_url = get_product_url(context.product, context.environment, tags=tags_list)
    print(f"URL seleccionada para el escenario: {context.base_url}")
    
    # Caso especial para el comparador (mantener compatibilidad)
    if 'comparador' in scenario.tags:
        print("Ejecutando escenario del comparador con URL específica: https://queplan.cl/Comparar/Seguros-de-Salud")
        context.driver.get("https://queplan.cl/Comparar/Seguros-de-Salud")
    else:
        context.driver.get(context.base_url)

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()