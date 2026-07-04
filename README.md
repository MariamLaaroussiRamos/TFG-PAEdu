![Python](https://img.shields.io/badge/Python-3.11-blue)
![Gradio](https://img.shields.io/badge/Gradio-5.x-orange)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

# PAEdu - Plataforma de Accesibilidad Educativa

PAEdu es una plataforma web desarrollada como Trabajo de Fin de Grado para transformar materiales educativos en recursos más accesibles y fáciles de entender para el alumnado con Necesidades Específicas de Apoyo Educativo (NEAE) y Trastorno del Espectro Autista (TEA).

La aplicación utiliza modelos de lenguaje y herramientas de procesamiento de texto para ofrecer una experiencia completa de adaptación de contenidos, que incluye:

- Extracción de texto desde archivos PDF.
- Simplificación automática de textos.
- Adaptación de preguntas de examen.
- Generación de versiones en lectura fácil.
- Creación automática de glosarios de términos complejos.
- Generación de audio a partir del texto adaptado.
- Exportación del resultado en formato PDF.

## Tabla de contenidos

- [Captura de la interfaz](#captura-de-la-interfaz)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Dependencias](#dependencias)
- [Notas importantes](#notas-importantes)
- [Autor](#autor)

## Captura de la interfaz

<p align="center">
  <img src="imagenes/interfaz_PAEdu.png" alt="Interfaz de PAEdu" width="900"/>
</p>

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/MariamLaaroussiRamos/TFG-PAEdu.git
cd TFG-PAEdu
```

2. Crea y activa un entorno virtual de Python 3.11:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Descarga el modelo de spaCy necesario:

```bash
python -m spacy download en_core_web_sm
```

## Uso

Con el entorno activado y las dependencias instaladas, ejecuta la aplicación desde el directorio raíz:

```bash
python src/app.py
```

Luego, abre la URL local que proporciona Gradio en el navegador.

### Flujo de trabajo

1. Sube un archivo PDF o pega texto en el panel de entrada.
2. Selecciona el modo de adaptación:
   - `Simplificar`
   - `Adaptar pregunta`
   - `Lectura fácil`
   - `Glosario`
3. Haz clic en `Transformar`.
4. Revisa el resultado en el panel de salida.
5. Descarga el PDF generado desde la pestaña `Documento Generado`.
6. Reproduce el audio en la pestaña `Audio` si se ha generado correctamente.

## Arquitectura

El proyecto está organizado en el directorio `src/` con los siguientes componentes principales:

- `src/app.py` - Clase principal `PAEduApp` que crea la interfaz Gradio y coordina los demás módulos.
- `src/pdf_reader.py` - Lee texto desde archivos PDF usando PyMuPDF.
- `src/text_simplifier.py` - Carga el modelo `google/flan-t5-base` y ofrece tres modos de adaptación de texto.
- `src/glossary.py` - Detecta palabras difíciles y genera un glosario con explicaciones simples.
- `src/tts.py` - Genera audio a partir del texto adaptado con `kokoro` y `soundfile`.
- `src/pdf_exporter.py` - Exporta un PDF con el texto original y el texto adaptado, usando ReportLab.

## Dependencias

Las dependencias principales se encuentran en `requirements.txt` e incluyen:

- `transformers`
- `torch`
- `accelerate`
- `gradio`
- `sentencepiece`
- `pymupdf`
- `reportlab`
- `kokoro`
- `soundfile`
- `misaki[en]`
- `wordfreq`
- `spacy`

## Notas importantes

- El modelo de generación de texto se carga en `src/text_simplifier.py` y puede usar GPU si está disponible.
- El glosario se construye detectando sustantivos poco frecuentes y solicitando explicaciones simples al modelo.
- Si el logo no está disponible, el PDF sigue generándose sin error.
- El audio se guarda localmente en un archivo MP3 y se muestra en la interfaz para descarga.

## Autor

**Mariam Laaroussi Ramos**

Trabajo de Fin de Grado - Ingeniería Informática


