from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore

class FearScore(WeightedEmotionScore):
    def __init__(self):
        super().__init__(eyebrows_weight=0.2, eyes_weight=0.3, nose_weight=0.0, mouth_weight=0.3, posture_weight=0.2)

    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        score = 0.0
        if 'eyebrows together' in eyebrows_result:
            score += 20.0
        if 'right eyebrow: raised' in eyebrows_result:
            score += 40.0
        if 'left eyebrow: raised' in eyebrows_result:
            score += 40.0
        return min(score, 100.0)

    def calculate_eyes_score(self, eyes_result: str) -> float:
        return 40.0 if 'open eyes' in eyes_result else 0.0

    def calculate_nose_score(self, nose_result: str) -> float:
        return 0.0  # Se ignora en esta emoción

    def calculate_mouth_score(self, mouth_result: str) -> float:
        score = 0.0
        if 'open mouth' in mouth_result:
            score += 30.0
        if 'no right smile' in mouth_result:
            score += 10.0
        if 'no left smile' in mouth_result:
            score += 10.0
        return min(score, 100.0)

    def calculate_posture_score(self, posture_result: str) -> float:
        score = 0.0
        if 'shoulders raised' in posture_result:
            score += 10.0
        if 'head pulled back' in posture_result:
            score += 10.0
        if 'torso rigid' in posture_result:
            score += 10.0
        return min(score, 100.0)