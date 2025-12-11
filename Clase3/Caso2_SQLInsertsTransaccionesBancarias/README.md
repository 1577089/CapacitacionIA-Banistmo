# Proyecto: Generador de Datos Sintéticos y Pruebas de Carga para Transacciones Bancarias

Este proyecto contiene un conjunto de scripts para generar datos sintéticos de transacciones bancarias y un sistema de pruebas automatizadas para validar la carga de estos datos en una base de datos.

## 1. Descripción del Proyecto

El objetivo principal es simular una carga masiva de datos para realizar pruebas de performance en un sistema bancario. El sistema genera un archivo `.sql` con 10,000 sentencias `INSERT` que representan movimientos históricos, siguiendo un conjunto de reglas de negocio específicas.

Adicionalmente, se ha desarrollado una suite de pruebas automatizadas para verificar la integridad, consistencia y correctitud de los datos cargados, culminando con la generación de un reporte de resultados en formato HTML.

## 2. Características Implementadas

*   **Generación de Datos Sintéticos:** Creación de un script en Python (`generar_transacciones.py`) que produce 10,000 registros de transacciones bancarias con datos realistas y distribuciones estadísticas definidas.
*   **Definición de Casos de Prueba:** Documentación de escenarios de prueba positivos, negativos y de borde en `casos_de_prueba_carga_datos.md`.
*   **Automatización de Pruebas:** Implementación de una suite de tests con `pytest` (`test_carga_transacciones.py`) que valida automáticamente los datos cargados.
*   **Entorno de Pruebas Aislado:** Uso de una base de datos en memoria (SQLite) para que las pruebas se ejecuten de forma rápida y sin dependencias de sistemas externos como Docker o PostgreSQL.
*   **Generación de Reportes:** Creación de un informe de resultados de pruebas en formato HTML (`reporte_tests.html`) para una fácil visualización y análisis.

## 3. Estructura del Proyecto

```
/Caso2_SQLInsertsTransaccionesBancarias
|
|-- generar_transacciones.py      # Script principal para generar los datos SQL.
|-- carga_transacciones.sql       # Archivo SQL con 10,000 INSERTs (generado).
|-- queries_transacciones.txt     # Copia en texto plano de los queries.
|
|-- test_carga_transacciones.py   # Script con los casos de prueba automatizados.
|-- casos_de_prueba_carga_datos.md # Documento con la definición de los casos de prueba.
|-- requirements.txt              # Dependencias de Python para el proyecto.
|
|-- reporte_tests.html            # Reporte final de la ejecución de pruebas (generado).
|-- README.md                     # Este archivo.
```

## 4. Configuración y Uso

Sigue estos pasos para configurar el entorno y ejecutar los diferentes componentes del proyecto.

### 4.1. Prerrequisitos

*   Tener Python 3.x instalado.

### 4.2. Instalación de Dependencias

1.  Abre una terminal en el directorio del proyecto.
2.  Instala las librerías necesarias ejecutando:

    ```bash
    pip install -r requirements.txt
    ```

### 4.3. Generación de Datos

Para generar (o regenerar) el archivo `carga_transacciones.sql` con 10,000 nuevos registros:

```bash
python generar_transacciones.py
```

Esto creará el archivo `carga_transacciones.sql` en el mismo directorio.

### 4.4. Ejecución de Pruebas Automatizadas

La suite de pruebas utiliza una base de datos SQLite temporal que se crea y destruye automáticamente, por lo que no se necesita ninguna configuración adicional.

Para ejecutar los tests y ver los resultados en la terminal:

```bash
pytest -v
```

### 4.5. Generación del Reporte HTML

Para ejecutar los tests y generar el informe `reporte_tests.html`:

```bash
pytest --html=reporte_tests.html --self-contained-html
```

Una vez generado, puedes abrir el archivo `reporte_tests.html` en cualquier navegador web para ver un resumen detallado de la ejecución, incluyendo el resultado y tiempo de cada test.
