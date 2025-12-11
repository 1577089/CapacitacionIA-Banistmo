import unittest
import io
import sys
import json
import time
from datetime import datetime
import html as _html
import xml.etree.ElementTree as ET
import re

START = time.time()
loader = unittest.TestLoader()
suite = loader.discover('c:\\Users\\1577089\\Desktop\\CapacitacionIA-Banistmo\\CapacitacionIA-Banistmo\\Clase3\\Caso1_CreacionClientesTestingPréstamos\\tests')

stream = io.StringIO()
runner = unittest.TextTestRunner(stream=stream, verbosity=2)
result = runner.run(suite)
END = time.time()

report = {
    'timestamp': datetime.now().isoformat(),
    'duration_seconds': round(END-START, 3),
    'testsRun': result.testsRun,
    'failures': len(result.failures),
    'errors': len(result.errors),
    'skipped': len(getattr(result, 'skipped', [])),
    'wasSuccessful': result.wasSuccessful(),
    'failures_details': [(case.id(), tb) for case, tb in result.failures],
    'errors_details': [(case.id(), tb) for case, tb in result.errors]
}

TEXT_OUT = stream.getvalue()

# write json and txt reports
JSON_PATH = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\tests\test_report.json"
TXT_PATH = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\tests\test_report.txt"
with open(JSON_PATH, 'w', encoding='utf-8') as j:
    json.dump(report, j, ensure_ascii=False, indent=2)
with open(TXT_PATH, 'w', encoding='utf-8') as t:
    t.write('UNittest report\n')
    t.write('Generated: ' + report['timestamp'] + '\n')
    t.write('Duration (s): ' + str(report['duration_seconds']) + '\n')
    t.write('Summary:\n')
    t.write(json.dumps({k:report[k] for k in ('testsRun','failures','errors','skipped','wasSuccessful')}, ensure_ascii=False, indent=2))
    t.write('\n\nFull output:\n')
    t.write(TEXT_OUT)

# HTML report (legible)
HTML_PATH = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\tests\test_report.html"
try:
    summary_json = json.dumps({k:report[k] for k in ('testsRun','failures','errors','skipped','wasSuccessful')}, ensure_ascii=False, indent=2)
    html_content = f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Unittest Report</title>
  <style>
    body{{font-family:Segoe UI,Arial,Helvetica,sans-serif;margin:20px}}
    pre{{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto}}
    .summary{{background:#fff;padding:10px;border:1px solid #e1e4e8;border-radius:6px}}
  </style>
</head>
<body>
  <h1>Unittest Report</h1>
  <p><strong>Generated:</strong> {report['timestamp']}</p>
  <p><strong>Duration (s):</strong> {report['duration_seconds']}</p>
  <h2>Summary</h2>
  <div class=\"summary\"><pre>{_html.escape(summary_json)}</pre></div>
  <h2>Full Output</h2>
  <pre>{_html.escape(TEXT_OUT)}</pre>
</body>
</html>"""
    with open(HTML_PATH, 'w', encoding='utf-8') as h:
        h.write(html_content)
except Exception as e:
    print('No se pudo escribir HTML report:', e)

print('Reportes escritos:')
print(JSON_PATH)
print(TXT_PATH)
print(HTML_PATH)

# JUnit XML generation (para CI)
JUNIT_PATH = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\tests\test_report.junit.xml"
try:
  lines = TEXT_OUT.splitlines()
  # parse lines like: "test_name (module.ClassName) ... ok"
  pattern = re.compile(r'^(?P<name>[^\s]+) \((?P<class>[^)]+)\) \.\.\. (?P<status>ok|FAIL|ERROR|skipped)$')
  testcases = []
  for ln in lines:
    m = pattern.match(ln.strip())
    if m:
      testcases.append((m.group('name'), m.group('class'), m.group('status')))

  tests = len(testcases)
  failures = sum(1 for _,_,s in testcases if s == 'FAIL')
  errors = sum(1 for _,_,s in testcases if s == 'ERROR')

  testsuite = ET.Element('testsuite', attrib={
    'name': 'unittest',
    'tests': str(tests),
    'failures': str(failures),
    'errors': str(errors),
    'time': str(report['duration_seconds']),
    'timestamp': report['timestamp']
  })

  for name, classname, status in testcases:
    tc = ET.SubElement(testsuite, 'testcase', attrib={'classname': classname, 'name': name, 'time': '0'})
    if status == 'FAIL':
      f = ET.SubElement(tc, 'failure', attrib={'message': 'failure'})
      # include any traceback in CDATA-like text
      f.text = ''
    if status == 'ERROR':
      e = ET.SubElement(tc, 'error', attrib={'message': 'error'})
      e.text = ''
    if status == 'skipped':
      ET.SubElement(tc, 'skipped')

  tree = ET.ElementTree(testsuite)
  tree.write(JUNIT_PATH, encoding='utf-8', xml_declaration=True)
  print('JUnit XML escrito:', JUNIT_PATH)
except Exception as e:
  print('No se pudo escribir JUnit XML:', e)
