from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import PagoLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PagoComponent(BaseComponent):
    def realizar_pago(self, datos_pago):

        time.sleep(3)  # Espera a que cargue el formulario de pago

        def fill_in_iframe_input(input_id=None, value=None, by=By.ID, by_name=None):
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for idx, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    try:
                        if by_name:
                            input_elem = WebDriverWait(self.driver, 0.5).until(
                                EC.visibility_of_element_located((By.NAME, by_name))
                            )
                        else:
                            input_elem = WebDriverWait(self.driver, 0.5).until(
                                EC.visibility_of_element_located((by, input_id))
                            )
                        input_elem.click()
                        input_elem.clear()
                        input_elem.send_keys(value)
                        self.driver.switch_to.default_content()
                        print(f"Campo {input_id or by_name} llenado en iframe {idx}")
                        return True
                    except Exception:
                        self.driver.switch_to.default_content()
                except Exception:
                    self.driver.switch_to.default_content()
            print(f"No se encontró el campo {input_id or by_name} en ningún iframe")
            return False

        # Llenar campos de pago en iframes
        fill_in_iframe_input("cardNumber", datos_pago['numero_tarjeta'])
        fill_in_iframe_input("expirationDate", datos_pago['fecha_vencimiento'])
        fill_in_iframe_input("securityCode", datos_pago['cvv'])

        # Campo nombre del titular: primero intenta en el DOM principal
        try:
            input_elem = WebDriverWait(self.driver, 0.5).until(
                EC.visibility_of_element_located((By.NAME, "HOLDER_NAME"))
            )
            input_elem.click()
            input_elem.clear()
            input_elem.send_keys(datos_pago['nombre_titular'])
            print("Campo HOLDER_NAME llenado en el DOM principal")
        except Exception:
            # Si falla, busca en los iframes (fallback)
            fill_in_iframe_input(by_name="HOLDER_NAME", value=datos_pago['nombre_titular'])

        # Click en pagar (fuera de iframe)
        self.click(*PagoLocators.BOTON_PAGAR)
        time.sleep(10)

    def obtener_mensaje_confirmacion_pago(self, timeout=50):
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(PagoLocators.MENSAJE_SUSCRIPCION)
            )
            return elemento.text
        except Exception:
            if self.logger:
                self.logger.error("No se encontró el mensaje 'No se pudo completar el pago'")
            return None

    def hacer_clic_siguiente_paso(self):
        self.click(*PagoLocators.BOTON_SIGUIENTE)