import os
import sys
import cv2
import base64
import json
import traceback
import datetime
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#from reportes_controller import guardar_reporte
#from rutas.reportes import reportes_bp


# Añadir el path del módulo de procesamiento de emociones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'face_emotion_recognition')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'face_emotion_recognition', 'examples')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Reconocimiento_voz')))

from face_emotion_recognition.emotion_processor.main import EmotionRecognitionSystem
from face_emotion_recognition.examples.video_stream import VideoStream
from face_emotion_recognition.examples.camera import Camera
from Reconocimiento_voz.main import procesar_audio, capture_audio, analyze_emotion


# Crear la aplicación de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

# Conexión local a MongoDB
mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client['SistemaTEPT']
collection_usuarios = db['Usuario']
pacientes_collection = db['pacientes']
reportes_collection = db['reportes']
counters_collection = db['counters']
counters_collection = db['countersU']



@app.route('/')
def index():
    return "API de Reconocimiento de Emociones Activa"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get("usuario")
    contrasena = data.get("contraseña")

    # --- EXCEPCIÓN TEMPORAL PARA USUARIOS 'cris' Y 'gabi' ---
    if usuario == "cris" and contrasena == "cris123":
        return jsonify({
            "success": True,
            "rol": "psicologo",
            "nombre": "cristian",
            "apellido": "Quispe",
            "usuario": "cris"
        }), 200
    
    if usuario == "gabi" and contrasena == "gabi123":
        return jsonify({
            "success": True,
            "rol": "administrador",
            "nombre": "Gabriela",
            "apellido": "Quispe",
            "usuario": "gabi"
        }), 200

    print(f"Usuario recibido: {usuario}, Contraseña recibida: {contrasena}")

    # --------------------------------------------------------

    user_data = collection_usuarios.find_one({"usuario": usuario})

    if user_data and check_password_hash(user_data["contraseña"], contrasena):
        return jsonify({
            "success": True,
            "rol": user_data["rol"],
            "nombre": user_data["nombre"],
            "apellido": user_data["apellido"],
            "usuario": user_data["usuario"]
        }), 200
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401
    

def get_next_usuario_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "usuarios"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return f"u{counter['seq']}"
# --- USUARIOS ---
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    if not all([data.get(k) for k in ['nombre', 'apellido', 'usuario', 'contraseña', 'rol', 'estado']]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if collection_usuarios.find_one({"usuario": data['usuario']}):
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 409

    hashed_pass = generate_password_hash(data['contraseña'])

    nuevo_usuario = {
        "id": get_next_usuario_id(),  # ✅ Aquí se genera el ID incremental
        "nombre": data['nombre'],
        "apellido": data['apellido'],
        "usuario": data['usuario'],
        "contraseña": hashed_pass,
        "rol": data['rol'],
        "estado": data['estado'],
        "fecha_creacion": data.get("fecha_creacion") or datetime.date.today().isoformat()
    }
    collection_usuarios.insert_one(nuevo_usuario)
    nuevo_usuario.pop("_id", None)  # Eliminar el campo _id de la respuesta
    return jsonify({"message": "Usuario creado exitosamente", "usuario": nuevo_usuario}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = list(collection_usuarios.find({}, {"_id": 0, "contraseña": 0}))
    return jsonify(usuarios), 200

@app.route('/usuarios/<usuario>', methods=['GET'])
def obtener_usuario(usuario):
    usuario_data = collection_usuarios.find_one(
        {"usuario": usuario},
        {"_id": 0, "nombre": 1, "apellido": 1, "usuario": 1, "rol": 1})
    if usuario_data:
        return jsonify(usuario_data), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/usuarios/<usuario>', methods=['PUT'])
def actualizar_usuario(usuario):
    data = request.json
    update_fields = {
        "nombre": data.get("nombre"),
        "apellido": data.get("apellido"),
        "rol": data.get("rol"),
        "estado": data.get("estado")
    }
    result = collection_usuarios.update_one({"usuario": usuario}, {"$set": update_fields})
    if result.modified_count == 1:
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    return jsonify({"error": "Usuario no encontrado o sin cambios"}), 404

@app.route('/usuarios/<usuario>', methods=['DELETE'])
def eliminar_usuario(usuario):
    resultado = collection_usuarios.delete_one({"usuario": usuario})
    if resultado.deleted_count == 1:
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404


@app.route('/usuarios/<usuario>/contrasena', methods=['PUT'])
def actualizar_contrasena(usuario):
    data = request.json
    nueva = data.get("nueva_contrasena")
    if not nueva or len(nueva) < 4:
        return jsonify({"error": "Contraseña inválida"}), 400

    resultado = collection_usuarios.update_one(
        {"usuario": usuario},
        {"$set": {"contraseña": generate_password_hash(nueva)}}
    )
    if resultado.modified_count == 1:
        return jsonify({"message": "Contraseña actualizada correctamente"}), 200
    return jsonify({"message": "No se encontró el usuario o la contraseña no cambió"}), 404

# --- PACIENTES ---
def get_next_paciente_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "pacientes"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return f"p{counter['seq']}"

@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    data = request.json
    nuevo_paciente = {
        "id_paciente": get_next_paciente_id(),
        "Nombre": data.get("Nombre"),
        "Apellidos": data.get("Apellidos"),
        "Edad": data.get("Edad"),
        "Genero": data.get("Genero"),
        "Telefono": data.get("Telefono")
    }
    pacientes_collection.insert_one(nuevo_paciente)
    return jsonify({"message": "Paciente creado exitosamente"}), 201

@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    pacientes = list(pacientes_collection.find({}, {"_id": 0}))
    return jsonify(pacientes), 200

@app.route('/pacientes/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):
    paciente = pacientes_collection.find_one({"id_paciente": id_paciente}, {"_id": 0})
    if paciente:
        return jsonify(paciente), 200
    return jsonify({"error": "Paciente no encontrado"}), 404

@app.route('/pacientes/<id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    data = request.json
    pacientes_collection.update_one({"id_paciente": id_paciente}, {"$set": data})
    return jsonify({"message": "Paciente actualizado exitosamente"}), 200

@app.route('/pacientes/<id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):
    pacientes_collection.delete_one({"id_paciente": id_paciente})
    return jsonify({"message": "Paciente eliminado exitosamente"}), 200

# --- PREGUNTAS ---
@app.route('/obtener_preguntas', methods=['GET'])
def obtener_preguntas():
    preguntas = list(db['PreguntasPsicologo'].find({}, {"_id": 0, "pregunta": 1}))
    return jsonify({"preguntas": preguntas}), 200

@app.route('/agregar_pregunta', methods=['POST'])
def agregar_pregunta():
    data = request.json
    db['PreguntasPsicologo'].insert_one({"pregunta": data.get("pregunta")})
    return jsonify({"message": "Pregunta agregada exitosamente"}), 201

@app.route('/eliminar_pregunta', methods=['DELETE'])
def eliminar_pregunta():
    data = request.json
    pregunta_id = data.get("id")
    if not pregunta_id:
        return jsonify({"error": "ID no proporcionado"}), 400
    result = db['PreguntasPsicologo'].delete_one({"_id": ObjectId(pregunta_id)})
    if result.deleted_count:
        return jsonify({"message": "Pregunta eliminada exitosamente"}), 200
    return jsonify({"error": "Pregunta no encontrada"}), 404

@app.route('/grabar_respuesta', methods=['GET'])
def grabar_respuesta():
    texto_transcrito, audio = capture_audio()
    emocion = analyze_emotion(texto_transcrito)
    return jsonify({
        "texto": texto_transcrito,
        "sentimiento_general": emocion.get("sentimiento_general", "Desconocido"),
        "emociones_especificas": emocion.get("emoción_específica", [])
    })

@app.route('/video_feed')
def video_feed():
    cam = Camera(0, 1280, 720)
    ers = EmotionRecognitionSystem()
    video_stream = VideoStream(cam, ers)

    def generate():
        for frame_encoded in video_stream.generate_frames():
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + base64.b64decode(frame_encoded) + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/procesar_audio', methods=['POST'])
def procesar_audio_endpoint():
    resultado = procesar_audio()
    if "error" in resultado:
        return jsonify({"success": False, "message": resultado["error"]}), 500

    return jsonify({
        "success": True,
        "texto": resultado["texto"],
        "emociones": resultado["emociones"],
        "tono_promedio": resultado["tono_promedio"],
        "pausas": resultado["pausas"],
        "graficos": {
            "emociones": base64.b64encode(resultado["graficos"]["emociones"]).decode('utf-8'),
            "pausas": base64.b64encode(resultado["graficos"]["pausas"]).decode('utf-8'),
            "tono": base64.b64encode(resultado["graficos"]["tono"]).decode('utf-8')
        }
    }), 200

@app.route('/capturar_audio', methods=['GET'])
def capturar_audio():
    texto_transcrito, emocion = capture_audio()
    return jsonify({"texto_transcrito": texto_transcrito, "emocion": emocion})

@app.route('/probar_diagnostico', methods=['GET'])
def prueba_diagnostico():
    from face_emotion_recognition.emotion_processor.main import EmotionRecognitionSystem
    import cv2

    sistema = EmotionRecognitionSystem(guardar_en_bd=False)
    cap = cv2.VideoCapture(0)

    for _ in range(30):
        ret, frame = cap.read()
        if not ret:
            break
        sistema.frame_processing(frame)

    cap.release()
    ruta = sistema.finalizar_diagnostico()  # Que retorne la ruta o nombre del JSON
    nombre_archivo = os.path.basename(ruta)
    return jsonify({
        "mensaje": "ok Diagnóstico finalizado", 
        "archivo": nombre_archivo
        }), 200

@app.route('/guardar_reporte_bd', methods=['POST'])
def guardar_reporte_bd():
    data = request.get_json()
    nombre_archivo = data.get("archivo")  # ejemplo: "reporte_PacienteX_2025-06-30T15-00-00.json"

    try:
        # Ruta base relativa a este archivo (app.py)
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_reportes = os.path.join(ruta_base, "reportes_generados")
        ruta_completa = os.path.join(ruta_reportes, nombre_archivo)

        print(f"[INFO] Guardando reporte desde: {ruta_completa}")
        # Leer el contenido del archivo JSON
        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido_reporte = json.load(f)
        contenido_reporte["nombre_archivo"] = nombre_archivo 
        # Insertar el contenido en la base de datos
        reportes_collection.insert_one(contenido_reporte)

        return jsonify({"mensaje": "Reporte guardado exitosamente en MongoDB"}), 200
    except Exception as e:
        print(f"[ERROR] Al guardar el reporte: {e}")
        traceback.print_exc()
        return jsonify({"error": "No se pudo guardar el reporte"}), 500



@app.route('/leer_reporte')
def leer_reporte():
    archivo = request.args.get("archivo")
    try:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_reportes = os.path.join(ruta_base, "reportes_generados")
        ruta_completa = os.path.join(ruta_reportes, archivo)

        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido = json.load(f)
        return jsonify(contenido)
    except Exception as e:
        print(f"[ERROR] Al leer reporte: {e}")
        return jsonify({"error": "No se pudo leer el reporte"}), 500

@app.route('/reporte_por_archivo', methods=['GET'])
def reporte_por_archivo():
    nombre = request.args.get("archivo")  # ejemplo: reporte_Juan_2025-06-30T15-00-00.json
    if not nombre:
        return jsonify({"error": "Falta el nombre del archivo"}), 400

    try:
        # Buscar por coincidencia exacta en nombre del archivo (debe estar guardado en Mongo)
        reporte = reportes_collection.find_one({"nombre_archivo": nombre})

        if not reporte:
            return jsonify({"error": "Reporte no encontrado"}), 404

        reporte["_id"] = str(reporte["_id"])  # Para que no falle en JSON
        return jsonify(reporte)

    except Exception as e:
        print(f"[ERROR] al consultar MongoDB: {e}")
        return jsonify({"error": "Error interno al consultar el reporte"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
