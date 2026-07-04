import fitz  # PyMuPDF

class PDFReader:
    """Lee el contenido de texto de un archivo PDF."""

    @staticmethod
    def leer_pdf(file) -> str:
        if file is None:
            return ""

        # Obtener la ruta del archivo, ya sea 'file' una ruta o un objeto de archivo
        file_path = file if isinstance(file, str) else file.name
        doc = fitz.open(file_path)
        texto = ""

        for page in doc:
            texto += page.get_text()

        doc.close()
        return texto.strip()
