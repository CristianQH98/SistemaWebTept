import librosa
import numpy as np

def extract_pitch(audio_path):
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    pitch_values = []
    for t in range(pitches.shape[1]):
        pitch = pitches[:, t]
        pitch = pitch[pitch > 0]
        if len(pitch) > 0:
            pitch_values.append(np.mean(pitch))
    
    avg_pitch = np.mean(pitch_values) if pitch_values else None
    # Interpretación del tono
    pitch_category = "alto" if avg_pitch and avg_pitch >= 150 else "bajo"
    return avg_pitch, pitch_category

def calculate_pause_durations(audio_path, threshold=0.01):
    y, sr = librosa.load(audio_path)
    intervals = librosa.effects.split(y, top_db=20)
    
    pause_durations = []
    pause_interpretations = []
    for i in range(1, len(intervals)):
        pause_duration = (intervals[i][0] - intervals[i-1][1]) / sr
        pause_durations.append(pause_duration)
        # Interpretación de la duración de las pausas
        pause_interpretations.append("larga" if pause_duration >= 0.5 else "corta")
    
    return pause_durations, pause_interpretations
