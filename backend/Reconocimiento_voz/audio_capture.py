import speech_recognition as sr

def capture_audio():
    # Inicializar el reconocedor de voz
    recognizer = sr.Recognizer()
    
    # Ajustar los parámetros para capturar mejor el audio
    recognizer.energy_threshold = 300  # Ajusta el umbral para captar mejor el audio
    recognizer.pause_threshold = 5   # Ajusta la pausa antes de que deje de escuchar (en segundos)
    
    # Usar el micrófono como fuente de audio
    with sr.Microphone() as source:
        print("Ajustando al ruido ambiente... por favor espera")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajustar al ruido de fondo
        
        print("Comienza a hablar...")
        
        # Capturar el audio
        audio = recognizer.listen(source, timeout=30, phrase_time_limit=30)  # Ajusta la duración máxima
        
        try:
            # Transcribir el audio a texto
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Texto reconocido:", text)
            return text, audio  # Devolvemos el texto y el objeto de audio
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None, None
        except sr.RequestError as e:
            print(f"Error en el servicio de reconocimiento de voz: {e}")
            return None, None
