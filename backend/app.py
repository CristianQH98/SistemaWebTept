import os
import sys
import cv2
import base64
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

# Añadir el path del módulo de procesamiento de emociones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'face_emotion_recognition')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'face_emotion_recognition', 'examples')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Reconocimiento_voz')))

from face_emotion_recognition.emotion_processor.main import EmotionRecognitionSystem
from face_emotion_recognition.examples.video_stream import VideoStream
from face_emotion_recognition.examples.camera import Camera
from Reconocimiento_voz.main import procesar_audio
from Reconocimiento_voz.main import capture_audio
from Reconocimiento_voz.main import analyze_emotion


# Crear la aplicación de Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS en toda la aplicación

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb+srv://crishqqh9811:cristianqh9811@sistematept.yiton.mongodb.net/"
client = MongoClient(mongo_uri)  # Conectar a la base de datos
db = client['SistemaTEPT']  # Seleccionar la base de datos
collection_usuarios = db['Usuario']  # Seleccionar la colección de usuarios 
pacientes_collection = db['pacientes']

# Ruta principal de prueba
@app.route('/')
def index():
    return "API de Reconocimiento de Emociones Activa"

# Ruta de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")
    user_data = collection_usuarios.find_one({"usuario": usuario})

    if user_data and user_data["contraseña"] == contraseña:
        # Asegúrate de incluir el nombre y apellido en la respuesta JSON
        return jsonify({
            "success": True,
            "rol": user_data["rol"],
            "nombre": user_data["nombre"],
            "apellido": user_data["apellido"]
        }), 200
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401


# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json  # Obtener datos JSON
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    rol = data.get('rol')
    
    # Validar datos
    if not nombre or not apellido or not usuario or not contraseña or not rol:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400  # Error si falta algún campo
    
    # Crear usuario en MongoDB
    nuevo_usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "usuario": usuario,
        "contraseña": contraseña,
        "rol": rol
    }
    collection_usuarios.insert_one(nuevo_usuario)  # Insertar nuevo usuario en la colección
    
    return jsonify({"message": "Usuario creado exitosamente", "usuario": nuevo_usuario}), 201  # Confirmación de creación

# Ruta para listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = list(collection_usuarios.find({}, {"_id": 0}))  # Obtener todos los usuarios, excluyendo _id
    return jsonify(usuarios), 200  # Devolver lista de usuarios

# Ruta para obtener un usuario específico por su nombre de usuario
@app.route('/usuarios/<usuario>', methods=['GET'])
def obtener_usuario(usuario):
    usuario_data = collection_usuarios.find_one({"usuario": usuario}, {"_id": 0})  # Buscar usuario específico
    if usuario_data:
        return jsonify(usuario_data), 200  # Devolver datos del usuario
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404  # Error si no se encuentra el usuario
    
#Crea un nuevo paciente
@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    data = request.json
    nuevo_paciente = {
        "id_paciente": data.get("id_paciente"),
        "Nombre": data.get("Nombre"),
        "Apellidos": data.get("Apellidos"),
        "Edad": data.get("Edad"),
        "Genero": data.get("Genero"),
        "Telefono": data.get("Telefono")
    }
    pacientes_collection.insert_one(nuevo_paciente)
    return jsonify({"message": "Paciente creado exitosamente"}), 201

# Ruta para obtener todos los pacientes
@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    pacientes = list(pacientes_collection.find({}, {"_id": 0}))
    return jsonify(pacientes), 200

# Ruta para obtener un paciente por ID
@app.route('/pacientes/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):
    paciente = pacientes_collection.find_one({"id_paciente": id_paciente}, {"_id": 0})
    if paciente:
        return jsonify(paciente), 200
    else:
        return jsonify({"error": "Paciente no encontrado"}), 404

# Ruta para actualizar un paciente
@app.route('/pacientes/<id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    data = request.json
    pacientes_collection.update_one({"id_paciente": id_paciente}, {"$set": data})
    return jsonify({"message": "Paciente actualizado exitosamente"}), 200

# Ruta para eliminar un paciente
@app.route('/pacientes/<id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):
    pacientes_collection.delete_one({"id_paciente": id_paciente})
    return jsonify({"message": "Paciente eliminado exitosamente"}), 200

# Ruta para obtener todas las preguntas
@app.route('/obtener_preguntas', methods=['GET'])
def obtener_preguntas():
    preguntas = list(db['PreguntasPsicologo'].find({}, {"_id": 0, "pregunta": 1}))
    return jsonify({"preguntas": preguntas}), 200 

# Ruta para agregar una nueva pregunta
@app.route('/agregar_pregunta', methods=['POST'])
def agregar_pregunta():
    data = request.json
    nueva_pregunta = {
        "pregunta": data.get("pregunta")
    }
    # Insertar la nueva pregunta en la colección
    db['PreguntasPsicologo'].insert_one(nueva_pregunta)
    return jsonify({"message": "Pregunta agregada exitosamente"}), 201

# Ruta para eliminar una pregunta específica
@app.route('/eliminar_pregunta', methods=['DELETE'])
def eliminar_pregunta():
    data = request.json
    pregunta_id = data.get("id")
    if pregunta_id:
        result = db['PreguntasPsicologo'].delete_one({"_id": ObjectId(pregunta_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Pregunta eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Pregunta no encontrada"}), 404
    else:
        return jsonify({"error": "ID de pregunta no proporcionado"}), 400

#grabar respuesta

@app.route('/grabar_respuesta', methods=['GET'])
def grabar_respuesta():
    texto_transcrito, audio = capture_audio()  # Captura y transcribe audio
    emocion = analyze_emotion(texto_transcrito)  # Analiza emoción en el texto
    
    # Imprimir el contenido de emocion para verificar su estructura
    print("Emoción detectada:", emocion)
    
    # Asegúrate de que "sentimiento_general" y "emoción_específica" sean las claves correctas
    sentimiento_general = emocion.get("sentimiento_general", "Desconocido")
    emociones_especificas = emocion.get("emoción_específica", [])
    
    return jsonify({
        "texto": texto_transcrito,
        "sentimiento_general": sentimiento_general,
        "emociones_especificas": emociones_especificas
    })


# Ruta para transmitir los frames de video
@app.route('/video_feed')
def video_feed():
    # Inicializar la cámara y el sistema de reconocimiento de emociones
    cam = Camera(0, 1280, 720)
    emotion_recognition_system = EmotionRecognitionSystem()
    video_stream = VideoStream(cam, emotion_recognition_system)

    def generate():
        for frame_encoded in video_stream.generate_frames():
            # Envía cada frame en formato multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + base64.b64decode(frame_encoded) + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

#ruta para procesar el audio 

@app.route('/procesar_audio', methods=['POST'])
def procesar_audio_endpoint():
    resultado = procesar_audio()
    
    if "error" in resultado:
        return jsonify({"success": False, "message": resultado["error"]}), 500
    
    # Convertir gráficos en base64 si quieres enviarlos
    emociones_grafico = base64.b64encode(resultado["graficos"]["emociones"]).decode('utf-8')
    pausa_duraciones_grafico = base64.b64encode(resultado["graficos"]["pausas"]).decode('utf-8')
    tono_grafico = base64.b64encode(resultado["graficos"]["tono"]).decode('utf-8')
    
    return jsonify({
        "success": True,
        "texto": resultado["texto"],
        "emociones": resultado["emociones"],
        "tono_promedio": resultado["tono_promedio"],
        "pausas": resultado["pausas"],
        "graficos": {
            "emociones": emociones_grafico,
            "pausas": pausa_duraciones_grafico,
            "tono": tono_grafico
        }
    }), 200

@app.route('/capturar_audio', methods=['GET'])
def capturar_audio():
    texto_transcrito, emocion = capture_audio()  # Ajusta según la función en `main.py`
    return jsonify({"texto_transcrito": texto_transcrito, "emocion": emocion})

# Iniciar la aplicación
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
  # Ejecutar la aplicación en modo de depuración