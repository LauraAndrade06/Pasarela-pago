from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

def validar_rut_duplicado(rut: str, ruts_existentes: set):
    """
    Lanza un ValueError si el RUT ya existe en el set de ruts_existentes.
    """
    if rut in ruts_existentes:
        raise ValueError(f"No puede haber mas de un perfil con el mismo número de identificación RUT: {rut}")

def validar_mayoria_edad(fecha_nacimiento: str, formato="%d-%m-%Y", edad_minima=18):
    """
    Lanza un ValueError si la persona es menor de 18 años.
    """
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento, formato)
        hoy = datetime.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        if edad < edad_minima:
            raise ValueError("Debe ser mayor a 18 años")
    except Exception:
        raise ValueError("Debe ser mayor a 18 años")

def validar_mensaje_en_ui(driver, mensaje_esperado, timeout=10):
    """
    Espera y valida que un mensaje con el texto esperado sea visible en la UI.
    Args:
        driver: instancia de Selenium WebDriver
        mensaje_esperado: texto exacto o parcial esperado en el mensaje
        timeout: tiempo máximo de espera en segundos
    Returns:
        True si el mensaje aparece, False en caso contrario
    """
    xpath = f"//*[contains(text(), '{mensaje_esperado}') or contains(., '{mensaje_esperado}') ]"
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(("xpath", xpath))
        )
        return mensaje_esperado in elemento.text
    except TimeoutException:
        return False

def validar_modal_mensaje(driver, texto_esperado, rut_esperado, timeout=10):
    """
    Espera y valida que una modal con el texto esperado y el rut esperado sean visibles en la UI.
    Args:
        driver: instancia de Selenium WebDriver
        texto_esperado: texto parcial o exacto esperado en la modal
        rut_esperado: RUT esperado como string
        timeout: tiempo máximo de espera en segundos
    Returns:
        True si ambos fragmentos aparecen, False en caso contrario
    """
    xpath = f"//*[contains(text(), '{texto_esperado}')]"
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(("xpath", xpath))
        )
        print("TEXTO ENCONTRADO EN MODAL:", elemento.text)
        return texto_esperado in elemento.text and rut_esperado in elemento.text
    except Exception:
        return False

# validations/common_validations.py
def validar_mensaje_en_pantalla(driver, mensaje_esperado, timeout=10):
    """
    Valida que un mensaje de error sea visible en la pantalla.
    - Busca en tooltips, elementos de error y en el body.
    - Ignora mayúsculas/minúsculas y espacios adicionales.
    """

    def buscar_en_elementos(elements, element_type="elemento"):
        for element in elements:
            if element.is_displayed():
                texto = " ".join(element.text.split()).upper()
                if mensaje_normalizado in texto:
                    print(f"=== MENSAJE ENCONTRADO EN {element_type.upper()} ===")
                    print(f"Texto: {element.text}")
                    return True
        return False

    try:
        mensaje_normalizado = " ".join(mensaje_esperado.split()).upper()

        def encontrar_mensaje(_):
            # Buscar en tooltips
            tooltips = driver.find_elements(By.CLASS_NAME, "tooltip-inner")
            if buscar_en_elementos(tooltips, "tooltip"):
                return True

            # Buscar en elementos de error
            elementos_error = driver.find_elements(
                By.CSS_SELECTOR,
                ".error, .text-danger, .invalid-feedback"
            )
            if buscar_en_elementos(elementos_error, "elemento de error"):
                return True

            # Buscar en el body
            if mensaje_esperado in driver.find_element(By.TAG_NAME, "body").text:
                print("=== MENSAJE ENCONTRADO EN EL BODY ===")
                return True

            return False

        WebDriverWait(driver, timeout).until(encontrar_mensaje)
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        print("=== HTML (primeros 1000 caracteres) ===")
        print(driver.page_source[:1000])
        return False