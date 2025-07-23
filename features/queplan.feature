@regression @queplan
Feature: Flujo completo de contratación de seguro en Queplan

  Background:
    Given que el usuario accede al formulario de Queplan

  @featuretest
  Scenario: Completar formulario y realizar pago exitoso
    When ingresa datos de contratante
    And ingresa datos de beneficiario
    And ingresa datos de dps
    And realiza el pago con tarjeta de crédito
    Then se debe mostrar la confirmación de pago exitoso

  @comparador
  Scenario: Validar el comparador antes de llegar a la pasarela de pago
    When completa el formulario inicial de búsqueda
    And selecciona un plan y hace clic en contratar
    And completa el formulario de contratación
    Then debe mostrarse el comparador con los datos correctos

  @negative
  Scenario: No se permite RUT duplicado
    When ingresa datos de contratante con rut "10638372-3"
    And ingresa datos de beneficiario con rut "10638372-3" y hacer clic en siguiente paso
    Then debe mostrarse el mensaje de error con rut "No puede haber mas de un perfil con el mismo número de identificación" y el rut "106383723"

  @negative
  Scenario: No se permite contratante menor de 18 años
    When ingresa datos de contratante menor de edad
    Then debe mostrarse el mensaje de error "Debe ser mayor a 18 años"

  @negative
  Scenario: No se permite cónyuge menor de 18 años
    When ingresa datos de contratante con rut "10638372-3"
    And ingresa datos de cónyuge menor de edad con rut "16557350-1"
    Then debe mostrarse el mensaje de error "Perfil (Cónyuge) no cumple con edad mínima de 18 años"

  @negative
  Scenario: No se permite que el hijo sea mayor que el contratante
    When ingresa solo la fecha de nacimiento del contratante "01-01-1990"
    And ingresa solo la fecha de nacimiento del beneficiario "01-01-1980" y parentesco "Hijo(a)"
    Then debe mostrarse el mensaje de error "La edad del 'Hijo/Hija' debería ser menor a la del titular."

  @negative
  Scenario: No se permite agregar más de un cónyuge
    When ingresa datos de contratante con rut "17470576-3"
    And ingresa datos de beneficiario con rut "15046896-5"
    And agrega otro cónyuge con rut "6065750-5"
    And hace clic en Siguiente paso
    Then debe mostrarse el mensaje de error "No es posible continuar, dado que los asegurados adicionales incorporados no cumplen con los requisitos de contratación."
