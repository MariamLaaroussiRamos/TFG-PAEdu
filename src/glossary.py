import spacy
from wordfreq import zipf_frequency
from text_simplifier import TextSimplifier

class GlosarioGenerator:
    """Detecta palabras poco frecuentes y genera un glosario de definiciones simples."""

    def __init__(self, simplifier: TextSimplifier, umbral_frecuencia: float = 3.3):
        self.simplifier = simplifier
        self.umbral_frecuencia = umbral_frecuencia
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("Por favor descarga el modelo de spacy ejecutando: python -m spacy download en_core_web_sm")

    def detectar_palabras_dificiles(self, texto: str) -> list:
        """Recorre el texto y busca sustantivos poco frecuentes (candidatos a glosario)."""
        doc = self.nlp(texto)
        dificiles = []
        vistas = set()

        for token in doc:
            palabra = token.text.lower()

            # el problema esta en los sustantivos por lo que filtro
            if token.pos_ not in ("NOUN", "PROPN"):
                continue

            if palabra in vistas or len(palabra) < 4:
                continue

            if zipf_frequency(palabra, "en") < self.umbral_frecuencia:
                dificiles.append(palabra)
                vistas.add(palabra)

        return dificiles

    @staticmethod
    def es_definicion_valida(palabra: str, definicion: str) -> bool:
        """Comprueba que la definición generada por el modelo tiene sentido (no vacía ni circular)."""
        definicion_lower = definicion.lower().strip()
        palabra_lower = palabra.lower()

        # Vacía o sospechosamente corta
        if len(definicion_lower.split()) < 3:
            return False

        # Circular: repite la palabra como parte central de la definición
        if definicion_lower == palabra_lower or definicion_lower.startswith(palabra_lower):
            return False

        return True

    def generar_glosario(self, texto: str) -> dict:
        """Genera el diccionario {palabra: definición} para las palabras difíciles del texto."""
        palabras = self.detectar_palabras_dificiles(texto)
        glosario = {}

        for palabra in palabras:
            prompt = f"""Explain the word in very simple words, like talking to a child.
        Do not repeat the word in your answer. Use one short sentence.

        Word: sun
        Explanation: It is the bright light in the sky during the day.

        Word: bicycle
        Explanation: It is a vehicle with two wheels that you ride by pedaling.

        Word: {palabra}
        Explanation:"""

            explicacion = self.simplifier._generar_respuesta(prompt).strip()

            if not self.es_definicion_valida(palabra, explicacion):
                explicacion = "(Simple explanation not available for this word)"

            glosario[palabra] = explicacion

        return glosario

    @staticmethod
    def formatear(glosario: dict) -> str:
        """Convierte el diccionario del glosario en un texto legible para mostrar en pantalla."""
        glosario_filtrado = {
            p: d for p, d in glosario.items()
            if d != "(Simple explanation not available for this word)"
        }

        if not glosario_filtrado:
            return "No difficult words found."

        lineas = ["Glossary\n"]
        for palabra, definicion in glosario_filtrado.items():
            lineas.append(f"• {palabra.capitalize()}: {definicion}")

        return "\n".join(lineas)
