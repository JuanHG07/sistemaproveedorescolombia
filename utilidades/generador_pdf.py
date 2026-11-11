import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from config.configuracion import RAIZ
from utilidades.constantes import CARPETA_REPORTES

AZUL = colors.HexColor("#1F4E79")
DORADO = colors.HexColor("#C9A227")
GRIS = colors.HexColor("#5B6B7B")
LOGO = RAIZ / "recursos" / "imagenes" / "logo_256.png"


def generar_pdf(titulo, encabezados, filas, nombre_archivo, filtros_txt="",
                carpeta=CARPETA_REPORTES, usuario=""):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"{nombre_archivo}_{datetime.now():%Y%m%d_%H%M%S}.pdf")
    doc = SimpleDocTemplate(ruta, pagesize=landscape(A4), leftMargin=1.5 * cm,
                            rightMargin=1.5 * cm, topMargin=1.2 * cm, bottomMargin=1.5 * cm,
                            title=titulo, author="SPC - Sistema de Proveedores Colombianos")
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle("titulo", parent=estilos["Title"], textColor=AZUL,
                                   alignment=0, fontSize=18, spaceAfter=2)
    estilo_sub = ParagraphStyle("sub", parent=estilos["Normal"], textColor=GRIS, fontSize=9)
    estilo_celda = ParagraphStyle("celda", parent=estilos["Normal"], fontSize=8, leading=10)
    estilo_cabecera = ParagraphStyle("cabecera", parent=estilo_celda, textColor=colors.white,
                                     fontName="Helvetica-Bold")

    cabecera = Table([[Image(str(LOGO), width=1.6 * cm, height=1.6 * cm),
                       [Paragraph(titulo, estilo_titulo),
                        Paragraph("SPC - Sistema de Proveedores Colombianos", estilo_sub)]]],
                     colWidths=[2 * cm, None])
    cabecera.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                  ("LINEBELOW", (0, 0), (-1, 0), 1.5, DORADO),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))

    detalle = f"Filtros: {filtros_txt or 'Sin filtros'}"
    generado = f"Generado el {datetime.now():%d/%m/%Y a las %I:%M %p}"
    if usuario:
        generado += f" por {usuario}"
    elementos = [cabecera, Spacer(1, 8), Paragraph(detalle, estilo_sub),
                 Paragraph(f"{generado} · {len(filas)} registros", estilo_sub), Spacer(1, 10)]

    datos = [[Paragraph(str(e), estilo_cabecera) for e in encabezados]]
    datos += [[Paragraph("" if c is None else str(c), estilo_celda) for c in f] for f in filas]
    if not filas:
        datos.append([Paragraph("No hay registros para los filtros seleccionados.", estilo_celda)]
                     + [""] * (len(encabezados) - 1))
    tabla = Table(datos, repeatRows=1, colWidths=[doc.width / len(encabezados)] * len(encabezados))
    estilo_tabla = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3DCE6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF3F8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if not filas:
        estilo_tabla.append(("SPAN", (0, 1), (-1, 1)))
    tabla.setStyle(TableStyle(estilo_tabla))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=_pie, onLaterPages=_pie)
    return ruta


def _pie(lienzo, doc):
    lienzo.saveState()
    lienzo.setFont("Helvetica", 8)
    lienzo.setFillColor(GRIS)
    lienzo.drawString(doc.leftMargin, 0.8 * cm, "SPC - Sistema de Proveedores Colombianos")
    lienzo.drawRightString(doc.pagesize[0] - doc.rightMargin, 0.8 * cm, f"Página {doc.page}")
    lienzo.restoreState()
