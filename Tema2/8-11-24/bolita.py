
import cv2
import mediapipe as mp
import pygame
import sys

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Control de Bola con Gestos")

# Configuración de la bola
ball_color = (255, 0, 0)
ball_radius = 20
ball_x, ball_y = 320, 240  # Posición inicial de la bola

# Configurar mediapipe para detección de manos
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variables para suavizar el movimiento
smoothing_factor = 0.2

while True:
    # Procesar eventos de Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    # Leer frame de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Invertir el frame para que actúe como un espejo
    frame = cv2.flip(frame, 1)

    # Convertir el frame a RGB para mediapipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar manos
    results = hands.process(image_rgb)

    # Si se detecta una mano
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener la posición de la muñeca
            wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

            # Convertir la posición de la muñeca de valores normalizados a píxeles
            screen_width, screen_height = pygame.display.get_surface().get_size()
            target_x = int(wrist_x * screen_width)
            target_y = int(wrist_y * screen_height)

            # Suavizar el movimiento de la bola
            ball_x += (target_x - ball_x) * smoothing_factor
            ball_y += (target_y - ball_y) * smoothing_factor

    # Dibujar la bola en la pantalla
    screen.fill((255, 255, 255))  # Fondo blanco
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Actualizar la pantalla de Pygame
    pygame.display.flip()

    # Mostrar el frame en una ventana de OpenCV (opcional)
    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar recursos
cap.release()
cv2.destroyAllWindows()
pygame.quit()
