import cv2
from emotion_processor.posture_visualization.utils.draw_skeleton import draw_landmarks_all
from emotion_processor.posture_recognition.detectors.basic_posture import BasicPostureDetector

class PostureVisualization:
    def __init__(self):
        self.basic_posture_detector = BasicPostureDetector()

    def main(self, image, holistic_results):
        # Verificamos si hay landmarks relevantes (pose o manos)
        if holistic_results.pose_landmarks or \
           holistic_results.left_hand_landmarks or \
           holistic_results.right_hand_landmarks:

            # Dibujamos los puntos del cuerpo
            image_with_landmarks = draw_landmarks_all(image, holistic_results)

            # Evaluamos postura si hay landmarks del cuerpo
            if holistic_results.pose_landmarks:
                posture_result = self.basic_posture_detector.detect_posture(
                    holistic_results.pose_landmarks.landmark
                )

                # Mostramos resultado de postura
                cv2.putText(
                    image_with_landmarks,
                    f"{posture_result}",
                    (20, 460),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),  # blanco
                    2,
                    cv2.LINE_AA
                )

                # (OPCIONAL) Ejemplo de alerta visual si detectás emoción intensa
                # if sad_score >= 100:
                #     cv2.putText(
                #         image_with_landmarks,
                #         "[ALERTA] Tristeza elevada detectada",
                #         (20, 420),
                #         cv2.FONT_HERSHEY_SIMPLEX,
                #         0.8,
                #         (0, 0, 255),  # rojo
                #         2,
                #         cv2.LINE_AA
                #     )

            return image_with_landmarks

        else:
            # Si no se detecta nada, mostramos mensaje de error
            cv2.putText(
                image,
                "Postura no detectada",
                (20, 460),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),  # rojo
                2,
                cv2.LINE_AA
            )
            return image
