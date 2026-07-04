import os
from datetime import datetime
from kokoro import KPipeline
import soundfile as sf

class TextToSpeech:
    """Genera archivos de audio a partir de texto usando kokoro de forma local."""

    def __init__(self, lang_code: str = "b", voice: str = "af_heart", speed: float = 0.9):
        # lang_code='b' -> inglés británico
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice = voice
        self.speed = speed

    def generar_audio(self, texto: str) -> str:
        nombre_archivo = f"audioPAEdu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        # Ruta en el directorio local actual
        ruta = os.path.abspath(nombre_archivo)

        generator = self.pipeline(
            texto,
            voice=self.voice,
            speed=self.speed
        )

        for _, _, audio in generator:
            sf.write(ruta, audio, 24000)
            break

        return ruta
