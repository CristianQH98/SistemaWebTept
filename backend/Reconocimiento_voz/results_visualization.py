import matplotlib.pyplot as plt

def plot_emotions(emotion_data):
    """
    Genera un gráfico de barras para mostrar el análisis emocional.
    """
    if isinstance(emotion_data, list):
        emociones = emotion_data
        valores = [1] * len(emociones)
    else:
        emociones = list(emotion_data.keys())
        valores = list(emotion_data.values())

    plt.figure(figsize=(8, 6))
    plt.bar(emociones, valores, color='skyblue')
    plt.xlabel("Emociones")
    plt.ylabel("Puntuación")
    plt.title("Análisis Emocional del Texto")
    plt.show()

def plot_pause_durations(pause_durations, pause_interpretations):
    """
    Muestra un gráfico de barras de las duraciones de pausas y su interpretación.
    """
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(pause_durations)), pause_durations, color='skyblue', alpha=0.7)
    
    for bar, interpretation in zip(bars, pause_interpretations):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, interpretation, ha='center', va='bottom', fontsize=10)
    
    plt.xlabel("Pausas")
    plt.ylabel("Duración (segundos)")
    plt.title("Duración de Pausas con Interpretación")
    plt.show()

def plot_pitch_over_time(pitch_values):
    """
    Muestra un gráfico de línea para el tono a lo largo de la sesión.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(pitch_values, color='purple', marker='o', linestyle='-')
    plt.axhline(y=150, color='r', linestyle='--', label='Umbral Alto/Bajo')
    plt.xlabel("Tiempo (marcas)")
    plt.ylabel("Tono (Hz)")
    plt.title("Variación del Tono a lo Largo del Tiempo")
    plt.legend()
    plt.show()
