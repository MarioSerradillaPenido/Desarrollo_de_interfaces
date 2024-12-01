import speech_recognition as sr
import webbrowser
import pyttsx3
import mediapipe as mp
import cv2
import pyautogui
import threading
from queue import Queue
import time
import sys

# Inicializar reconocimiento de voz y motor de texto a voz
r = sr.Recognizer()
engine = pyttsx3.init()

# Configuración inicial del motor de voz
engine.setProperty('rate', 150)  # Velocidad de lectura inicial

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Crear una cola para los mensajes de síntesis de texto
speech_queue = Queue()

# Función para procesar la cola de síntesis de texto en un hilo separado
def procesar_speech_queue():
    while True:
        texto = speech_queue.get()
        if texto == "stop":  # Permitir terminar el hilo si es necesario
            sys.exit()
        engine.say(texto)
        engine.runAndWait()
        speech_queue.task_done()

# Iniciar un hilo para la síntesis de texto
speech_thread = threading.Thread(target=procesar_speech_queue, daemon=True)
speech_thread.start()

# Función para responder con texto hablado
def responder_texto_async(texto):
    print(texto)
    speech_queue.put(texto)

# Función para leer un archivo
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            responder_texto_async(f"El contenido del archivo es: {contenido}")
    except FileNotFoundError:
        responder_texto_async("El archivo no se encontró.")
    except Exception as e:
        responder_texto_async(f"Ocurrió un error: {e}")

# Función para guardar una nota
def guardar_nota(texto):
    try:
        with open("notasDeVoz.txt", "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        responder_texto_async("Tu nota ha sido guardada.")
    except Exception as e:
        responder_texto_async(f"No se pudo guardar la nota: {e}")

# Función para buscar en Google
def buscar_en_google(texto_buscar):
    url = f"https://www.google.com/search?q={texto_buscar}"
    webbrowser.open(url)
    responder_texto_async(f"He buscado {texto_buscar} en Google.")

# Función para procesar gestos de la mano con MediaPipe
gesture_last_time = 0  # Para controlar la frecuencia de respuesta a gestos

def procesar_gestos(frame):
    global gesture_last_time
    gesture_cooldown = 2  # En segundos

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

            current_time = time.time()
            
            # Detectar gestos solo si ha pasado el tiempo de espera
            if current_time - gesture_last_time > gesture_cooldown:
                if index_y < thumb_y and middle_y < thumb_y:  # Apunta palma hacia abajo
                    pyautogui.press('volumeup')
                    responder_texto_async("He subido el volumen.")
                    gesture_last_time = current_time
                elif index_y > thumb_y and middle_y > thumb_y:  # Palma hacia arriba
                    pyautogui.press('volumedown')
                    responder_texto_async("He bajado el volumen.")
                    gesture_last_time = current_time

    return frame

# Función para procesar comandos de voz
def procesar_comando(text):
    if "abre amazon" in text:
        webbrowser.open('http://amazon.es')
        responder_texto_async("He abierto Amazon.")
    elif "abre las noticias" in text:
        webbrowser.open('http://elmundo.es')
        responder_texto_async("He abierto las noticias.")
    elif "abre google" in text:
        webbrowser.open('http://google.es')
        responder_texto_async("He abierto Google Chrome.")
    elif "leer texto" in text:
        responder_texto_async("¿Qué archivo deseas que te lea?")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                nombre_archivo = r.recognize_google(audio, language="es-ES").strip()
                leer_archivo(nombre_archivo)
            except sr.UnknownValueError:
                responder_texto_async("No entendí el nombre del archivo.")
    elif "toma nota" in text:
        responder_texto_async("Bloc de notas abierto, te escucho")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                nota = r.recognize_google(audio, language="es-ES").strip()
                guardar_nota(nota)
            except sr.UnknownValueError:
                responder_texto_async("No entendí la nota.")
    elif "buscar en google" in text:
        responder_texto_async("¿Qué deseas buscar en Google?")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                texto_buscar = r.recognize_google(audio, language="es-ES").strip()
                buscar_en_google(texto_buscar)
            except sr.UnknownValueError:
                responder_texto_async("No entendí lo que deseas buscar.")
    else:
        responder_texto_async("¿Podrías repetir?")

# Configurar micrófono para reconocimiento de voz
def configurar_microfono():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        responder_texto_async("Estoy listo para escucharte, dime qué deseas hacer.")
        while True:
            try:
                audio = r.listen(source)
                comando = r.recognize_google(audio, language="es-ES").lower()
                print(f"Comando reconocido: {comando}")
                procesar_comando(comando)
            except sr.UnknownValueError:
                responder_texto_async("No pude entender lo que dijiste. ¿Podrías repetir?")
            except sr.RequestError:
                responder_texto_async("Error al conectarse con el servicio de Google. Intenta de nuevo.")

# Bucle principal del asistente
cap = cv2.VideoCapture(0)  # Usamos la cámara para captar los gestos

# Iniciar el reconocimiento de voz en un hilo separado
voice_thread = threading.Thread(target=configurar_microfono, daemon=True)
voice_thread.start()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Procesar los gestos de la mano
    frame = procesar_gestos(frame)
    
    # Mostrar la imagen de la cámara
    cv2.imshow("Gestos", frame)

    # Detener el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
speech_queue.put("stop")  # Finalizar el hilo de síntesis de texto
