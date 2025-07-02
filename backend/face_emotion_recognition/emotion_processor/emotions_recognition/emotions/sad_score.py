from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


class SadScore(WeightedEmotionScore):
    def __init__(self):
        super().__init__(eyebrows_weight=0.35, eyes_weight=0.35, nose_weight=0.1, mouth_weight=0.25, posture_weight=0.5)

    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        """
        Las cejas caídas y juntas son signos típicos de tristeza.
        """
        score = 0.0
        if 'eyebrows together' in eyebrows_result:
            score += 60.0
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 20.0
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 20.0
        return score

    def calculate_eyes_score(self, eyes_result: str) -> float:
        """
        Los ojos cerrados o con mirada baja son comunes en tristeza.
        """
        if 'closed eyes' in eyes_result:
            return 100.0
        if 'eyes downcast' in eyes_result:
            return 60.0
        return 0.0

    def calculate_nose_score(self, nose_result: str) -> float:
        """
        La nariz se ignora en tristeza leve; si quisieras usarla, podrías incluir 'flaring nostrils'.
        """
        return 0.0

    def calculate_mouth_score(self, mouth_result: str) -> float:
        """
        Una boca cerrada, sin sonrisa o con comisuras hacia abajo refleja tristeza.
        """
        score = 0.0
        if 'closed mouth' in mouth_result:
            score += 20.0
        if 'no right smile' in mouth_result:
            score += 30.0
        if 'no left smile' in mouth_result:
            score += 30.0
        if 'mouth corners down' in mouth_result:
            score += 70.0  # muy representativo de tristeza
        return score

    def calculate_posture_score(self, posture_result: str) -> float:
        """
        Cabeza o torso caídos puede indicar desánimo emocional.
        """
        if 'head down' in posture_result or 'slouched shoulders' in posture_result:
            return 100.0
        return 0.0