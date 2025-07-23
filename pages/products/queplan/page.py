from pages.base_page import BasePage
from pages.products.queplan.components.contracted import ContratanteComponent
from pages.products.queplan.components.beneficiary import BeneficiarioComponent
from pages.products.queplan.components.payment import PagoComponent
from pages.products.queplan.components.dps import DpsComponent
from validations.common_validations import validar_mensaje_en_pantalla, validar_modal_mensaje

class QueplanPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.contratante = ContratanteComponent(driver)
        self.beneficiario = BeneficiarioComponent(driver)
        self.dps = DpsComponent(driver)
        self.pago = PagoComponent(driver)

    def ingresar_datos_contratante(self, datos):
        self.contratante.ingresar_datos(datos)

    def ingresar_datos_beneficiario(self, datos):
        self.beneficiario.ingresar_beneficiario1(datos)

    def ingresar_datos_beneficiario2(self, datos):
        self.beneficiario.ingresar_beneficiario2(datos)

    def hacer_clic_siguiente_paso(self):
        self.pago.hacer_clic_siguiente_paso()

    def dps_inputs(self):
        print("QueplanPage: Llamando a dps_inputs")
        self.dps.dps_inputs()
        print("QueplanPage: dps_inputs completado")

    def realizar_pago(self, datos_pago):
        self.pago.realizar_pago(datos_pago)

    def obtener_mensaje_confirmacion_pago(self, timeout=50):
        return self.pago.obtener_mensaje_confirmacion_pago(timeout)

    def validar_mensaje_error_generico(self, mensaje_esperado, timeout=10):
        return validar_mensaje_en_pantalla(self.driver, mensaje_esperado, timeout)

    def validar_modal_mensaje_generico(self, texto_esperado, rut_esperado, timeout=10):
        return validar_modal_mensaje(self.driver, texto_esperado, rut_esperado, timeout)