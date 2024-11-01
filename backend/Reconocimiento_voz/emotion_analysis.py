from transformers import pipeline

# Cargar el modelo de análisis de sentimientos multilingüe
emotion_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Diccionario de léxico emocional en español
lexico_emocional = {
    "tristeza": ["triste", "deprimido", "desanimado", "melancólico", "solo", "desolado", "desesperado"],
    "enojo": ["enojado", "molesto", "irritado", "furioso", "frustrado", "indignado", "iracundo"],
    "miedo": ["asustado", "nervioso", "ansioso", "preocupado", "temeroso", "aterrorizado", "paranoico"],
    "ansiedad": ["ansioso", "inquieto", "tenso", "estresado", "angustiado", "nervioso"],
    "culpa": ["culpable", "arrepentido", "responsable", "remordimiento"],
    "vergüenza": ["avergonzado", "humillado", "deshonrado", "indigno"],
    "apatía": ["apático", "indiferente", "desinteresado", "sin motivación"],
    "desconfianza": ["desconfiado", "sospechoso", "receloso", "vigilante"],
    "entumecimiento": ["vacío", "sin emociones", "entumecido", "insensible"]
}

def analyze_emotion(text):
    """
    Realiza un análisis emocional combinado usando el modelo de sentimientos y el léxico emocional.
    """
    # Primero, usa el modelo de sentimientos para obtener el sentimiento general
    sentimiento = emotion_analyzer(text)[0]
    
    # Buscar emociones específicas en el texto usando el léxico emocional
    emociones_detectadas = {}
    for emocion, palabras in lexico_emocional.items():
        if any(palabra in text.lower() for palabra in palabras):
            emociones_detectadas[emocion] = True
    
    # Formatear el resultado final
    resultado = {
        "sentimiento_general": sentimiento["label"],
        "emoción_específica": list(emociones_detectadas.keys())  # Emociones detectadas por léxico
    }
    
    return resultado
