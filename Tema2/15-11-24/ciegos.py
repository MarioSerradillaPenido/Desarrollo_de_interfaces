import speech_recognition as sr
import webbrowser
import pyttsx3

# Inicializar reconocimiento de voz y motor de texto a voz
r = sr.Recognizer()
engine = pyttsx3.init()

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
    """Procesa el comando reconocido por el usuario."""
    if "abre amazon" in text:
        webbrowser.open('http://amazon.es')
        responder_texto("He abierto Amazon.")
    elif "abre las noticias" in text:
        webbrowser.open('http://elmundo.es')
        responder_texto("He abierto las noticias.")
    elif "abre google" in text:
        webbrowser.open('http://google.es')
        responder_texto("He abierto google chrome.")
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
    elif "qué tal" in text:
        responder_texto("Bien, ¿y tú?")
    else:
        responder_texto("¿Podrias repetir?")

# Bucle principal del asistente
while True:
    with sr.Microphone() as source:
        responder_texto('Modo ciego activado:')
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language="es-ES")
            print(f'Has dicho: {text}')
            procesar_comando(text)
        except sr.UnknownValueError:
            print("No te he entendido. Por favor, intenta de nuevo.")
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento de voz: {e}")
