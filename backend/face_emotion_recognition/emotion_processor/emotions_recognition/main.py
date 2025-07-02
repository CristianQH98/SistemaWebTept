from typing import Dict
from emotion_processor.emotions_recognition.features.emotion_score import EmotionScore
from .emotions.angry_score import AngryScore
from .emotions.avoidance_score import AvoidanceScore
from .emotions.sad_score import SadScore
from .emotions.tension_score import TensionScore
from .emotions.fear_score import FearScore


class EmotionRecognition:
    def __init__(self):
        self.emotions: Dict[str, EmotionScore] = {
            'angry': AngryScore(),
            'avoidance': AvoidanceScore(),
            'sad': SadScore(),
            'tension': TensionScore(),
            'fear': FearScore(),
        }

    def recognize_emotion(self, processed_features: dict) -> dict:
        scores = {}
        for emotion_name, emotion_score_obj in self.emotions.items():
            scores.update(emotion_score_obj.calculate_score(processed_features))
        return scores
