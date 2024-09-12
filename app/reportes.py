import os
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from flask import Response
from app.models import Oveja, Salud, Reproduccion, Alimentacion, Inventario, Finanzas

# Directorio para archivos temporales
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

# Crear el directorio si no existe
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

def generate_excel_report(data, filename):
    df = pd.DataFrame(data)
    output_path = os.path.join(TMP_DIR, filename)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output_path


def generate_ovejas_report(file_path):
    ovejas = Oveja.query.all()
    data = [{
        'ID': o.id,
        'Nombre': o.nombre,
        'Fecha de Nacimiento': o.fecha_nacimiento,
        'Raza': o.raza,
        'Sexo': o.sexo,
        'ID Padre': o.id_padre,
        'ID Madre': o.id_madre
    } for o in ovejas]
    return generate_excel_report(data, file_path)

def generate_salud_report(file_path):
    salud = Salud.query.all()
    data = [{
        'ID': s.id,
        'Oveja ID': s.id_oveja,
        'Fecha': s.fecha,
        'Tipo de Tratamiento': s.tipo_tratamiento,
        'Detalle': s.detalle
    } for s in salud]
    return generate_excel_report(data, file_path)

def generate_reproduccion_report(file_path):
    reproduccion = Reproduccion.query.all()
    data = [{
        'ID': r.id,
        'Oveja ID': r.id_oveja,
        'Fecha de Apareamiento': r.fecha_apareamiento,
        'ID Macho': r.id_macho,
        'Fecha de Parto': r.fecha_parto,
        'Número de Crías': r.num_crias
    } for r in reproduccion]
    return generate_excel_report(data, file_path)

def generate_alimentacion_report(file_path):
    alimentacion = Alimentacion.query.all()
    data = [{
        'ID': a.id,
        'Oveja ID': a.id_oveja,
        'Fecha': a.fecha,
        'Tipo de Alimentación': a.tipo_alimento,
        'Cantidad': a.cantidad
    } for a in alimentacion]
    return generate_excel_report(data, file_path)

def generate_inventario_report(file_path):
    inventario = Inventario.query.all()
    data = [{
        'ID': i.id,
        'Tipo': i.tipo,
        'Descripción': i.descripcion,
        'Cantidad': i.cantidad,
        'Fecha de Adquisición': i.fecha_adquisicion
    } for i in inventario]
    return generate_excel_report(data, file_path)

def generate_finanzas_report(file_path):
    finanzas = Finanzas.query.all()
    data = [{
        'ID': f.id,
        'Tipo': f.tipo,
        'Descripción': f.descripcion,
        'Monto': f.monto,
        'Fecha': f.fecha
    } for f in finanzas]
    return generate_excel_report(data, file_path)

# Generar reportes en PDF
def generate_pdf_report(data, title, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    
    for row in data:
        pdf.cell(0, 10, txt=', '.join(f'{key}: {value}' for key, value in row.items()), ln=True)
    
    pdf.output(file_path)
    return file_path

def generate_ovejas_pdf_report(file_path):
    ovejas = Oveja.query.all()
    data = [{
        'ID': o.id,
        'Nombre': o.nombre,
        'Fecha de Nacimiento': o.fecha_nacimiento,
        'Raza': o.raza,
        'Sexo': o.sexo,
        'ID Padre': o.id_padre,
        'ID Madre': o.id_madre
    } for o in ovejas]
    return generate_pdf_report(data, 'Reporte de Ovejas', file_path)

def generate_salud_pdf_report(file_path):
    salud = Salud.query.all()
    data = [{
        'ID': s.id,
        'Oveja ID': s.id_oveja,
        'Fecha': s.fecha,
        'Tipo de Tratamiento': s.tipo_tratamiento,
        'Detalle': s.detalle
    } for s in salud]
    return generate_pdf_report(data, 'Reporte de Salud', file_path)

def generate_reproduccion_pdf_report(file_path):
    reproduccion = Reproduccion.query.all()
    data = [{
        'ID': r.id,
        'Oveja ID': r.id_oveja,
        'Fecha de Apareamiento': r.fecha_apareamiento,
        'ID Macho': r.id_macho,
        'Fecha de Parto': r.fecha_parto,
        'Número de Crías': r.num_crias
    } for r in reproduccion]
    return generate_pdf_report(data, 'Reporte de Reproducción', file_path)

def generate_alimentacion_pdf_report(file_path):
    alimentacion = Alimentacion.query.all()
    data = [{
        'ID': a.id,
        'Oveja ID': a.id_oveja,
        'Fecha': a.fecha,
        'Tipo de Alimentación': a.tipo_alimento,
        'Cantidad': a.cantidad
    } for a in alimentacion]
    return generate_pdf_report(data, 'Reporte de Alimentación', file_path)

def generate_inventario_pdf_report(file_path):
    inventario = Inventario.query.all()
    data = [{
        'ID': i.id,
        'Tipo': i.tipo,
        'Descripción': i.descripcion,
        'Cantidad': i.cantidad,
        'Fecha de Adquisición': i.fecha_adquisicion
    } for i in inventario]
    return generate_pdf_report(data, 'Reporte de Inventario', file_path)

def generate_finanzas_pdf_report(file_path):
    finanzas = Finanzas.query.all()
    data = [{
        'ID': f.id,
        'Tipo': f.tipo,
        'Descripción': f.descripcion,
        'Monto': f.monto,
        'Fecha': f.fecha
    } for f in finanzas]
    return generate_pdf_report(data, 'Reporte de Finanzas', file_path)
