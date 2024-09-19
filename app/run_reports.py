import os
import sys

# Asegúrate de que el directorio 'app' esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app
from app.reportes import (
    generate_ovejas_report, generate_salud_report, 
    generate_reproduccion_report, generate_alimentacion_report, 
    generate_inventario_report, generate_finanzas_report,
    generate_ovejas_pdf_report, generate_salud_pdf_report, 
    generate_reproduccion_pdf_report, generate_alimentacion_pdf_report, 
    generate_inventario_pdf_report, generate_finanzas_pdf_report
)

def run_reports():
    app = create_app()
    with app.app_context():
        generate_ovejas_report()
        generate_salud_report()
        generate_reproduccion_report()
        generate_alimentacion_report()
        generate_inventario_report()
        generate_finanzas_report()

        generate_ovejas_pdf_report()
        generate_salud_pdf_report()
        generate_reproduccion_pdf_report()
        generate_alimentacion_pdf_report()
        generate_inventario_pdf_report()
        generate_finanzas_pdf_report()

if __name__ == '__main__':
    run_reports()
