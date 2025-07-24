from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import PagoLocators
import time

class PagoComponent(BaseComponent):
    def realizar_pago(self, datos_pago):
        time.sleep(5)
        #self.click(*PagoLocators.PASARELA_PAGO)
        self.type(*PagoLocators.NUMERO_TARJETA, datos_pago['numero_tarjeta'])
        self.type(*PagoLocators.FECHA_VENCIMIENTO, datos_pago['fecha_vencimiento'])
        self.type(*PagoLocators.CVV, datos_pago['cvv'])
        self.type(*PagoLocators.NOMBRE_TARJETA, datos_pago['nombre_titular'])
        self.click(*PagoLocators.BOTON_PAGAR)

    def obtener_mensaje_confirmacion_pago(self, timeout=50):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(PagoLocators.MENSAJE_SUSCRIPCION)
            )
            return elemento.text
        except Exception:
            if self.logger:
                self.logger.error("No se encontró el mensaje 'Suscripción solicitada'")
            return None

    def hacer_clic_siguiente_paso(self):
        self.click(*PagoLocators.BOTON_SIGUIENTE)