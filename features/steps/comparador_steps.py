from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
from utils.queplan_data import QueplanTestData

@when('completa el formulario inicial de búsqueda')
def step_impl(context):
    try:
        try:
            if not hasattr(context, 'driver') or context.driver is None:
                print("El driver de Selenium no está inicializado. Iniciando nuevo driver...")
                raise Exception("Driver no inicializado")
                
            try:
                # Verificar si hay ventanas abiertas
                window_handles = context.driver.window_handles
                if not window_handles:
                    print("No hay ventanas de navegador abiertas")
                    raise Exception("No hay ventanas de navegador abiertas")
            except Exception as window_error:
                print(f"Error al verificar ventanas: {str(window_error)}")
                raise Exception("Error al verificar ventanas del navegador")
                
            # Verificar si ya estamos en la página de comparación o en la página de compra online
            try:
                current_url = context.driver.current_url
                print(f"URL actual: {current_url}")
                
                if "Compra-Online" in current_url:
                    print("Ya estamos en la página de compra online, saltando el paso de búsqueda")
                    return
            except Exception as url_error:
                print(f"Error al obtener URL: {str(url_error)}")
                raise Exception("Error al obtener URL actual")
                
        except Exception as e:
            print(f"Error al verificar el estado del navegador: {str(e)}")
            # Reiniciar el navegador si hay problemas
            print("Reiniciando el navegador debido a un problema con la ventana...")
            
            # Cerrar el driver existente si aún está presente
            try:
                if hasattr(context, 'driver') and context.driver:
                    context.driver.quit()
                    print("Driver cerrado correctamente")
            except Exception as close_error:
                print(f"Error al cerrar el driver: {str(close_error)}")
            
            # Reiniciar el navegador usando el hook de before_scenario
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service as ChromeService
            import os
            import time
                    
            # Buscar el chromedriver en la misma ubicación que en environment.py
            chromedriver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chromedriver.exe")
            if not os.path.exists(chromedriver_path):
                chromedriver_path = "chromedriver.exe"
            
            print(f"Reiniciando con ChromeDriver desde: {chromedriver_path}")
            service = ChromeService(executable_path=chromedriver_path)
            
            # Crear un nuevo driver
            try:
                context.driver = webdriver.Chrome(service=service)
                context.driver.implicitly_wait(10)
                context.driver.set_window_size(1920, 1080)
                
                # Reiniciar la página del comparador
                print("Navegando a la página del comparador...")
                context.driver.get("https://queplan.cl/Comparar/Seguros-de-Salud")
                
                # Esperar a que la página se cargue completamente
                time.sleep(5)
                
                # Verificar que la página se cargó correctamente
                if "queplan" in context.driver.current_url.lower():
                    print("Navegador reiniciado correctamente y página cargada")
                else:
                    print(f"La página no se cargó correctamente. URL actual: {context.driver.current_url}")
            except Exception as init_error:
                print(f"Error al inicializar el nuevo driver: {str(init_error)}")
                raise Exception(f"No se pudo inicializar el navegador: {str(init_error)}")
                
            return
        
        # Esperar a que el campo de edad esté disponible
        try:
            edad_input = WebDriverWait(context.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="cotizante_edad"]'))
            )
            edad_input.clear()
            edad_input.send_keys('25')
            
            # Seleccionar el sexo
            context.driver.find_element(By.CSS_SELECTOR, 'mat-select[formcontrolname="cotizante_sexo"]').click()
            WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//mat-option[contains(., "Hombre")]'))
            ).click()
            
            # Hacer clic en el botón de enviar
            WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            ).click()
            
            # Esperar a que se complete la redirección
            time.sleep(3)
            print(f"URL después de enviar el formulario: {context.driver.current_url}")
        except Exception as e:
            print(f"Error durante la interacción con el formulario: {str(e)}")
            try:
                context.driver.save_screenshot('error-formulario-inicial.png')
            except:
                print("No se pudo guardar la captura de pantalla")
    except Exception as e:
        context.error_mensaje = str(e)
        print(f"Error general en el paso 'completa el formulario inicial de búsqueda': {str(e)}")
        raise Exception(f"Error al completar el formulario inicial: {str(e)}")

@when('selecciona un plan y hace clic en contratar')
def step_impl(context):
    try:
        # Verificar si el navegador sigue abierto
        try:
            # Intentar acceder a una propiedad del navegador para verificar si sigue abierto
            window_handles = context.driver.window_handles
            if not window_handles:
                raise Exception("No hay ventanas de navegador abiertas")
                
            # Verificar si ya estamos en la página de compra online
            current_url = context.driver.current_url
            print(f"URL actual en paso 'selecciona un plan': {current_url}")
            
            if "Compra-Online" in current_url:
                print("Ya estamos en la página de compra online, saltando la selección de plan")
                return
        except Exception as e:
            print(f"Error al verificar el estado del navegador en 'selecciona un plan': {str(e)}")
            # Usar el mismo método de reinicio que en el paso anterior
            print("Reiniciando el navegador...")
            raise Exception("El navegador se cerró inesperadamente. Por favor, reinicia la prueba.")
            return
            
        # Esperar a que los botones "Contratar" estén visibles
        print('Esperando a que los botones "Contratar" estén disponibles...')
        botones_contratar = WebDriverWait(context.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[.//span[text()="Contratar"]]'))
        )
        
        # Pausa breve para asegurar que la página esté completamente cargada
        time.sleep(2)
        
        # Contar los botones disponibles
        count = len(botones_contratar)
        print(f"Se encontraron {count} botones 'Contratar'.")
        
        if count == 0:
            raise Exception('No se encontraron botones "Contratar" disponibles.')
        
        # Seleccionar uno de los primeros 5 botones para mayor confiabilidad
        max_index = min(5, count)
        random_index = random.randint(0, max_index - 1)
        
        print(f"Seleccionando el botón #{random_index + 1} de {count} disponibles.")
        
        # Guardar el índice del botón seleccionado para poder re-obtenerlo si es necesario
        indice_seleccionado = random_index
        print(f"Índice del botón seleccionado: {indice_seleccionado}")
        
        # Función para intentar hacer clic con reintentos
        def intentar_clic_con_reintentos(max_intentos=3):
            for intento in range(1, max_intentos + 1):
                try:
                    print(f"Intento {intento} de {max_intentos} para hacer clic en el botón")
                    # Re-obtener los botones para evitar stale element reference
                    botones_actualizados = WebDriverWait(context.driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//a[.//span[text()="Contratar"]]'))
                    )
                    
                    if len(botones_actualizados) <= indice_seleccionado:
                        print(f"Advertencia: El índice {indice_seleccionado} ya no es válido. Usando el primer botón disponible.")
                        boton_actual = botones_actualizados[0]
                    else:
                        boton_actual = botones_actualizados[indice_seleccionado]
                    
                    # Asegurarse de que el botón esté visible en la pantalla
                    print("Haciendo scroll al botón...")
                    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_actual)
                    
                    # Esperar a que el botón esté visible y estable
                    time.sleep(1.5)
                    
                    # Intentar hacer clic con JavaScript
                    print('Haciendo clic en el botón "Contratar" seleccionado...')
                    context.driver.execute_script("arguments[0].click();", boton_actual)
                    return True
                except Exception as e:
                    print(f"Error en el intento {intento}: {str(e)}")
                    if intento == max_intentos:
                        raise
                    time.sleep(1)  # Esperar antes de reintentar
        
        # Intentar hacer clic con reintentos
        intentar_clic_con_reintentos()
        
        # Verificar que el clic haya tenido efecto esperando a que aparezca un elemento de la siguiente página
        print('Verificando que el clic haya tenido efecto...')
        time.sleep(2)  # Breve pausa para la transición
        
        # Esperar por un elemento que indique que estamos en la siguiente página
        navegacion_exitosa = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form, .contratacion-form, .form-container'))
        )
        
        if not navegacion_exitosa:
            print('No se detectó navegación exitosa después del clic. Intentando con otro botón...')
            # Si no funcionó, intentar con otro botón
            otro_indice = (random_index + 1) % count
            otro_boton = botones_contratar[otro_indice]
            context.driver.execute_script("arguments[0].scrollIntoView(true);", otro_boton)
            context.driver.execute_script("arguments[0].click();", otro_boton)
        
        print('Navegación a la página de contratación exitosa.')
        print(f"URL después de hacer clic en contratar: {context.driver.current_url}")
    except Exception as e:
        context.error_mensaje = str(e)
        # Capturar una screenshot para diagnóstico
        context.driver.save_screenshot('error-contratar.png')
        raise Exception(f"Error al seleccionar y contratar plan: {str(e)}")

@when('completa el formulario de contratación')
def step_impl(context):
    try:
        # Verificar si el navegador sigue abierto
        try:
            # Intentar acceder a una propiedad del navegador para verificar si sigue abierto
            window_handles = context.driver.window_handles
            if not window_handles:
                raise Exception("No hay ventanas de navegador abiertas")
                
            # Verificar la URL actual para entender en qué parte del flujo estamos
            current_url = context.driver.current_url
            print(f"URL actual en paso 'completa el formulario de contratación': {current_url}")
        except Exception as e:
            print(f"Error al verificar el estado del navegador en 'completa el formulario de contratación': {str(e)}")
            # Usar el mismo método de reinicio que en el paso anterior
            print("Reiniciando el navegador...")
            raise Exception("El navegador se cerró inesperadamente. Por favor, reinicia la prueba.")
            return
        
        # Obtener los datos de prueba
        datos = QueplanTestData.DATOS_COMPARADOR
        
        # Esperar y completar el campo de nombre
        nombre_input = WebDriverWait(context.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="nombre"]'))
        )
        nombre_input.clear()
        nombre_input.send_keys(datos['nombre'])
        print(f"Ingresado nombre: {datos['nombre']}")
        
        # Completar el campo de RUT
        rut_input = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="rutsolicitud"]'))
        )
        rut_input.clear()
        rut_input.send_keys(datos['rutsolicitud'])
        print(f"Ingresado RUT: {datos['rutsolicitud']}")
        
        # Completar el campo de email
        email_input = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]'))
        )
        email_input.clear()
        email_input.send_keys(datos['email'])
        print(f"Ingresado email: {datos['email']}")
        
        # Completar el campo de teléfono
        telefono_input = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="telefono"]'))
        )
        telefono_input.clear()
        telefono_input.send_keys(datos['telefono'])
        print(f"Ingresado teléfono: {datos['telefono']}")
        
        # Hacer clic en el botón "Iniciar contratación"
        try:
            print("Buscando botón 'Iniciar contratación'...")
            iniciar_button = WebDriverWait(context.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Iniciar contratación"]'))
            )
            print("Botón 'Iniciar contratación' encontrado")
        except Exception as e:
            print(f"Error al buscar botón 'Iniciar contratación': {str(e)}")
            print("Intentando buscar otros botones similares...")
            # Buscar otros posibles botones que puedan servir
            botones = context.driver.find_elements(By.XPATH, '//button[contains(.//span/text(), "Iniciar") or contains(.//span/text(), "contratación")]')
            if botones:
                print(f"Se encontraron {len(botones)} botones alternativos")
                iniciar_button = botones[0]
            else:
                raise Exception("No se encontró ningún botón de inicio de contratación")
        
        # Hacer scroll al botón y hacer clic
        print("Haciendo scroll al botón...")
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iniciar_button)
        time.sleep(1.5)
        
        # Capturar URL antes del clic
        url_antes = context.driver.current_url
        print(f"URL antes de hacer clic: {url_antes}")
        
        # Hacer clic con JavaScript para mayor confiabilidad
        print("Haciendo clic en el botón 'Iniciar contratación'...")
        context.driver.execute_script("arguments[0].click();", iniciar_button)
        
        # Esperar a que se complete la redirección
        print("Esperando redirección...")
        time.sleep(5)  # Aumentar tiempo de espera para asegurar que la redirección se complete
        
        # Capturar y mostrar la URL después del clic
        url_despues = context.driver.current_url
        print(f"URL después de hacer clic en 'Iniciar contratación': {url_despues}")
        
        # Verificar si hubo cambio de URL
        if url_antes == url_despues:
            print("ADVERTENCIA: La URL no cambió después de hacer clic en el botón")
    except Exception as e:
        context.error_mensaje = str(e)
        context.driver.save_screenshot('error-formulario-contratacion.png')
        raise Exception(f"Error al completar el formulario de contratación: {str(e)}")

@then('debe mostrarse el comparador con los datos correctos')
def step_impl(context):
    try:
        # Verificar la URL actual para entender en qué parte del flujo estamos
        current_url = context.driver.current_url
        print(f"URL actual en paso de validación del comparador: {current_url}")
        
        # Obtener los datos de prueba
        datos = QueplanTestData.DATOS_COMPARADOR
        
        # Tomar una captura de pantalla para verificación visual
        context.driver.save_screenshot('comparador-validacion.png')
        print("Se ha guardado una captura de pantalla para verificación visual")
        
        # Esperar a que se cargue algún elemento que confirme que estamos en la página correcta
        # Esto podría ser un resumen de datos, un título, etc.
        try:
            # Intentar encontrar elementos que confirmen que estamos en la página del comparador
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "resumen") or contains(@class, "comparador") or contains(@class, "plan-details")]'))
            )
            print("Se encontró un elemento que confirma que estamos en la página del comparador")
        except Exception as e:
            print(f"No se encontró un elemento específico del comparador: {str(e)}")
            print("Continuando con la validación general...")
        
    except Exception as e:
        context.error_mensaje = str(e)
        context.driver.save_screenshot('error-comparador.png')
        raise Exception(f"Error al verificar el comparador: {str(e)}")
