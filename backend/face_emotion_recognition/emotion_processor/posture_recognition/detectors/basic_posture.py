import math
import mediapipe as mp

class BasicPostureDetector:
    def __init__(self):
        pass

    def get_angle(self, point1, point2, point3):
        a = [point1.x - point2.x, point1.y - point2.y]
        b = [point3.x - point2.x, point3.y - point2.y]
        dot_product = a[0]*b[0] + a[1]*b[1]
        mag_a = math.sqrt(a[0]**2 + a[1]**2)
        mag_b = math.sqrt(b[0]**2 + b[1]**2)
        if mag_a * mag_b == 0:
            return 0
        angle = math.acos(dot_product / (mag_a * mag_b))
        return math.degrees(angle)

    def detect_posture(self, landmarks):
        if not landmarks or len(landmarks) < 33:
            return "Vista parcial del cuerpo"

        try:
            from math import dist
            mp_pose = mp.solutions.pose
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

            visibilidad_torso = 0.5
            visibilidad_manos = 0.3

            torso = [left_shoulder, right_shoulder, left_hip, right_hip]
            if any(p.visibility < visibilidad_torso for p in torso):
                return "Vista parcial del cuerpo"

            if left_wrist.visibility < visibilidad_manos or right_wrist.visibility < visibilidad_manos:
                return "Vista parcial del cuerpo"

            # --- Detectar brazos cruzados (nuevas condiciones más robustas) ---
            wrist_L_to_elbow_R = dist([left_wrist.x, left_wrist.y], [right_elbow.x, right_elbow.y])
            wrist_R_to_elbow_L = dist([right_wrist.x, right_wrist.y], [left_elbow.x, left_elbow.y])
            wrist_to_wrist = dist([left_wrist.x, left_wrist.y], [right_wrist.x, right_wrist.y])
            y_alignment = abs(left_wrist.y - right_wrist.y)

            if (
                (wrist_L_to_elbow_R < 0.25 and wrist_R_to_elbow_L < 0.25 and y_alignment < 0.2)
                or (wrist_to_wrist < 0.25)
            ):
                return "Brazos cruzados"

            # --- Detectar postura general ---
            ambos_lados_visibles = all(
                p.visibility >= visibilidad_torso for p in [left_shoulder, right_shoulder, left_hip, right_hip]
            )
            lado_izquierdo_visible = all(p.visibility >= visibilidad_torso for p in [left_shoulder, left_hip])
            lado_derecho_visible = all(p.visibility >= visibilidad_torso for p in [right_shoulder, right_hip])

            if ambos_lados_visibles:
                upper_center = self._get_center(left_shoulder, right_shoulder)
                lower_center = self._get_center(left_hip, right_hip)
                tipo = "precisa"
            elif lado_izquierdo_visible:
                upper_center = left_shoulder
                lower_center = left_hip
                tipo = "aproximada"
            elif lado_derecho_visible:
                upper_center = right_shoulder
                lower_center = right_hip
                tipo = "aproximada"
            else:
                return "Vista parcial del cuerpo"

            vertical_line = type('Point', (), {'x': upper_center.x, 'y': upper_center.y - 0.1})()
            angle = self.get_angle(lower_center, upper_center, vertical_line)

            if 75 <= angle <= 105:
                return "Postura erguida" if tipo == "precisa" else "Postura erguida (aprox.)"
            else:
                return "Postura inclinada" if tipo == "precisa" else "Postura inclinada (aprox.)"

        except Exception as e:
            return f"Error en detección de postura: {str(e)}"

    def _get_center(self, point1, point2):
        return type('Point', (), {
            'x': (point1.x + point2.x) / 2,
            'y': (point1.y + point2.y) / 2
        })()
def obtener_postura_textual(results):
        if not results.pose_landmarks:
            return "incompleta"

        detector = BasicPostureDetector()
        postura = detector.detect_posture(results.pose_landmarks.landmark)

        # Aquí traducimos lo que devuelva a etiquetas limpias para el reporte
        if "parcial" in postura.lower():
            return "incompleta"
        elif "erguida" in postura.lower() or "alineado" in postura.lower():
            return "erguida"
        else:
            return "inclinada"
 