import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from utilidades.constantes import CARPETA_REPORTES


def generar_pdf(titulo, encabezados, filas, nombre_archivo, filtros_txt=""):
    """Crea un PDF tabular y devuelve la ruta."""
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta = os.path.join(CARPETA_REPORTES, f"{nombre_archivo}_{datetime.now():%Y%m%d_%H%M%S}.pdf")
    doc = SimpleDocTemplate(ruta, pagesize=landscape(A4))
    est = getSampleStyleSheet()
    elementos = [Paragraph(titulo, est["Title"])]
    if filtros_txt:
        elementos.append(Paragraph(f"Filtros: {filtros_txt}", est["Normal"]))
    elementos.append(Spacer(1, 12))
    datos = [encabezados] + [[str(c) if c is not None else "" for c in f] for f in filas]
    tabla = Table(datos, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF3F8")]),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabla)
    doc.build(elementos)
    return ruta
