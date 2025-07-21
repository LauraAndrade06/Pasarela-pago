from behave import given, when, then
from utils.queplan_data import QueplanTestData
import copy
import time
from pages.products.queplan.locators.queplan_locators import ContratanteLocators, BeneficiarioLocators


@given("que el usuario accede al formulario de Queplan")
def step_impl(context):
    context.page = context.queplan_page
    context.driver.get(context.base_url)
    context.error_mensaje = None

@when("ingresa datos de contratante menor de edad")
def step_impl(context):
    datos_menor = dict(QueplanTestData.DATOS_CONTRATANTE)
    datos_menor['fecha_nacimiento'] = '02-02-2020'  # Menor de edad
    try:
        context.page.ingresar_datos_contratante(datos_menor)
        context.page.hacer_clic_siguiente_paso()
    except Exception as e:
        context.error_mensaje = str(e)

@when('ingresa datos de cónyuge menor de edad con rut "{rut}"')
def step_impl(context, rut):
    datos = copy.deepcopy(QueplanTestData.DATOS_BENEFICIARIO_1)
    datos['rut'] = rut
    datos['fecha_nacimiento'] = "09-09-2010"  # Fecha que hace menor de 18 años
    try:
        context.page.ingresar_datos_beneficiario(datos)
        context.page.hacer_clic_siguiente_paso()
    except Exception as e:
        context.error_mensaje = str(e)

@when('ingresa datos de contratante con rut "{rut}"')
def step_impl(context, rut):
    datos = copy.deepcopy(QueplanTestData.DATOS_CONTRATANTE)
    datos['rut'] = rut
    context.page.ingresar_datos_contratante(datos)

# Para cuando NO se especifica hacer clic
@when('ingresa datos de beneficiario con rut "{rut}"')
def step_ingresar_beneficiario_sin_clic(context, rut):
    datos = copy.deepcopy(QueplanTestData.DATOS_BENEFICIARIO_1)
    datos['rut'] = rut
    try:
        context.page.ingresar_datos_beneficiario(datos)
    except Exception as e:
        context.error_mensaje = str(e)

# Para cuando SÍ se especifica hacer clic
@when('ingresa datos de beneficiario con rut "{rut}" y hacer clic en siguiente paso')
def step_ingresar_beneficiario_con_clic(context, rut):
    datos = copy.deepcopy(QueplanTestData.DATOS_BENEFICIARIO_1)
    datos['rut'] = rut
    try:
        context.page.ingresar_datos_beneficiario(datos)
        context.page.hacer_clic_siguiente_paso()
    except Exception as e:
        context.error_mensaje = str(e)

@when('ingresa solo la fecha de nacimiento del contratante "{fecha}"')
def step_impl(context, fecha):
    context.page.contratante.type(*ContratanteLocators.FECHA_NAC, fecha)
    context.page.contratante.click(*ContratanteLocators.BOTON_AGREGAR_BENEFICIARIO)

@when('ingresa solo la fecha de nacimiento del beneficiario "{fecha}" y parentesco "Hijo(a)"')
def step_impl(context, fecha):
    context.page.beneficiario.type(*BeneficiarioLocators.FECHA_NAC, fecha)
    context.page.beneficiario.select_mat_option(*BeneficiarioLocators.RELACION, "Hijo(a)")

@when('agrega otro cónyuge con rut "{rut}"')
def step_impl(context, rut):
    try:
        datos = copy.deepcopy(QueplanTestData.DATOS_BENEFICIARIO_2)
        datos['rut'] = rut
        context.page.ingresar_datos_beneficiario2(datos)
        # No hacer clic en Siguiente paso aquí
    except Exception as e:
        context.error_mensaje = str(e)

@when('hace clic en Siguiente paso')
def step_impl(context):
    try:
        context.page.hacer_clic_siguiente_paso()
    except Exception as e:
        context.error_mensaje = str(e)

@then('debe mostrarse el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    time.sleep(5)
    assert context.page.validar_mensaje_error_generico(mensaje), \
        f"No se mostró el mensaje '{mensaje}'"

@then('debe mostrarse el mensaje de error con rut "{mensaje}" y el rut "{rut}"')
def step_impl(context, mensaje, rut):
    time.sleep(5)  # Espera adicional para asegurar que el mensaje esté visible
    assert context.page.validar_modal_mensaje_generico(mensaje, rut), \
        f"No se mostró el mensaje: '{mensaje}' con RUT {rut}"