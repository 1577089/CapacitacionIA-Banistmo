# run_tests.ps1 - Ejecuta tests y abre el reporte HTML si existe
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Ejecutar el runner Python
python (Join-Path $scriptDir 'run_tests_and_report.py')

# Ruta del HTML
$html = Join-Path $scriptDir 'tests\test_report.html'
if (Test-Path $html) {
    Write-Host "Abriendo reporte HTML: $html"
    Start-Process $html
} else {
    Write-Host "No se encontró el reporte HTML. Mostrando report.txt:" 
    Get-Content (Join-Path $scriptDir 'tests\test_report.txt') | Out-Host
}
