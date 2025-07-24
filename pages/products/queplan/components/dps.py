from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import dpsLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.products.queplan.locators.queplan_locators import ContratanteLocators
import time

class DpsComponent(BaseComponent):
    def dps_inputs(self):
        print("DpsComponent: Iniciando dps_inputs")
        try:
            # Primero hacemos clic en el checkbox de términos antes de procesar los radio buttons
            try:
                print("DpsComponent: Intentando aceptar términos DPS antes de procesar radio buttons")
                self.click_mat_checkbox(*ContratanteLocators.DPS_TERMINOS)
                print("DpsComponent: Términos DPS aceptados exitosamente")
            except Exception as e:
                print(f"DpsComponent: Error al aceptar términos DPS: {e}")
                print("DpsComponent: Continuando con los radio buttons")
            
            # Lista de nombres de los radio buttons DPS
            dps_radios = [
                'dps**q1', 'dps**q2', 'dps**qA2', 'dps**q3', 'dps**qA3', 'dps**q4', 'dps**qA4', 'dps**q5', 
                'dps**qA5', 'dps**q6', 'dps**qA6', 'dps**q7', 'dps**q8', 'dps**q9', 'dps**q10', 'dps**q11', 
                'dps**q12', 'dps**q13', 'dps**q14', 'dps**qA14', 'dps**q15', 'dps**q16', 'dps**q17', 'dps**q18'
            ]
            
            # Tiempo máximo de espera para cada radio button (segundos)
            timeout = 10
            wait = WebDriverWait(self.driver, timeout)
            
            for i, nombre in enumerate(dps_radios):
                try:
                    print(f"DpsComponent: Procesando pregunta {i+1}/{len(dps_radios)}: {nombre}")
                    
                    # Esperar a que el radio button esté presente en el DOM
                    xpath = f"//input[@type='radio' and @name='{nombre}' and @value='No']"                    
                    print(f"DpsComponent: Esperando que aparezca el radio button {nombre}")
                    
                    try:
                        # Buscar TODOS los radio buttons con el mismo nombre y value="No"
                        radios_no = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                        print(f"DpsComponent: Encontrados {len(radios_no)} radio buttons para {nombre}")
                        
                        # Esperar un poco para asegurar que la UI esté lista
                        time.sleep(0.5)
                        
                        # Contador para saber cuántos botones se clickearon
                        botones_clickeados = 0
                        
                        # Procesar cada radio button encontrado
                        for idx, radio_no in enumerate(radios_no):
                            try:
                                # Verificar si está visible usando JavaScript (más confiable)
                                is_visible = self.driver.execute_script(
                                    "return arguments[0].offsetParent !== null && "
                                    "arguments[0].offsetWidth > 0 && "
                                    "arguments[0].offsetHeight > 0 && "
                                    "window.getComputedStyle(arguments[0]).visibility !== 'hidden';", 
                                    radio_no
                                )
                                
                                if is_visible:
                                    print(f"DpsComponent: Radio button {nombre} #{idx+1} encontrado y visible")
                                    
                                    # Hacer scroll hasta el elemento
                                    self._scroll_to(radio_no)
                                    
                                    # Intentar hacer clic usando JavaScript (más confiable para Angular Material)
                                    self.driver.execute_script("arguments[0].click();", radio_no)
                                    print(f"DpsComponent: Clickeado radio button {nombre} #{idx+1}")
                                    botones_clickeados += 1
                                    
                                    # Esperar un momento después de cada clic
                                    time.sleep(0.5)
                                else:
                                    print(f"DpsComponent: Radio button {nombre} #{idx+1} presente pero no visible")
                            except Exception as e:
                                print(f"DpsComponent: Error al procesar radio button {nombre} #{idx+1}: {e}")
                        
                        if botones_clickeados > 0:
                            print(f"DpsComponent: Se clickearon {botones_clickeados} botones para {nombre}")
                            # Esperar a que la UI se actualice después de los clics
                            time.sleep(1)
                        else:
                            print(f"DpsComponent: No se pudo clickear ningún botón para {nombre}")
                            # Si no se pudo clickear ningún botón y es el primero, es un error crítico
                            if i == 0:
                                raise Exception(f"No se pudo clickear ningún botón para {nombre}")
                        
                            
                    except Exception as e:
                        print(f"DpsComponent: Timeout esperando radio button {nombre}: {e}")
                        # Si es el primer radio button y no aparece, es un error crítico
                        if i == 0:
                            raise Exception(f"El primer radio button {nombre} no apareció: {e}")
                        # Si no es el primero, podría ser que ya no hay más preguntas
                        print(f"DpsComponent: Posiblemente no hay más preguntas después de la {i}")
                        break
                        
                except Exception as e:
                    print(f"DpsComponent: Error al procesar radio button {nombre}: {e}")
                    # Si es un error en el primer radio button, es crítico
                    if i == 0:
                        raise
            
            print("DpsComponent: Proceso de clic en radio buttons completado")
            
            # Aceptar los términos DPS al final del proceso
            print("DpsComponent: Aceptando términos DPS")
            # Esperar un momento para que la UI se estabilice completamente después de los radio buttons
            time.sleep(2)
            
        except Exception as e:
            print(f"DpsComponent: Error general en dps_inputs: {e}")
            raise
            
    def hacer_clic_siguiente_paso(self):
        """
        Hace clic en el botón 'Siguiente paso' después de aceptar los términos y condiciones.
        """
        try:
            print("DpsComponent: Haciendo clic en el botón 'Siguiente paso'")
            # Utilizamos el localizador del botón siguiente desde PagoLocators
            from pages.products.queplan.locators.queplan_locators import PagoLocators
            
            # Esperamos un momento para asegurar que la página esté lista
            import time
            time.sleep(1)
            
            # Hacemos scroll hasta el botón y hacemos clic
            self.click(*PagoLocators.BOTON_SIGUIENTE)
            print("DpsComponent: Se hizo clic exitosamente en 'Siguiente paso'")
            
            # Esperamos un momento para que la página responda al clic
            time.sleep(1)
            return True
        except Exception as e:
            print(f"DpsComponent: Error al hacer clic en 'Siguiente paso': {e}")
            return False
