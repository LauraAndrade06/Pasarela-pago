from behave import when, then
from utils.queplan_data import QueplanTestData


@when("ingresa datos de contratante")
def step_impl(context):
    try:
        context.page.ingresar_datos_contratante(QueplanTestData.DATOS_CONTRATANTE)
    except Exception as e:
        context.error_mensaje = str(e)

@when("ingresa datos de beneficiario")
def step_impl(context):
    try:
        context.page.ingresar_datos_beneficiario(QueplanTestData.DATOS_BENEFICIARIO_1)
        context.page.hacer_clic_siguiente_paso()  # Hacer clic después de agregar el primer beneficiario
    except Exception as e:
        context.error_mensaje = str(e)

@when("ingresa datos de dps")
def step_impl(context):
    print("\n\nSTEP: Ingresando datos de DPS")
    try:
        print("Intentando llamar a context.page.dps_inputs()")
        context.page.dps_inputs()
        print("Llamada a context.page.dps_inputs() completada")
    except Exception as e:
        print(f"ERROR en step dps_inputs: {e}")
        context.error_mensaje = str(e)

@when("realiza el pago con tarjeta de crédito")
def step_impl(context):
    try:
        context.page.realizar_pago(QueplanTestData.DATOS_PAGO)
    except Exception as e:
        context.error_mensaje = str(e)

@then('se debe mostrar la confirmación de pago exitoso')
def step_impl(context):
    mensaje = context.page.obtener_mensaje_confirmacion_pago()
    assert mensaje and 'Suscripción solicitada' in mensaje, "No se mostró el mensaje 'Suscripción solicitada'"
