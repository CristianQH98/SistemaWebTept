import cv2
import numpy as np


class EmotionsVisualization:
    def __init__(self):
        self.emotion_colors = {
            'angry': (35, 50, 220),
            'avoidance': (186, 119, 4),
            'sad': (128, 37, 146),
            'tension': (100, 100, 255),
            'fear': (0, 255, 255)
        }
        self.emotion_labels = {
            'angry': 'Enojo',
            'avoidance': 'Evitación',
            'sad': 'Tristeza',
            'tension': 'Tensión',
            'fear': 'Miedo'
        }

    def main(self, emotions: dict, original_image: np.ndarray):
        for i, (emotion, score) in enumerate(emotions.items()):
            if emotion not in self.emotion_colors:
                continue  # Ignora emociones no reconocidas (por si acaso)
            cv2.putText(original_image, self.emotion_labels[emotion], (10, 30 + i * 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, self.emotion_colors[emotion], 1, cv2.LINE_AA)
            cv2.rectangle(original_image, (150, 15 + i * 40),
                          (150 + int(score * 2.5), 35 + i * 40), self.emotion_colors[emotion], -1)
            cv2.rectangle(original_image, (150, 15 + i * 40),
                          (400, 35 + i * 40), (255, 255, 255), 1)

        return original_image