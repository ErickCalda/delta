import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QThread, pyqtSignal, Qt

class RenderThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path

    def run(self):
        comando = f"manim -qm {self.script_path} DiferencialEsfera"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode != 0:
            print("Error de Manim:\n", resultado.stderr)
            
        video_output = os.path.join("media", "videos", "esfera", "720p30", "DiferencialEsfera.mp4")
        if os.path.exists(video_output):
            self.finished_signal.emit(os.path.abspath(video_output))
        else:
            self.finished_signal.emit("")

class ManimApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Margen de Error (Diferencial de Esfera)")
        self.setGeometry(100, 100, 950, 750)

        # Tema "Cyber Terminal"
        self.setStyleSheet("""
            QMainWindow { background-color: #0d1117; }
            QLabel { color: #00ff00; font-family: 'Consolas', 'Courier New', monospace; font-size: 15px; padding: 5px; }
            QPushButton { background-color: transparent; color: #38bdf8; font-size: 15px; font-weight: bold; font-family: 'Consolas', 'Courier New', monospace; padding: 12px; border-radius: 4px; border: 2px solid #38bdf8; }
            QPushButton:hover { background-color: #38bdf8; color: #0d1117; }
            QPushButton:disabled { border: 2px solid #475569; color: #475569; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        self.label_status = QLabel("Listo. Presiona 'Generar Animación' para compilar el modelo de tanque petroquímico.")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_status)

        # =========================================
        # BOTONES EN FILA (NUEVO)
        # =========================================
        self.botones_layout = QHBoxLayout() # Layout horizontal
        
        self.btn_render = QPushButton("Generar Animación")
        self.btn_render.clicked.connect(self.start_render)
        self.botones_layout.addWidget(self.btn_render)

        # Botón para abrir archivos en Fedora
        self.btn_abrir = QPushButton("Abrir Ubicación del Video")
        self.btn_abrir.clicked.connect(self.abrir_carpeta)
        self.btn_abrir.setEnabled(False) # Apagado hasta que haya video
        self.botones_layout.addWidget(self.btn_abrir)

        self.layout.addLayout(self.botones_layout)

        # Contenedor de Video
        self.video_container = QWidget()
        self.video_container.setStyleSheet("background-color: black; border-radius: 8px; border: 1px solid #1e3a8a;")
        self.container_layout = QVBoxLayout(self.video_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget()
        self.container_layout.addWidget(self.video_widget)
        
        self.layout.addWidget(self.video_container, stretch=1)
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

    def start_render(self):
        script_name = "esfera.py" 
        if not os.path.exists(script_name):
            self.label_status.setText(f"Error: No se encuentra el archivo '{script_name}'.")
            return

        self.label_status.setText("Compilando vectores matemáticos... Por favor espera.")
        self.btn_render.setEnabled(False)
        self.btn_abrir.setEnabled(False)

        self.thread = RenderThread(script_name)
        self.thread.finished_signal.connect(self.play_video)
        self.thread.start()

    def play_video(self, video_path):
        self.btn_render.setEnabled(True)
        if video_path:
            self.label_status.setText("¡Simulación completada! Reproduciendo...")
            self.btn_abrir.setEnabled(True) # Activamos el nuevo botón
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()
        else:
            self.label_status.setText("Error en el renderizado. Revisa la terminal.")

        # Función que llama al sistema operativo (Fedora/Linux)
    def abrir_carpeta(self):
            ruta = os.path.abspath(os.path.join("media", "videos", "esfera", "720p30"))
            if os.path.exists(ruta):
                # Detecta el sistema operativo
                if sys.platform == "win32":
                    os.startfile(ruta) # El comando nativo de Windows para abrir carpetas
                elif sys.platform == "linux":
                    subprocess.run(["xdg-open", ruta])
                elif sys.platform == "darwin": # Para macOS
                    subprocess.run(["open", ruta])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ManimApp()
    ventana.show()
    sys.exit(app.exec())