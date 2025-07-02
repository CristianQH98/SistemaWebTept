import os
import sys
import cv2
import base64
from emotion_processor.main import EmotionRecognitionSystem
from camera import Camera

# Ajustar el path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class VideoStream:
    def __init__(self, cam: Camera, emotion_recognition_system: EmotionRecognitionSystem):
        self.camera = cam
        self.emotion_recognition_system = emotion_recognition_system

    def generate_frames(self):
        """Generador de frames en formato JPEG listos para ser enviados al frontend"""
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            # Ahora frame_processing devuelve también la emoción, el score y el timestamp
            frame, emocion, score, timestamp = self.emotion_recognition_system.frame_processing(frame)

            # Evaluar alerta y guardar captura con barra si corresponde
            self.emotion_recognition_system.diagnostico.evaluar_alerta_emocion(
                emocion=emocion,
                score=score,
                timestamp=timestamp,
                frame=frame  # pasamos el frame actual con rostro
            )

            # Codificar el frame para envío al frontend
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break

            frame_encoded = base64.b64encode(jpeg).decode('utf-8')
            yield frame_encoded
