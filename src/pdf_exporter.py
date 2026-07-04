import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable, Table, TableStyle
from xml.sax.saxutils import escape

class PDFExporter:
    """Genera el PDF de salida adaptado utilizando rutas locales."""

    COLOR_PRIMARIO = colors.HexColor("#2E5EAA")
    COLOR_SECUNDARIO = colors.HexColor("#6C757D")

    def __init__(self, logo_path: str = "imagenes/logo_app.png"):
        self.logo_path = logo_path
        self.estilos = self._crear_estilos()

    def _crear_estilos(self) -> dict:
        """Define los estilos de texto que se usan en el PDF (título, subtítulo, cuerpo, etc.)."""
        base = getSampleStyleSheet()
        return {
            "titulo": ParagraphStyle(
                "titulo", parent=base["Title"], fontName="Helvetica-Bold",
                fontSize=20, leading=24, textColor=self.COLOR_PRIMARIO,
                alignment=TA_CENTER, spaceAfter=6
            ),
            "subtitulo": ParagraphStyle(
                "subtitulo", parent=base["Normal"], fontName="Helvetica",
                fontSize=12, leading=16, textColor=self.COLOR_SECUNDARIO,
                alignment=TA_CENTER, spaceAfter=4
            ),
            "seccion": ParagraphStyle(
                "seccion", parent=base["Heading2"], fontName="Helvetica-Bold",
                fontSize=13, leading=16, textColor=colors.white,
                alignment=TA_CENTER
            ),
            "cuerpo": ParagraphStyle(
                "cuerpo", parent=base["Normal"], fontName="Helvetica",
                fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=14
            ),
        }

    def _etiqueta_seccion(self, texto: str) -> Table:
        """Franja de color con el título de la sección dentro (como una 'card header')."""
        tabla = Table([[Paragraph(texto, self.estilos["seccion"])]], colWidths=[16.2 * cm])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.COLOR_PRIMARIO),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        return tabla

    def _pie_pagina(self, canvas_obj, doc):
        """Pie de página que se repite en todas las hojas del PDF (línea, texto y número de página)."""
        canvas_obj.saveState()
        canvas_obj.setStrokeColor(self.COLOR_SECUNDARIO)
        canvas_obj.line(2.2 * cm, 1.6 * cm, doc.pagesize[0] - 2.2 * cm, 1.6 * cm)

        canvas_obj.setFont("Helvetica-Oblique", 8)
        canvas_obj.setFillColor(self.COLOR_SECUNDARIO)
        canvas_obj.drawString(2.2 * cm, 1.2 * cm, "Generado por PAEdu · Plataforma de Accesibilidad Educativa")
        canvas_obj.drawRightString(doc.pagesize[0] - 2.2 * cm, 1.2 * cm, f"Página {doc.page}")
        canvas_obj.restoreState()

    def exportar_pdf(self, texto_original: str, texto_resultado: str, modo: str) -> str:
        """Genera el PDF final con el texto original y el texto adaptado."""
        nombre_archivo = f"PAEdu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta = os.path.abspath(nombre_archivo)

        doc = SimpleDocTemplate(
            ruta, pagesize=letter,
            topMargin=2.3 * cm, bottomMargin=2.3 * cm,
            leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        )

        elementos = []

        # Usar el logo local si existe
        if os.path.exists(self.logo_path):
            try:
                elementos.append(Image(self.logo_path, width=3 * cm, height=3 * cm, hAlign="CENTER"))
                elementos.append(Spacer(1, 8))
            except Exception:
                pass  # si no encuentra el logo, sigue sin romper el documento

        # Cabecera
        elementos.append(Paragraph("ASISTENTE EDUCATIVO INCLUSIVO", self.estilos["titulo"]))
        elementos.append(Paragraph(f"Modo de adaptación: <b>{escape(modo)}</b>", self.estilos["subtitulo"]))
        elementos.append(HRFlowable(width="100%", thickness=1, color=self.COLOR_SECUNDARIO, spaceAfter=18))

        # Texto original
        elementos.append(self._etiqueta_seccion("TEXTO ORIGINAL"))
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(escape(texto_original).replace("\n", "<br/>"), self.estilos["cuerpo"]))
        elementos.append(Spacer(1, 16))

        # Texto adaptado
        elementos.append(self._etiqueta_seccion("TEXTO ADAPTADO"))
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(escape(texto_resultado).replace("\n", "<br/>"), self.estilos["cuerpo"]))

        doc.build(elementos, onFirstPage=self._pie_pagina, onLaterPages=self._pie_pagina)
        return ruta
