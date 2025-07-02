from datetime import datetime
import cv2
import numpy as np
import os


class DiagnosticoEnProceso:
    def __init__(self, psicologo_info, paciente_info):
        self.psicologo = psicologo_info
        self.paciente = paciente_info
        self.emociones = []
        self.posturas = []
        self.voz = []
        self.capturas = []
        self.alertas = []
        self.inicio = datetime.now()
        self.fin = None
        self.emociones_recientes = []
        self.emociones_criticas = {}  
        
    def agregar_emocion(self, emocion, score, timestamp, frame=None):
        self.emociones.append({"emocion": emocion, "score": score, "timestamp": timestamp})
        self.evaluar_alerta_emocion(emocion, score, timestamp, frame)

    def agregar_postura(self, postura, timestamp):
        self.posturas.append({"postura": postura, "timestamp": timestamp})

    def agregar_transcripcion(self, texto, emocion_detectada, timestamp):
        self.voz.append({"texto": texto, "emocion": emocion_detectada, "timestamp": timestamp})

    def guardar_captura(self, ruta, descripcion, timestamp, frame=None):
        if frame is not None:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            frame = generar_imagen_con_barra(frame, descripcion.split("'")[1], 100)
            cv2.imwrite(ruta, frame)
        else:
            print("[Advertencia] No se recibió frame para la captura")
        self.capturas.append({"ruta": ruta, "descripcion": descripcion, "timestamp": timestamp})

    def evaluar_alerta_emocion(self, emocion, score, timestamp, frame=None):

        if score >= 100:
            self.alertas.append({
                "tipo": "Emoción intensa",
                "emocion": emocion,
                "score": score,
                "timestamp": timestamp
            })

        if score == 100:
            # Alerta directa por score máximo
            self.alertas.append({
                "tipo": "Score máximo",
                "emocion": emocion,
                "timestamp": timestamp,
                "detalle": f"Score de 100 detectado en emoción {emocion}"
            })

            # Iniciar o actualizar seguimiento de emoción crítica
            estado = self.emociones_criticas.get(emocion, {
                "conteo": 0,
                "capturas_realizadas": 0
            })
            estado["conteo"] += 1

            # Captura al tercer frame
            if estado["conteo"] == 3 and estado["capturas_realizadas"] == 0:
                self.guardar_captura(
                     ruta=f"capturas/{emocion}_critica_1.jpg",
                     descripcion=f"Primera captura de emoción intensa '{emocion}' (score=100)",
                     timestamp=timestamp,
                     frame=frame
                )
                estado["capturas_realizadas"] += 1

            # Captura al quinto frame
            elif estado["conteo"] == 5 and estado["capturas_realizadas"] == 1:
                self.guardar_captura(
                    ruta=f"capturas/{emocion}_critica_2.jpg",
                    descripcion=f"Segunda captura de emoción intensa '{emocion}' (score=100 sostenido)",
                    timestamp=timestamp,
                    frame=frame 
                )
                estado["capturas_realizadas"] += 1

            self.emociones_criticas[emocion] = estado
        else:
            # Si el score bajó, reseteamos el estado de esa emoción
            self.emociones_criticas[emocion] = {
                "conteo": 0,
                "capturas_realizadas": 0
            }

        # Evaluación de score sostenido (>90 durante 3 segundos)
        t_actual = datetime.fromisoformat(timestamp)
        self.emociones_recientes.append({"emocion": emocion, "score": score, "timestamp": timestamp})

        self.emociones_recientes = [
            e for e in self.emociones_recientes
            if (t_actual - datetime.fromisoformat(e["timestamp"])).total_seconds() <= 3
        ]

        conteo = sum(1 for e in self.emociones_recientes if e["emocion"] == emocion and e["score"] > 90)
        if conteo >= 3:
            self.alertas.append({
                "tipo": "Score mantenido",
                "emocion": emocion,
                "timestamp": timestamp,
                "detalle": f"Score >90 mantenido para emoción {emocion} durante al menos 3 segundos"
            })
            self.emociones_recientes = []

    def finalizar_sesion(self):
        self.fin = datetime.now()

    def generar_reporte(self):
        return {
            "psicologo": self.psicologo,
            "paciente": self.paciente,
            "emociones": self.emociones,
            "posturas": self.posturas,
            "voz": self.voz,
            "capturas": self.capturas,
            "alertas": self.alertas,
            "timestamp_inicio": self.inicio.isoformat(),
            "timestamp_fin": self.fin.isoformat() if self.fin else None
        }
    
def generar_imagen_con_barra(frame, emocion, score):
        """
        Dibuja una barra representando la emoción sobre el frame dado.

        - frame: imagen original (de tipo ndarray)
        - emocion: string ('tension', 'miedo', etc.)
        - score: entero entre 0 y 100

        Retorna: el frame con la barra dibujada
        """

        # Clonamos la imagen para no modificar el original
        output = frame.copy()

        # Dimensiones
        alto, ancho, _ = output.shape
        barra_alto = 50
        margen = 10

        # Área de barra
        inicio_barra_y = alto - barra_alto - margen
        fin_barra_y = alto - margen

        # Color de barra por emoción (puedes personalizar)
        colores = {
            'tension': (0, 140, 255),
            'miedo': (0, 0, 255),
            'tristeza': (255, 0, 0),
            'enojo': (0, 0, 128),
            'evasión': (160, 160, 160)
        }

        color = colores.get(emocion.lower(), (255, 255, 255))

        # Fondo de barra
        cv2.rectangle(output, (margen, inicio_barra_y), (ancho - margen, fin_barra_y), (50, 50, 50), -1)

        # Barra proporcional al score
        barra_ancho = int((ancho - 2 * margen) * (score / 100))
        cv2.rectangle(output, (margen, inicio_barra_y), (margen + barra_ancho, fin_barra_y), color, -1)

        # Texto
        texto = f"{emocion.upper()} ({score})"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(output, texto, (margen, inicio_barra_y - 10), font, 0.9, color, 2)

        return output