from pages.products.queplan.components.base_component import BaseComponent
from pages.products.queplan.locators.queplan_locators import dpsLocators

class DpsComponent(BaseComponent):
    def dps_inputs(self):
        """
        Selecciona todos los botones de radio con valor "No" que están visibles.
        Implementación directa basada en el código de Playwright.
        """
        print("DpsComponent: Iniciando dps_inputs")
        try:
            # Conjunto para evitar duplicados
            ids_procesados = set()
            ids_botones_no = []
            
            # Encontrar todos los contenedores formly-field
            print("DpsComponent: Buscando contenedores formly-field")
            contenedores = self.driver.find_elements(By.CSS_SELECTOR, 'formly-field')
            print(f"DpsComponent: Encontrados {len(contenedores)} contenedores")
            
            for i, contenedor in enumerate(contenedores):
                try:
                    # Verificar si el contenedor está oculto
                    estilo = self.driver.execute_script("return arguments[0].style.display", contenedor)
                    if estilo == "none":
                        continue
                        
                    # Buscar botones de radio con valor "No" dentro del contenedor
                    botones_no = contenedor.find_elements(By.CSS_SELECTOR, 'input[type="radio"][value="No"]')
                    print(f"DpsComponent: Contenedor {i} tiene {len(botones_no)} botones No")
                    
                    for boton in botones_no:
                        id_boton = boton.get_attribute('id')
                        
                        # Filtrar solo IDs que contienen "mat-radio"
                        if id_boton and "mat-radio" in id_boton and id_boton not in ids_procesados:
                            # Verificar si el botón es visible
                            try:
                                es_visible = boton.is_displayed()
                                ids_botones_no.append({"id": id_boton, "visible": es_visible})
                                ids_procesados.add(id_boton)
                                print(f"DpsComponent: Botón encontrado - ID: {id_boton}, Visible: {es_visible}")
                            except Exception as e:
                                print(f"DpsComponent: Error al verificar visibilidad: {e}")
                except Exception as e:
                    print(f"DpsComponent: Error procesando contenedor {i}: {e}")
            
            print(f"DpsComponent: Total botones 'No' encontrados: {len(ids_botones_no)}")
            
            # Hacer clic en los botones encontrados
            for boton_info in ids_botones_no:
                id_boton = boton_info["id"]
                try:
                    # Buscar el botón por ID
                    selector = f"#{id_boton}"
                    boton = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if boton.is_displayed():
                        # Hacer scroll hasta el botón
                        self._scroll_to(boton)
                        
                        # Intentar hacer clic usando JavaScript (más confiable para Angular Material)
                        self.driver.execute_script("arguments[0].click();", boton)
                        print(f"DpsComponent: Clickeado botón {id_boton}")
                        
                        # Esperar un momento entre clics
                        import time
                        time.sleep(0.5)
                    else:
                        print(f"DpsComponent: Botón no visible: {id_boton}")
                        
                except Exception as e:
                    print(f"DpsComponent: Error al hacer clic en {id_boton}: {e}")
            
            print("DpsComponent: Proceso de clic completado")
            
        except Exception as e:
            print(f"DpsComponent: Error general en dps_inputs: {e}")
            raise

