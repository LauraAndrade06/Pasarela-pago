import time
from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import BeneficiarioLocators, ContratanteLocators
from selenium.webdriver.common.by import By

class BeneficiarioComponent(BaseComponent):
    def ingresar_beneficiario1(self, datos):
        self.click(*ContratanteLocators.BOTON_AGREGAR_BENEFICIARIO)
        self.type(*BeneficiarioLocators.NOMBRE, datos['nombre'])
        self.type(*BeneficiarioLocators.APELLIDO_PATERNO, datos['apellido_paterno'])
        self.type(*BeneficiarioLocators.APELLIDO_MATERNO, datos['apellido_materno'])
        self.type(*BeneficiarioLocators.RUT, datos['rut'])
        self.type(*BeneficiarioLocators.FECHA_NAC, datos['fecha_nacimiento'])
        if datos['genero_beneficiario1'].lower() in ['masculino', 'hombre', 'm']:
            self.click(*BeneficiarioLocators.GENERO)
        else:
            self.click(*BeneficiarioLocators.GENERO)
        self.select_mat_option(*BeneficiarioLocators.RELACION, datos['relacion_contratante'])
        self.select_mat_option(*BeneficiarioLocators.SISTEMA_PENSIONAL, datos['sistema_pensional'])
        self.select_mat_option(*BeneficiarioLocators.REGION, datos['region'])
        self.select_mat_option(*BeneficiarioLocators.COMUNA, datos['comuna'])
        self.type(*BeneficiarioLocators.DIRECCION, datos['direccion'])
        self.type(*BeneficiarioLocators.ESTATURA, datos['estatura'])
        self.type(*BeneficiarioLocators.PESO, datos['peso'])

    def ingresar_beneficiario2(self, datos):
        self.click(*ContratanteLocators.BOTON_AGREGAR_BENEFICIARIO)
        self.type(*BeneficiarioLocators.NOMBRE2, datos['nombre'])
        self.type(*BeneficiarioLocators.APELLIDO_PATERNO2, datos['apellido_paterno'])
        self.type(*BeneficiarioLocators.APELLIDO_MATERNO2, datos['apellido_materno'])
        self.type(*BeneficiarioLocators.RUT2, datos['rut'])
        self.type(*BeneficiarioLocators.FECHA_NAC2, datos['fecha_nacimiento'])
        time.sleep(1)
        # Para seleccionar el género del segundo beneficiario
        if datos['genero_beneficiario2'].lower() in ['femenino', 'mujer', 'f']:
            # Hacer clic en Femenino
            self.driver.find_element(By.XPATH,
                                     "/html/body/app-root/queplan-online-sale-manager/proxy-payment-stepper/div/div/payment-stepper/stepper/div/mat-horizontal-stepper/div/div[2]/div[1]/div/div[1]/integration-form/form/formly-form/formly-field/formly-group/formly-field[2]/qp-array-type/div[2]/div[2]/formly-field/formly-group/formly-field[8]/formly-wrapper-mat-form-field/mat-form-field/div[1]/div/div[2]/formly-field-mat-radio/mat-radio-group/mat-radio-button[1]/div/div/input").click()
        else:
            # Hacer clic en Masculino
            self.driver.find_element(By.XPATH,
                                     "/html/body/app-root/queplan-online-sale-manager/proxy-payment-stepper/div/div/payment-stepper/stepper/div/mat-horizontal-stepper/div/div[2]/div[1]/div/div[1]/integration-form/form/formly-form/formly-field/formly-group/formly-field[2]/qp-array-type/div[2]/div[2]/formly-field/formly-group/formly-field[8]/formly-wrapper-mat-form-field/mat-form-field/div[1]/div/div[2]/formly-field-mat-radio/mat-radio-group/mat-radio-button[2]/div/div/input").click()
        self.select_mat_option(*BeneficiarioLocators.RELACION2, datos['relacion_contratante'])
        self.select_mat_option(*BeneficiarioLocators.SISTEMA_PENSIONAL2, datos['sistema_pensional'])
        self.select_mat_option(*BeneficiarioLocators.REGION2, datos['region'])
        self.select_mat_option(*BeneficiarioLocators.COMUNA2, datos['comuna'])
        self.type(*BeneficiarioLocators.DIRECCION2, datos['direccion'])
        self.type(*BeneficiarioLocators.ESTATURA2, datos['estatura'])
        self.type(*BeneficiarioLocators.PESO2, datos['peso'])