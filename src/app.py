import os
import gradio as gr

# Importo mis clases locales
from pdf_reader import PDFReader
from text_simplifier import TextSimplifier
from glossary import GlosarioGenerator
from tts import TextToSpeech
from pdf_exporter import PDFExporter

class PAEduApp:
    """Clase principal que conecta el modelo, el glosario, el TTS, el exportador y la interfaz."""
    def __init__(self):
        logo = os.path.join("imagenes", "logo_app.png")
        print(f"¿Existe el logo local?: {os.path.exists(logo)}")

        # Instancio todos los componentes una sola vez (el modelo tarda en cargar)
        self.reader = PDFReader()
        self.simplifier = TextSimplifier()
        self.glosario_generator = GlosarioGenerator(self.simplifier)
        self.tts = TextToSpeech()
        self.exporter = PDFExporter(logo_path=logo)

        self.demo = self._construir_interfaz()

    def procesar(self, texto: str, modo: str):
        """Según el modo elegido en la interfaz, llama a un método u otro."""
        if not texto or texto.strip() == "":
            return "Introduce texto o sube un PDF."

        if modo == "Simplificar":
            return self.simplifier.simplificar(texto)
        elif modo == "Adaptar pregunta":
            return self.simplifier.adaptar_examen(texto)
        elif modo == "Lectura fácil":
            return self.simplifier.lectura_facil(texto)
        elif modo == "Glosario":
            glosario = self.glosario_generator.generar_glosario(texto)
            return self.glosario_generator.formatear(glosario)

        return "Modo no válido."

    def run_pipeline(self, texto: str, modo: str):
        """Pipeline completo: procesa el texto según el modo y genera también el audio."""
        if not texto:
            return "Por favor, introduce texto o sube un PDF.", None
        resultado = self.procesar(texto, modo)
        audio_path = self.tts.generar_audio(resultado)
        return resultado, audio_path

    def exportar(self, entrada_texto: str, salida_texto: str, modo: str):
        """Genera el PDF descargable cada vez que cambia el texto de salida."""
        if not salida_texto:
            return None
        return self.exporter.exportar_pdf(entrada_texto, salida_texto, modo)

    def _construir_interfaz(self) -> gr.Blocks:
        """Monta toda la interfaz de la aplicación con Gradio Blocks."""
        theme = gr.themes.Soft(
            primary_hue="pink", secondary_hue="rose", neutral_hue="slate", radius_size="md"
        ).set(
            body_background_fill="#faf7f8", block_background_fill="white",
            block_border_width="0.5px", block_border_color="#e9c9d1"
        )

        custom_css = """
        .header-container { text-align: center; padding: 25px 0 30px; margin-bottom: 15px; }
        .main-title { font-size: 25px; font-weight: 700; color: #ec4899; }
        .sub-title { margin-top: 8px; font-size: 15px; color: #6b7280; }
        .action-btn { font-weight: 600 !important; margin-top: 8px !important; }
        textarea { height: 420px !important; overflow-y: auto !important; }
        .gradio-container { overflow-x: hidden; }
        """

        with gr.Blocks(theme=theme, css=custom_css) as demo:

            # Header
            gr.Markdown("""
            <div class="header-container">
                <div class="main-title">Plataforma de Accesibilidad Educativa</div>
                <div class="sub-title">Asistente de IA para la transformación y adaptación de documentos</div>
            </div>
            """)

            with gr.Row():

                # panel de control/columna izq
                with gr.Column(scale=1, min_width=300):
                    # Sección 1: Carga de PDF
                    with gr.Group():
                        gr.Markdown("### Configuración")
                        pdf_input = gr.File(label="", file_types=[".pdf"], file_count="single", height=120)

                    # elección de modo y botón para enviar
                    modo = gr.Dropdown(
                        choices=["Simplificar", "Adaptar pregunta", "Lectura fácil", "Glosario"],
                        value="Simplificar", label="Modo de Adaptación", interactive=True
                    )

                    boton = gr.Button("Transformar", variant="primary", elem_classes="action-btn", size="lg")

                # columna dcha/visualizacion de contenido
                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📝 Textos"):
                            with gr.Row():
                              # Texto original
                                with gr.Column():
                                    gr.Markdown("#### Texto Original")
                                    entrada = gr.Textbox(placeholder="El texto extraído...", lines=1, max_lines=20, elem_classes="textarea", show_label=False)
                                # Texto adaptado
                                with gr.Column():
                                    gr.Markdown("#### Texto Adaptado")
                                    salida = gr.Textbox(placeholder="El resultado...", lines=1, max_lines=20, interactive=False, elem_classes="textarea", show_label=False)
                        # Pestaña 2: audio
                        with gr.TabItem("🎧 Audio"):
                            gr.Markdown("### 🔊 Reproductor de Voz")
                            audio = gr.Audio(label="Audio del Texto Adaptado", type="filepath")
                        # Pestaña 3: doc generado
                        with gr.TabItem("📥 Documento Generado"):
                            gr.Markdown("### 📄 Descargar PDF Adaptado")
                            descargar = gr.File(label="", interactive=False, height=80)
            # eventos y logica
            # cuando se sube un PDF, se extrae el texto automáticamente
            pdf_input.change(fn=self.reader.leer_pdf, inputs=pdf_input, outputs=entrada)
            # al pulsar el botón se ejecuta el pipeline completo (adaptar texto + generar audio)
            boton.click(fn=self.run_pipeline, inputs=[entrada, modo], outputs=[salida, audio])
            # cada vez que cambia el texto de salida, se genera automáticamente el PDF descargable
            salida.change(fn=self.exportar, inputs=[entrada, salida, modo], outputs=descargar)

        return demo

    def launch(self, **kwargs):
        """Lanza la interfaz de Gradio."""
        self.demo.launch(**kwargs)

if __name__ == "__main__":
    app = PAEduApp()
    app.launch(debug=True)
