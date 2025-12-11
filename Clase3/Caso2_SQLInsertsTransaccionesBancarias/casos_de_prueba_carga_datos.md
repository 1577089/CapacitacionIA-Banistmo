# Casos de Prueba: Carga Masiva de Transacciones

**Proyecto:** Sistema Core Bancario - Testing de Performance
**Funcionalidad:** Carga masiva de datos de transacciones desde un archivo SQL.
**Fecha:** 2025-12-11

---

## 1. Escenarios Positivos (Happy Path)

| ID | Escenario | Pasos de Prueba | Resultado Esperado |
| :-- | :--- | :--- | :--- |
| **CP-001** | **Carga exitosa del script completo** | 1. Conectar a la base de datos PostgreSQL. <br> 2. Ejecutar el script `carga_transacciones.sql`. <br> 3. Verificar el log de ejecución. | El script se ejecuta completamente sin errores. La base de datos reporta 10,000 filas insertadas en la tabla `transacciones`. |
| **CP-002** | **Verificación de conteo de registros** | 1. Ejecutar `SELECT COUNT(*) FROM transacciones;`. | El resultado es exactamente 10,000. |
| **CP-003** | **Validación de integridad de datos (Tipos y Formatos)** | 1. Seleccionar una muestra aleatoria de 100 registros. <br> 2. Verificar que `id_transaccion` siga el formato "TRX-YYYYMMDD-NNNNN". <br> 3. Verificar que `fecha_hora` sea un TIMESTAMP válido. <br> 4. Verificar que `monto` sea un DECIMAL(15,2). <br> 5. Verificar que `id_cuenta_origen` y `id_cuenta_destino` sigan el formato "ACC-NNNNN". | Todos los campos en la muestra cumplen con los tipos de datos y formatos definidos. No hay valores nulos en columnas no permitidas. |
| **CP-004** | **Validación de reglas de negocio (Distribución)** | 1. Ejecutar queries para contar la distribución de `tipo_transaccion`, `estado` y `canal`. | Las distribuciones se aproximan a las definidas: <br> - `tipo_transaccion`: ~40% TRANSFERENCIA, ~25% DEPOSITO, etc. <br> - `estado`: ~85% EXITOSA, ~10% PENDIENTE, etc. <br> - `canal`: ~50% APP_MOVIL, ~30% WEB, etc. |
| **CP-005** | **Validación de regla de negocio (Cuentas)** | 1. Ejecutar `SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion = 'TRANSFERENCIA' AND id_cuenta_origen = id_cuenta_destino;`. <br> 2. Ejecutar `SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion IN ('DEPOSITO', 'RETIRO') AND id_cuenta_destino IS NOT NULL;`. | Ambos queries deben devolver 0. |
| **CP-006** | **Validación de regla de negocio (Límite diario)** | 1. Ejecutar `SELECT id_cuenta_origen, DATE(fecha_hora), COUNT(*) FROM transacciones GROUP BY id_cuenta_origen, DATE(fecha_hora) HAVING COUNT(*) > 50;`. | El query no debe devolver ningún registro. |
| **CP-007** | **Validación de rangos de montos** | 1. Ejecutar queries para verificar que los montos de las transacciones estén dentro de los rangos especificados para cada `tipo_transaccion`. | Todos los montos están dentro de los rangos correctos. Por ejemplo, no hay 'RETIRO' por más de $3,000,000. |
| **CP-008** | **Validación de orden cronológico** | 1. Seleccionar los primeros 10 y los últimos 10 registros ordenados por `id_transaccion`. <br> 2. Verificar que las `fecha_hora` de los primeros registros sean más antiguas que las de los últimos. | Las fechas están ordenadas cronológicamente de manera ascendente. |

---

## 2. Escenarios Negativos

| ID | Escenario | Pasos de Prueba | Resultado Esperado |
| :-- | :--- | :--- | :--- |
| **CN-001** | **Intento de carga con ID de transacción duplicado** | 1. Modificar el script `carga_transacciones.sql` para duplicar un `id_transaccion`. <br> 2. Intentar ejecutar el script modificado. | La ejecución del script falla en la línea del INSERT duplicado debido a una violación de la restricción de clave primaria (Primary Key). La transacción debe ser rechazada y no insertada. |
| **CN-002** | **Intento de carga con tipo de dato incorrecto** | 1. Modificar el script para cambiar un valor de `monto` a un texto (ej. 'cien mil'). <br> 2. Intentar ejecutar el script. | La ejecución falla en la línea del INSERT modificado debido a un error de tipo de dato. La transacción es rechazada. |
| **CN-003** | **Intento de carga con valor nulo en campo obligatorio** | 1. Modificar el script para establecer `id_cuenta_origen` como `NULL` en una fila. <br> 2. Intentar ejecutar el script. | La ejecución falla debido a una violación de la restricción `NOT NULL`. La transacción es rechazada. |
| **CN-004** | **Intento de carga violando regla de negocio (Transferencia a misma cuenta)** | 1. Crear manualmente una sentencia `INSERT` donde `id_cuenta_origen` sea igual a `id_cuenta_destino`. <br> 2. Ejecutar la sentencia. | La base de datos debería rechazar el `INSERT` si existe un `CHECK CONSTRAINT` para esta regla. Si no existe, el `INSERT` será exitoso (lo cual indicaría una debilidad en el DDL). |

---

## 3. Escenarios Alternos y de Borde

| ID | Escenario | Pasos de Prueba | Resultado Esperado |
| :-- | :--- | :--- | :--- |
| **CA-001** | **Carga de un archivo SQL vacío** | 1. Crear un archivo `.sql` vacío. <br> 2. Ejecutar el script en la base de datos. | El script se ejecuta sin errores. No se inserta ninguna fila. El conteo de la tabla `transacciones` no cambia. |
| **CA-002** | **Rendimiento de la carga (Performance)** | 1. Medir el tiempo total que toma la ejecución completa del script `carga_transacciones.sql`. | El tiempo de ejecución se registra como una línea base para futuras pruebas de performance. (Ej: "La carga de 10,000 registros tomó X segundos"). |
| **CA-003** | **Comportamiento transaccional (Rollback)** | 1. Crear un script con 100 `INSERTs` válidos y un `INSERT` inválido en el medio (ej. en la posición 50). <br> 2. Envolver la ejecución en un bloque de transacción (`BEGIN; ... COMMIT;`). <br> 3. Ejecutar el script. | La transacción completa debe fallar y realizar un `ROLLBACK`. Ninguno de los 100 registros debe ser insertado en la tabla. |
| **CA-004** | **Carga con caracteres especiales en descripción** | 1. Modificar el script para incluir caracteres especiales, acentos y comillas en el campo `descripcion`. <br> 2. Ejecutar el script. | El script se ejecuta correctamente, demostrando que el `escaping` de caracteres (ej. comillas simples) funciona y los datos se almacenan sin corrupción. |
