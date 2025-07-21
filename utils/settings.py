import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración general
BROWSER = os.getenv('BROWSER', 'chrome')
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '15'))
SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'

# Configuración de reportes
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
SCREENSHOT_DIR = os.path.join(REPORT_DIR, 'screenshots')