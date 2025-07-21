from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import logging

class BasePage:
    def __init__(self, driver, timeout=10, logger=None):
        self.driver = driver
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    def _wait_element(self, by, locator, timeout=None, clickable=False):
        """Espera por un elemento según las condiciones dadas."""
        timeout = timeout or self.timeout
        condition = EC.element_to_be_clickable if clickable else EC.visibility_of_element_located
        try:
            return WebDriverWait(self.driver, timeout).until(condition((by, locator)))
        except Exception as e:
            self.logger.error(f"Elemento no encontrado: {by}={locator}: {e}")
            raise

    def _scroll_to(self, element):
        """Desplaza la vista hasta el elemento."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def click(self, by, locator, timeout=None):
        """Hace clic en un elemento con scroll y espera.
        
        Args:
            by: Estrategia de localización (By.XPATH, By.ID, etc.)
            locator: Valor del localizador
            timeout: Tiempo máximo de espera en segundos
            
        Raises:
            Exception: Si no se puede hacer clic en el elemento
        """
        try:
            # 1. Esperar a que el elemento esté presente y sea clickeable
            element = self._wait_element(by, locator, timeout, clickable=True)
            
            # 2. Hacer scroll hasta el elemento
            self._scroll_to(element)
            
            # 3. Esperar nuevamente después del scroll
            element = WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            
            # 4. Intentar hacer clic de forma estándar
            try:
                element.click()
            except:
                # 5. Si falla, intentar con JavaScript
                self.driver.execute_script("arguments[0].click();", element)
                
        except Exception as e:
            self.logger.error(f"Error al hacer clic en {by}={locator}: {e}")
            # Tomar captura de pantalla para depuración
            self.take_screenshot(f"error_click_{locator}.png")
            raise

    def type(self, by, locator, text, timeout=None):
        """Escribe texto en un campo con validaciones."""
        try:
            element = self._wait_element(by, locator, timeout, clickable=True)
            self._scroll_to(element)
            element.clear()
            element.send_keys(str(text))
        except Exception as e:
            self.logger.error(f"Error al escribir en {by}={locator}: {e}")
            raise

    def select_mat_option(self, by, value, option_text, timeout=None):
        """
        Selecciona una opción en un mat-select de Angular Material.

        Args:
            by: Estrategia de localización (By.ID, By.CSS_SELECTOR, etc.)
            value: Valor del localizador
            option_text: Texto de la opción a seleccionar
            timeout: Tiempo máximo de espera (opcional)
        """
        try:
            # Esperar a que el mat-select sea clickeable
            select = WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable((by, value))
            )

            # Hacer scroll hasta el select
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",
                select
            )

            # Hacer clic usando JavaScript para evitar problemas de superposición
            self.driver.execute_script("arguments[0].click();", select)

            # Construir el XPath para la opción en el overlay
            option_xpath = (
                "//div[contains(@class, 'cdk-overlay-container')]//"
                "div[contains(@class, 'cdk-overlay-pane')]//"
                f"mat-option//span[contains(text(), '{option_text}') or contains(., '{option_text}')]"
            )

            # Esperar a que la opción esté presente y sea clickeable
            option = WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )

            # Hacer scroll hasta la opción
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                option
            )

            # Hacer clic en la opción usando JavaScript
            self.driver.execute_script("arguments[0].click();", option)

        except Exception as e:
            self.logger.error(f"Error al seleccionar opción '{option_text}' en {by}={value}: {e}")
            self.take_screenshot(f"error_select_{value}.png")
            raise

    # Método auxiliar para compatibilidad
    def wait_until_visible(self, by, locator, timeout=None):
        return self._wait_element(by, locator, timeout)