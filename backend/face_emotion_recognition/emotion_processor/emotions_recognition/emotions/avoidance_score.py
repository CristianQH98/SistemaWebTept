from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore

class AvoidanceScore(WeightedEmotionScore):
    def __init__(self):
        super().__init__(
            eyebrows_weight=0.15,
            eyes_weight=0.30,
            nose_weight=0.30,
            mouth_weight=0.25,
            posture_weight=0.0
        )

    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        score = 0.0
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 50.0
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 50.0
        return score

    def calculate_eyes_score(self, eyes_result: str) -> float:
        score = 0.0
        if 'closed eyes' in eyes_result:
            score += 70.0
        if 'eyes downcast' in eyes_result or 'eyes looking away' in eyes_result:
            score += 30.0
        return score

    def calculate_nose_score(self, nose_result: str, landmarks=None, image_width=1) -> float:
        score = 0.0

        # 🔧 FORZAMOS el resultado como si la cabeza estuviera girada
        head_direction = "face turned right"

        # Clasificamos evasión según el giro de cabeza solamente
        if head_direction in ['face turned left', 'face turned right']:
            score += 100.0  # evasión clara: sin contacto visual
        elif head_direction == 'face center':
            score += 10.0  # neutral

        return score

    def calculate_mouth_score(self, mouth_result: str) -> float:
        score = 0.0
        mouth_result = mouth_result.split(', ')
        if 'open mouth' in mouth_result:
            score += 50.0
        if 'right smile' in mouth_result:
            score += 25.0
        if 'left smile' in mouth_result:
            score += 25.0
        return score

    def calculate_posture_score(self, posture_result: str) -> float:
        return 0.0  # aún no usamos postura
