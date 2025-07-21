.PHONY: install test test-with-report run clean generate-report serve-report help

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
BEHAVE = $(VENV)/bin/behave
ALLURE = allure

# Directorios
ALLURE_RESULTS = allure-results
ALLURE_REPORT = allure-report

# Comandos por defecto
help:
	@echo "Comandos disponibles:"
	@echo "  make install           - Instala las dependencias"
	@echo "  make test             - Ejecuta las pruebas con behave"
	@echo "  make test-with-report - Ejecuta pruebas y genera reporte HTML"
	@echo "  make generate-report  - Genera el reporte de Allure"
	@echo "  make serve-report     - Sirve el reporte de Allure localmente"
	@echo "  make open-report      - Abre el reporte generado"
	@echo "  make clean            - Limpia archivos generados"

# Instalar dependencias
install:
	python3 -m venv $(VENV) || python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirement.txt
	$(PIP) install allure-behave

# Crear directorio de resultados
$(ALLURE_RESULTS):
	mkdir -p $(ALLURE_RESULTS)

# Ejecutar pruebas con Allure
test: $(ALLURE_RESULTS)
	$(BEHAVE) -f allure_behave.formatter:AllureFormatter -o $(ALLURE_RESULTS) features/

# Ejecutar pruebas y generar reporte HTML
test-with-report: test generate-report open-report

# Generar reporte de Allure
generate-report: $(ALLURE_RESULTS)
	$(ALLURE) generate $(ALLURE_RESULTS) -o $(ALLURE_REPORT) --clean

# Servir reporte de Allure localmente
serve-report:
	$(ALLURE) serve $(ALLURE_RESULTS)

# Abrir el reporte generado
open-report:
	@if [ -d "$(ALLURE_REPORT)" ]; then \
		echo "Abriendo el reporte en el navegador..."; \
		open "$(ALLURE_REPORT)/index.html" || xdg-open "$(ALLURE_REPORT)/index.html" || start "" "$(ALLURE_REPORT)/index.html"; \
	else \
		echo "Error: Primero genera el reporte con 'make generate-report'"; \
		exit 1; \
	fi

# Limpiar archivos generados
clean:
	rm -rf __pycache__ \
	   .pytest_cache \
	   $(ALLURE_REPORT) \
	   $(ALLURE_RESULTS) \
	   chromedriver.log
	find . -type d -name "__pycache__" -exec rm -r {} +

# Comando para ejecutar pruebas específicas
test-%: $(ALLURE_RESULTS)
	$(BEHAVE) -f allure_behave.formatter:AllureFormatter -o $(ALLURE_RESULTS) features/$*.feature
