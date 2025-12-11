"""
Script para ejecutar suite completa de pruebas con reportes
"""
import subprocess
import sys
from datetime import datetime


def run_tests(markers=None, verbose=True):
    """
    Ejecutar suite de pruebas
    
    Args:
        markers: Lista de markers a ejecutar (critical, high, medium)
        verbose: Ejecutar en modo verbose
    """
    cmd = ["pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if markers:
        marker_str = " or ".join(markers)
        cmd.extend(["-m", marker_str])
    
    # Agregar opciones adicionales
    cmd.extend([
        "--tb=short",
        "-ra",
        "--color=yes"
    ])
    
    print(f"\n{'='*80}")
    print(f"Ejecutando pruebas: {' '.join(cmd)}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        priority = sys.argv[1].lower()
        
        if priority == "critical":
            return run_tests(markers=["critical"])
        elif priority == "high":
            return run_tests(markers=["critical", "high"])
        elif priority == "all":
            return run_tests()
        elif priority == "smoke":
            return run_tests(markers=["smoke"])
        elif priority == "regression":
            return run_tests(markers=["regression"])
        else:
            print(f"Prioridad desconocida: {priority}")
            print("Opciones: critical, high, all, smoke, regression")
            return 1
    else:
        # Por defecto ejecutar todas
        return run_tests()


if __name__ == "__main__":
    sys.exit(main())
