import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class TextSimplifier:
    """Carga el modelo de lenguaje y ofrece los distintos modos de adaptación de texto."""

    def __init__(self, model_name: str = "google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

        print(f"Modelo cargado en: {self.device}")

    def _generar_respuesta(self, prompt: str) -> str:
        """Método interno que manda un prompt al modelo y devuelve el texto generado."""
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.3
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def simplificar(self, texto: str) -> str:
        """Modo 1: simplifica el texto en bullets con frases cortas."""
        prompt = f"""Rewrite the text in simple words and short sentences.
Write each idea as a bullet point starting with "-".

Text: {texto}

Simple version:
-"""
        return self._generar_respuesta(prompt)

    def adaptar_examen(self, texto: str) -> list:
        """Modo 2: coge preguntas de examen y las reescribe más simples (pensado para alumnado con TEA)."""
        preguntas = [q.strip() for q in texto.split("\n") if q.strip()]
        resultados = []

        for q in preguntas:
            prompt = f"""
Rewrite this exam question in simple English for ASD students.

Rules:
- Keep the meaning
- Use very simple words
- Use ONE short sentence only

Output format:
Simplified question: ...

Question:
{q}

Simplified question:
"""
            out = self._generar_respuesta(prompt)
            resultados.append(out)

        return "\n".join(resultados)  # Convertido a string para la interfaz

    def lectura_facil(self, texto: str) -> str:
        """Modo 3: reescribe el texto siguiendo las pautas de "lectura fácil"."""
        prompt = f"""Rewrite the text in Easy-to-Read style.
Rules: short sentences, simple words, one idea per sentence, no metaphors, no abbreviations.

Text: {texto}

Easy-to-Read version:
-"""
        return self._generar_respuesta(prompt)
