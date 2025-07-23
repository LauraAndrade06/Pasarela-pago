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
            # No intentamos tomar capturas para evitar errores
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
            # No intentamos tomar capturas para evitar errores
            raise

    # Método auxiliar para compatibilidad
    def wait_until_visible(self, by, locator, timeout=None):
        return self._wait_element(by, locator, timeout)

    def click_mat_checkbox(self, by, locator, timeout=None):
        """
        Método especializado para hacer clic en checkboxes de Angular Material.
        
        Args:
            by: Estrategia de localización (By.CSS_SELECTOR, By.XPATH, etc.)
            locator: Valor del localizador
            timeout: Tiempo máximo de espera (opcional)
        """
        try:
            # Esperar a que el checkbox sea visible
            checkbox = self._wait_element(by, locator, timeout)
            
            # Hacer scroll hasta el checkbox
            self._scroll_to(checkbox)
            
            # Intentar hacer clic usando JavaScript en el área del checkbox
            # En Angular Material, a veces necesitamos hacer clic en el área interna
            self.driver.execute_script("""
                var checkbox = arguments[0];
                // Intentar hacer clic en el input interno si existe
                var input = checkbox.querySelector('input[type="checkbox"]');
                if (input) {
                    input.click();
                } else {
                    // Si no hay input, hacer clic en el checkbox directamente
                    checkbox.click();
                }
            """, checkbox)
            
            # Esperar un momento para que el estado del checkbox cambie
            import time
            time.sleep(0.5)
            
        except Exception as e:
            self.logger.error(f"Error al hacer clic en checkbox {by}={locator}: {e}")
            # No intentamos tomar capturas para evitar errores
            raise
            
    def obtener_ids_botones_no(self):
        """
        Obtiene los IDs de todos los botones de radio con valor "No" que están visibles.
        Basado en el código de Playwright proporcionado.
        
        Returns:
            list: Lista de diccionarios con id y estado de visibilidad de los botones.
        """
        try:
            ids_procesados = set()  # Para evitar duplicados
            ids_botones_no = []
            
            # Encontrar todos los contenedores formly-field
            contenedores = self.driver.find_elements(By.CSS_SELECTOR, 'formly-field')
            
            for contenedor in contenedores:
                # Verificar si el contenedor está oculto
                estilo = self.driver.execute_script("return arguments[0].style.display", contenedor)
                if estilo == "none":
                    continue
                    
                # Buscar botones de radio con valor "No" dentro del contenedor
                botones_no = contenedor.find_elements(By.CSS_SELECTOR, 'input[type="radio"][value="No"]')
                
                for boton in botones_no:
                    id_boton = boton.get_attribute('id')
                    
                    # Filtrar solo IDs que contienen "mat-radio"
                    if id_boton and "mat-radio" in id_boton and id_boton not in ids_procesados:
                        # Verificar si el botón es visible
                        try:
                            es_visible = boton.is_displayed()
                            ids_botones_no.append({"id": id_boton, "visible": es_visible})
                            ids_procesados.add(id_boton)
                        except:
                            pass  # Ignorar elementos que no se pueden verificar
            
            self.logger.info(f"Resultados de botones 'No' con 'mat-radio': {ids_botones_no}")
            return ids_botones_no
            
        except Exception as e:
            self.logger.error(f"Error en obtener_ids_botones_no: {e}")
            return []
    
    def clickear_botones_no(self):
        """
        Hace clic en todos los botones de radio con valor "No" que están visibles.
        Basado en el código de Playwright proporcionado.
        """
        try:
            ids_botones_no = self.obtener_ids_botones_no()
            self.logger.info(f"Botones obtenidos para clic: {ids_botones_no}")
            
            for boton_info in ids_botones_no:
                id_boton = boton_info["id"]
                try:
                    # Buscar el botón por ID
                    selector = f"#{id_boton}"
                    boton = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if boton.is_displayed():
                        # Hacer scroll hasta el botón
                        self._scroll_to(boton)
                        
                        # Intentar hacer clic de forma estándar
                        try:
                            boton.click()
                        except:
                            # Si falla, intentar con JavaScript
                            self.driver.execute_script("arguments[0].click();", boton)
                            
                        self.logger.info(f"Clickeado: {id_boton}")
                        
                        # Esperar un momento entre clics
                        import time
                        time.sleep(0.5)
                    else:
                        self.logger.info(f"Radio button no visible: {id_boton}")
                        
                except Exception as e:
                    self.logger.error(f"Error al hacer clic en {id_boton}: {e}")
                    
            self.logger.info("Proceso de clic completado.")
            
        except Exception as e:
            self.logger.error(f"Error en clickear_botones_no: {e}")
            raise