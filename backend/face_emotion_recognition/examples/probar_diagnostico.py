from emotion_processor.main import EmotionRecognitionSystem
import cv2

sistema = EmotionRecognitionSystem(guardar_en_bd=True)

# Simulación básica: procesar 30 frames de una cámara o video
cap = cv2.VideoCapture(0)
for _ in range(30):
    ret, frame = cap.read()
    if not ret:
        break
    sistema.frame_processing(frame)

cap.release()

# Al finalizar, guardamos el diagnóstico
sistema.finalizar_diagnostico()
