from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore

class AngryScore(WeightedEmotionScore):
    def __init__(self):
        # Pesos redistribuidos para reducir dominancia de boca y cejas
        super().__init__(eyebrows_weight=0.30, eyes_weight=0.25, nose_weight=0.15, mouth_weight=0.20, posture_weight=0.10)

    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        score = 0.0
        if 'eyebrows together' in eyebrows_result:            # cejas juntas
            score += 20.0
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 15.0
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 15.0
        if 'deep frown' in eyebrows_result:                   # nueva condición
            score += 25.0
        return min(score, 100.0)

    def calculate_eyes_score(self, eyes_result: str) -> float:
        score = 0.0
        if 'closed eyes' in eyes_result:
            score += 40.0
        if 'narrowed eyes' in eyes_result:
            score += 25.0
        if 'staring' in eyes_result:
            score += 25.0
        return min(score, 100.0)

    def calculate_nose_score(self, nose_result: str) -> float:
        score = 0.0
        if 'wrinkled nose' in nose_result:
            score += 40.0
        if 'flared nostrils' in nose_result:
            score += 30.0
        return min(score, 100.0)

    def calculate_mouth_score(self, mouth_result: str) -> float:
        score = 0.0
        mouth_result = [m.strip() for m in mouth_result.split(',')]
        if 'closed mouth' in mouth_result:
            score += 10.0
        if 'tight lips' in mouth_result:
            score += 30.0
        if 'tight lips hard' in mouth_result:
            score += 40.0
        if 'tight jaw' in mouth_result:
            score += 20.0
        if 'no right smile' in mouth_result:
            score += 10.0
        if 'no left smile' in mouth_result:
            score += 10.0
        return min(score, 100.0)

    def calculate_posture_score(self, posture_result: str) -> float:
        score = 0.0
        if 'shoulders raised' in posture_result:
            score += 25.0
        if 'leaning forward' in posture_result:
            score += 25.0
        if 'jaw clenched' in posture_result:
            score += 20.0
        return min(score, 100.0)
