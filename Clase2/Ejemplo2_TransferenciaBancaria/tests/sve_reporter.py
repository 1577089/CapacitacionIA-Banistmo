"""
Generador de reportes en formato SVE (Standard Verification Environment)
para resultados de test cases de transferencias bancarias.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any
import os


class SVEReporter:
    """Generador de reportes SVE para test cases."""
    
    def __init__(self, project_name: str = "Transferencias Bancarias"):
        self.project_name = project_name
        self.test_results: List[Dict[str, Any]] = []
        self.start_time = None
        self.end_time = None
        
    def add_test_result(self, 
                       test_id: str,
                       test_name: str,
                       status: str,
                       duration: float,
                       scenario: str = "",
                       expected_result: str = "",
                       actual_result: str = "",
                       error_message: str = "",
                       preconditions: str = "",
                       test_data: Dict[str, Any] = None):
        """
        Agrega un resultado de test al reporte.
        
        Args:
            test_id: ID del test case (ej: TC-01)
            test_name: Nombre del test
            status: PASS, FAIL, SKIP, ERROR
            duration: Duración en segundos
            scenario: Descripción del escenario
            expected_result: Resultado esperado
            actual_result: Resultado actual
            error_message: Mensaje de error si falló
            preconditions: Precondiciones del test
            test_data: Datos de prueba utilizados
        """
        result = {
            "test_id": test_id,
            "test_name": test_name,
            "status": status.upper(),
            "duration": round(duration, 3),
            "scenario": scenario,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "error_message": error_message,
            "preconditions": preconditions,
            "test_data": test_data or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
    
    def generate_sve_xml(self, output_file: str = "sve_report.xml"):
        """Genera reporte SVE en formato XML."""
        root = ET.Element("TestReport")
        root.set("format", "SVE")
        root.set("version", "1.0")
        
        # Metadata
        metadata = ET.SubElement(root, "Metadata")
        ET.SubElement(metadata, "Project").text = self.project_name
        ET.SubElement(metadata, "GeneratedAt").text = datetime.now().isoformat()
        ET.SubElement(metadata, "TestFramework").text = "pytest"
        
        # Summary
        summary = ET.SubElement(root, "Summary")
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        skipped = sum(1 for r in self.test_results if r["status"] == "SKIP")
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")
        
        ET.SubElement(summary, "TotalTests").text = str(total_tests)
        ET.SubElement(summary, "Passed").text = str(passed)
        ET.SubElement(summary, "Failed").text = str(failed)
        ET.SubElement(summary, "Skipped").text = str(skipped)
        ET.SubElement(summary, "Errors").text = str(errors)
        ET.SubElement(summary, "PassRate").text = f"{(passed/total_tests*100):.2f}%" if total_tests > 0 else "0%"
        
        total_duration = sum(r["duration"] for r in self.test_results)
        ET.SubElement(summary, "TotalDuration").text = f"{total_duration:.2f}s"
        
        # Test Cases
        testcases = ET.SubElement(root, "TestCases")
        
        for result in self.test_results:
            tc = ET.SubElement(testcases, "TestCase")
            tc.set("id", result["test_id"])
            tc.set("status", result["status"])
            
            ET.SubElement(tc, "Name").text = result["test_name"]
            ET.SubElement(tc, "Scenario").text = result["scenario"]
            ET.SubElement(tc, "Preconditions").text = result["preconditions"]
            ET.SubElement(tc, "ExpectedResult").text = result["expected_result"]
            ET.SubElement(tc, "ActualResult").text = result["actual_result"]
            ET.SubElement(tc, "Duration").text = f"{result['duration']:.3f}s"
            ET.SubElement(tc, "Timestamp").text = result["timestamp"]
            
            if result["error_message"]:
                ET.SubElement(tc, "ErrorMessage").text = result["error_message"]
            
            if result["test_data"]:
                test_data = ET.SubElement(tc, "TestData")
                for key, value in result["test_data"].items():
                    data_item = ET.SubElement(test_data, "DataItem")
                    data_item.set("name", key)
                    data_item.text = str(value)
        
        # Escribir archivo XML con formato
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        
        return output_file
    
    def generate_sve_json(self, output_file: str = "sve_report.json"):
        """Genera reporte SVE en formato JSON."""
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        skipped = sum(1 for r in self.test_results if r["status"] == "SKIP")
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")
        total_duration = sum(r["duration"] for r in self.test_results)
        
        report = {
            "format": "SVE",
            "version": "1.0",
            "metadata": {
                "project": self.project_name,
                "generated_at": datetime.now().isoformat(),
                "test_framework": "pytest",
                "environment": "Development"
            },
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "errors": errors,
                "pass_rate": f"{(passed/total_tests*100):.2f}%" if total_tests > 0 else "0%",
                "total_duration": f"{total_duration:.2f}s"
            },
            "test_cases": self.test_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def generate_sve_csv(self, output_file: str = "sve_report.csv"):
        """Genera reporte SVE en formato CSV."""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Test ID', 'Test Name', 'Status', 'Duration (s)',
                'Scenario', 'Expected Result', 'Actual Result',
                'Error Message', 'Timestamp'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.test_results:
                writer.writerow({
                    'Test ID': result['test_id'],
                    'Test Name': result['test_name'],
                    'Status': result['status'],
                    'Duration (s)': result['duration'],
                    'Scenario': result['scenario'],
                    'Expected Result': result['expected_result'],
                    'Actual Result': result['actual_result'],
                    'Error Message': result['error_message'],
                    'Timestamp': result['timestamp']
                })
        
        return output_file
    
    def generate_all_formats(self, base_name: str = "sve_report"):
        """Genera reportes en todos los formatos SVE."""
        files = {
            'xml': self.generate_sve_xml(f"{base_name}.xml"),
            'json': self.generate_sve_json(f"{base_name}.json"),
            'csv': self.generate_sve_csv(f"{base_name}.csv")
        }
        return files
