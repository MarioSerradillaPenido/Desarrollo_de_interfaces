import speech_recognition as sr
import webbrowser
import pyttsx3
import cv2
import pyautogui
import mediapipe as mp

# Inicializar reconocimiento de voz y motor de texto a voz
r = sr.Recognizer()
engine = pyttsx3.init()

# Configuración de la cámara y MediaPipe para detectar gestos de la mano
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

# Funciones de respuesta y acciones con voz
def responder_texto(texto):
    """Función para responder con texto hablado."""
    engine.say(texto)
    engine.runAndWait()
    print(texto)

def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo y lo dice en voz alta."""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            responder_texto(f"El contenido del archivo es: {contenido}")
    except FileNotFoundError:
        responder_texto("El archivo no se encontró.")
    except Exception as e:
        responder_texto(f"Ocurrió un error: {e}")

def guardar_nota(texto):
    """Guarda una nota en un archivo de texto."""
    try:
        with open("notasDeVoz.txt", "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        responder_texto("Tu nota ha sido guardada.")
    except Exception as e:
        responder_texto(f"No se pudo guardar la nota: {e}")

def procesar_comando(text):
    """Procesa comandos de voz."""
    if "abre amazon" in text:
        webbrowser.open('http://amazon.es')
        responder_texto("He abierto Amazon.")
    elif "abre las noticias" in text:
        webbrowser.open('http://elmundo.es')
        responder_texto("He abierto las noticias.")
    elif "abre google" in text:
        webbrowser.open('http://google.es')
        responder_texto("He abierto Google Chrome.")
    elif "leer texto" in text:
        responder_texto("¿Qué archivo deseas que te lea?")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                nombre_archivo = r.recognize_google(audio, language="es-ES").strip()
                leer_archivo(nombre_archivo)
            except sr.UnknownValueError:
                responder_texto("No entendí el nombre del archivo.")
    elif "toma nota" in text:
        responder_texto("Bloc de notas abierto, te escucho")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                nota = r.recognize_google(audio, language="es-ES").strip()
                guardar_nota(nota)
            except sr.UnknownValueError:
                responder_texto("No entendí la nota.")
    elif "buscar en google" in text:
        responder_texto("¿Qué deseas buscar en Google?")
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                texto_buscar = r.recognize_google(audio, language="es-ES").strip()
                buscar_en_google(texto_buscar)
            except sr.UnknownValueError:
                responder_texto("No entendí lo que deseas buscar.")
    else:
        responder_texto("¿Podrías repetir?")

# Función para buscar en Google
def buscar_en_google(texto_buscar):
    url = f"https://www.google.com/search?q={texto_buscar}"
    webbrowser.open(url)
    responder_texto(f"He buscado {texto_buscar} en Google.")

# Configurar micrófono para reconocimiento de voz
def configurar_microfono():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        responder_texto("Estoy listo para escucharte, dime qué deseas hacer.")
        while True:
            try:
                audio = r.listen(source)
                comando = r.recognize_google(audio, language="es-ES").lower()
                print(f"Comando reconocido: {comando}")
                procesar_comando(comando)
            except sr.UnknownValueError:
                responder_texto("No pude entender lo que dijiste. ¿Podrías repetir?")
            except sr.RequestError:
                responder_texto("Error al conectarse con el servicio de Google. Intenta de nuevo.")

# Función para detectar gestos con la mano
def detectar_gestos():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                if index_finger_y < thumb_y:
                    hand_gesture = 'pointing up'
                elif index_finger_y > thumb_y:
                    hand_gesture = 'pointing down'
                else:
                    hand_gesture = 'other'

                if hand_gesture == 'pointing up':
                    pyautogui.press('volumeup')
                elif hand_gesture == 'pointing down':
                    pyautogui.press('volumedown')

        cv2.imshow("Gestos de Mano", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Función principal
if __name__ == "__main__":
    # Iniciar el reconocimiento de voz en un hilo separado
    import threading
    threading.Thread(target=configurar_microfono, daemon=True).start()

    # Iniciar la detección de gestos de mano
    detectar_gestos()

    cap.release()
    cv2.destroyAllWindows()