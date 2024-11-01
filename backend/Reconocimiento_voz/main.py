from audio_capture import capture_audio
from emotion_analysis import analyze_emotion
from results_visualization import plot_emotions, plot_pause_durations, plot_pitch_over_time
from audio_features import extract_pitch, calculate_pause_durations

def guardar_audio(audio, file_path="audio_capturado.wav"):
    import wave
    with wave.open(file_path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(audio.get_wav_data())

def procesar_audio():
    print("Iniciando captura de audio...")
    texto_transcrito, audio = capture_audio()
    
    if texto_transcrito:
        print("Texto capturado:", texto_transcrito)
        
        # Análisis emocional en el texto
        resultado_emocional = analyze_emotion(texto_transcrito)
        
        # Guardar el archivo de audio para análisis posterior
        guardar_audio(audio, "audio_capturado.wav")
        
        # Análisis de características vocales en el archivo guardado
        avg_pitch, pitch_category = extract_pitch("audio_capturado.wav")
        pause_durations, pause_interpretations = calculate_pause_durations("audio_capturado.wav")
        
        # Generar visualizaciones y preparar resultados
        emociones_plot = plot_emotions(resultado_emocional['emoción_específica'])
        pausa_duraciones_plot = plot_pause_durations(pause_durations, pause_interpretations)
        tono_plot = plot_pitch_over_time(pause_durations)
        
        # Resultado estructurado
        return {
            "texto": texto_transcrito,
            "emociones": resultado_emocional,
            "tono_promedio": {"valor": avg_pitch, "categoria": pitch_category},
            "pausas": {"duraciones": pause_durations, "interpretaciones": pause_interpretations},
            "graficos": {
                "emociones": emociones_plot,
                "pausas": pausa_duraciones_plot,
                "tono": tono_plot
            }
        }
    else:
        return {"error": "No se pudo capturar texto"}
