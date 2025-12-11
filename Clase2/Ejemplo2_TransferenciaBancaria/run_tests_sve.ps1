# Script para ejecutar tests y generar reportes SVE
# Ejecutar como: .\run_tests_sve.ps1

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TESTS AUTOMATIZADOS + REPORTES SVE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Configurar variables de entorno
$env:AUTH_TOKEN = "Bearer test"
$env:PYTHONPATH = (Get-Location).Path

Write-Host "[OK] Variables de entorno configuradas" -ForegroundColor Green
Write-Host "   AUTH_TOKEN: $env:AUTH_TOKEN" -ForegroundColor Gray
Write-Host ""

# Limpiar reportes anteriores
Write-Host "Limpiando reportes anteriores..." -ForegroundColor Yellow
Remove-Item -Path "sve_report.*" -ErrorAction SilentlyContinue
Remove-Item -Path ".pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".coverage" -ErrorAction SilentlyContinue
Write-Host "[OK] Limpieza completada" -ForegroundColor Green
Write-Host ""

# Ejecutar tests
Write-Host "Ejecutando suite de tests..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host ""

pytest -v --tb=short

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "=============================================" -ForegroundColor Gray

if ($exitCode -eq 0) {
    Write-Host "[OK] TESTS COMPLETADOS EXITOSAMENTE" -ForegroundColor Green
} else {
    Write-Host "[WARNING] TESTS COMPLETADOS CON ERRORES (Exit code: $exitCode)" -ForegroundColor Yellow
}

Write-Host ""

# Verificar si se generaron los reportes SVE
Write-Host "Verificando reportes SVE generados:" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray

$reportFiles = @("sve_report.xml", "sve_report.json", "sve_report.csv")
$allGenerated = $true

foreach ($file in $reportFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "   [OK] $file - $size bytes" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] $file (NO GENERADO)" -ForegroundColor Red
        $allGenerated = $false
    }
}

Write-Host "=============================================" -ForegroundColor Gray
Write-Host ""

if ($allGenerated) {
    Write-Host "PROCESO COMPLETADO - Todos los reportes SVE generados" -ForegroundColor Green
    Write-Host ""
    Write-Host "Archivos disponibles:" -ForegroundColor Cyan
    Write-Host "   - sve_report.xml  (Formato XML estandar)" -ForegroundColor White
    Write-Host "   - sve_report.json (Formato JSON para APIs)" -ForegroundColor White
    Write-Host "   - sve_report.csv  (Formato CSV para Excel)" -ForegroundColor White
    Write-Host ""
    Write-Host "Puedes abrir los reportes con:" -ForegroundColor Yellow
    Write-Host "   - XML:  notepad sve_report.xml" -ForegroundColor Gray
    Write-Host "   - JSON: code sve_report.json" -ForegroundColor Gray
    Write-Host "   - CSV:  start sve_report.csv (abre en Excel)" -ForegroundColor Gray
} else {
    Write-Host "ADVERTENCIA: No se generaron todos los reportes" -ForegroundColor Yellow
    Write-Host "   Verifica que los tests se hayan ejecutado correctamente" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
