import cv2
import mediapipe as mp
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_CONTOURS

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh

# Colores personalizados
COLOR_WHITE = (255, 255, 255)
COLOR_CELESTE = (255, 255, 0)

def draw_filtered_pose_landmarks(image, landmarks, connections):
    h, w, _ = image.shape

    # Dibujar solo conexiones (líneas blancas gruesas del cuerpo)
    for connection in connections:
        start_idx, end_idx = connection
        start = landmarks.landmark[start_idx]
        end = landmarks.landmark[end_idx]

        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)

        cv2.line(image, (x1, y1), (x2, y2), COLOR_WHITE, thickness=4)

    # Dibujar puntos clave en el cuerpo (hombros, codos, muñecas)
    keypoints = [11, 12, 13, 14, 15, 16]  # hombros y brazos
    for idx in keypoints:
        landmark = landmarks.landmark[idx]
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (cx, cy), 8, COLOR_WHITE, -1)  # contorno
        cv2.circle(image, (cx, cy), 5, COLOR_CELESTE, -1)  # relleno

def draw_hand_keypoints(image, hand_landmarks):
    h, w, _ = image.shape
    for landmark in hand_landmarks.landmark:
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (cx, cy), 5, COLOR_CELESTE, -1)

def draw_landmarks_all(image, results):
    # Pose: líneas blancas y puntos clave
    if results.pose_landmarks:
        draw_filtered_pose_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

    # Cara: solo contornos (labios, ojos, cejas, mandíbula, etc.)
    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            FACEMESH_CONTOURS,
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=1, circle_radius=0),
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=1)
        )

    # Mano izquierda
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=2, circle_radius=0),
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=2))
        draw_hand_keypoints(image, results.left_hand_landmarks)

    # Mano derecha
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=2, circle_radius=0),
            mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=2))
        draw_hand_keypoints(image, results.right_hand_landmarks)

    return image
