from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore

class TensionScore(WeightedEmotionScore):
    def __init__(self):
        super().__init__(eyebrows_weight=0.40, eyes_weight=0.30, nose_weight=0.0, mouth_weight=0.30, posture_weight=0.0)

    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        score = 0.0
        if 'eyebrows together' in eyebrows_result:  # cejas muy juntas
            score += 40.0
        if 'right eyebrow: lowered' in eyebrows_result:  # ceja baja
            score += 25.0
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 25.0
        if 'left arch: negative' in eyebrows_result or 'right arch: negative' in eyebrows_result:  # curvatura negativa
            score += 10.0
        return min(score, 100.0)

    def calculate_mouth_score(self, mouth_result: str) -> float:
        score = 0.0
        if 'closed mouth' in mouth_result:  # labios cerrados o apretados
            score += 40.0
        if 'tight lips' in mouth_result or 'pressed lips' in mouth_result:
            score += 40.0
        if 'downward curvature' in mouth_result:  # labios hacia abajo
            score += 20.0
        return score

    def calculate_eyes_score(self, eyes_result: str) -> float:
        score = 0.0
        if 'opened eyes' in eyes_result:  # ojos bien abiertos (hipervigilancia)
            score += 40.0
        if 'upper eyelid raised' in eyes_result or 'lower eyelid tightened' in eyes_result:
            score += 40.0
        if 'staring' in eyes_result:  # mirada fija
            score += 20.0
        return min(score, 100.0)

    def calculate_nose_score(self, nose_result: str) -> float:
        return 0.0
    
    def calculate_posture_score(self, posture_result: str) -> float:
        return 0.0
