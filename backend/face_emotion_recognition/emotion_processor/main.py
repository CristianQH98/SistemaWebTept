# Corrección para EmotionRecognitionSystem y su integración completa de emociones y posturas
import numpy as np
from emotion_processor.face_mesh.face_mesh_processor import FaceMeshProcessor
from emotion_processor.data_processing.main import PointsProcessing
from emotion_processor.emotions_recognition.main import EmotionRecognition
from emotion_processor.emotions_visualizations.main import EmotionsVisualization
from emotion_processor.posture_recognition.main import PostureRecognition
from emotion_processor.posture_visualization.main import PostureVisualization
from emotion_processor.diagnostico_session import DiagnosticoEnProceso
from emotion_processor.posture_recognition.detectors.basic_posture import obtener_postura_textual
from datetime import datetime
import json
import sys
import os



class EmotionRecognitionSystem:
    def __init__(self, guardar_en_bd=False):
        self.guardar_en_bd = guardar_en_bd
        self.face_mesh = FaceMeshProcessor()
        self.data_processing = PointsProcessing()
        self.emotions_recognition = EmotionRecognition()
        self.emotions_visualization = EmotionsVisualization()
        self.posture_recognition = PostureRecognition()
        self.posture_visualization = PostureVisualization()
        self.diagnostico = DiagnosticoEnProceso(
            psicologo_info={"nombre": "Cristian"}, 
            paciente_info={"nombre": "Paciente X"}) 
    
    def finalizar_diagnostico(self):
        self.diagnostico.finalizar_sesion()
        reporte = self.diagnostico.generar_reporte()

        # Ruta base relativa a este archivo (main.py)
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_reportes = os.path.join(ruta_base, "..", "reportes_generados")  # sube a backend y entra a reportes_generados

        # Asegurar que la carpeta exista
        os.makedirs(ruta_reportes, exist_ok=True)

        nombre_sanitizado = reporte['paciente']['nombre'].replace(' ', '_')
        timestamp_sanitizado = reporte['timestamp_inicio'].replace(':', '-')
        nombre_archivo = f"reporte_{nombre_sanitizado}_{timestamp_sanitizado}.json"
        reporte["nombre_archivo"] = nombre_archivo
        ruta_archivo = os.path.join(ruta_reportes, nombre_archivo)

        # Guardar el JSON
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(reporte, f, indent=4, ensure_ascii=False)

        print(f" Reporte guardado en: {ruta_archivo}")
        return ruta_archivo


    def frame_processing(self, face_image: np.ndarray):
        face_points, control_process, original_image = self.face_mesh.process(face_image, draw=False)
        if control_process:
            processed_features = self.data_processing.main(face_points)
            emotions = self.emotions_recognition.recognize_emotion(processed_features)
            timestamp = datetime.now().isoformat()

            # Obtener emoción dominante
            emocion_dominante = max(emotions, key=emotions.get)
            score_dominante = emotions[emocion_dominante]

            for emocion, score in emotions.items():
                self.diagnostico.agregar_emocion(emocion, score, timestamp)

                if score >= 100:
                    nombre_img = f"{emocion}_{timestamp.replace(':', '-')}.jpg"
                    ruta_img = f"capturas/{nombre_img}"
                    self.diagnostico.guardar_captura(ruta_img, f"{emocion.upper()} elevada", timestamp)
                    
            draw_emotions = self.emotions_visualization.main(emotions, original_image)
            holistic_results = self.posture_recognition.main(original_image)
            postura_textual = obtener_postura_textual(holistic_results)
            self.diagnostico.agregar_postura(postura_textual, timestamp)

            draw_posture = self.posture_visualization.main(draw_emotions, holistic_results)
   
            return draw_emotions, emocion_dominante, score_dominante, timestamp
        else:
            print("No face mesh detected")
            return face_image, "neutra", 0, datetime.now().isoformat()