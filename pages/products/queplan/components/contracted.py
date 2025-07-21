from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import ContratanteLocators

class ContratanteComponent(BaseComponent):
    def ingresar_datos(self, datos):
        self.type(*ContratanteLocators.NOMBRE, datos['nombre'])
        self.type(*ContratanteLocators.APELLIDO_PATERNO, datos['apellido_paterno'])
        self.type(*ContratanteLocators.APELLIDO_MATERNO, datos['apellido_materno'])
        self.type(*ContratanteLocators.RUT, datos['rut'])
        self.type(*ContratanteLocators.FECHA_NAC, datos['fecha_nacimiento'])
        if datos['genero'].lower() in ['masculino', 'hombre', 'm']:
            self.click(*ContratanteLocators.GENERO)
        else:
            self.click(*ContratanteLocators.GENERO)
        self.select_mat_option(*ContratanteLocators.SISTEMA_PENSIONAL, datos['sistema_pensional'])
        self.select_mat_option(*ContratanteLocators.REGION, datos['region'])
        self.select_mat_option(*ContratanteLocators.COMUNA, datos['comuna'])
        self.type(*ContratanteLocators.DIRECCION, datos['direccion'])
        self.type(*ContratanteLocators.ESTATURA, datos['estatura'])
        self.type(*ContratanteLocators.PESO, datos['peso'])
        self.type(*ContratanteLocators.CORREO_PRINCIPAL, datos['correo_principal'])
        self.type(*ContratanteLocators.CORREO_VALIDACION, datos['correo_validacion'])
        self.type(*ContratanteLocators.TELEFONO, datos['numero_telefono'])
        self.select_mat_option(*ContratanteLocators.TIPO_PAGO, datos['tipo_pago'])
        self.select_mat_option(*ContratanteLocators.TIPO_CUENTA, datos['tipo_cuenta'])
        self.select_mat_option(*ContratanteLocators.BANCO, datos['banco'])
        self.type(*ContratanteLocators.NUMERO_CUENTA, datos['numero_cuenta'])