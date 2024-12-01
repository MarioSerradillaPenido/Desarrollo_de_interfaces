import cv2
import numpy as np
import subprocess  # Para ejecutar aplicaciones
 
# Carga el diccionario de marcadores ArUco y los parámetros de detección
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
 
# Configura la cámara
cap = cv2.VideoCapture(0)
 
# Dimensiones de la cámara
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Matrices de la cámara y coeficientes de distorsión (deben ajustarse para un uso real)
camera_matrix = np.array([[frame_width, 0, frame_width / 2],
                          [0, frame_height, frame_height / 2],
                          [0, 0, 1]], dtype="double")
dist_coeffs = np.zeros((4, 1))  # Asumiendo sin distorsión
 
# Coordenadas de los puntos del cubo en 3D (definimos un cubo de 5x5x5 cm)
axis = np.float32([[0, 0, 0], [0, 5, 0], [5, 5, 0], [5, 0, 0],
                   [0, 0, -5], [0, 5, -5], [5, 5, -5], [5, 0, -5]])
 
# Función para abrir una aplicación basada en el ID detectado
def open_application(marker_id):
    if marker_id == 1:
        subprocess.Popen(["notepad"])  # Ejemplo para abrir Notepad en Windows
    elif marker_id == 2:
        subprocess.Popen(["calc"])  # Ejemplo para abrir la calculadora en Windows
    elif marker_id == 3:
        subprocess.Popen(["mspaint"])  # Ejemplo para abrir Paint en Windows
    else:
        print(f"ID {marker_id} detectado, pero no tiene aplicación asignada.")
 
def draw_cube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)
   
    # Conecta las líneas para crear el cubo
    img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), 3)
    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)
    return img
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
 
    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # Detecta los marcadores ArUco
    corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
 
    # Si se detectan marcadores
    if ids is not None:
        for i, corner in enumerate(corners):
            # Obtiene el ID del marcador detectado
            marker_id = ids[i][0]
           
            # Llama a la función para abrir la aplicación
            open_application(marker_id)
 
            # Estima la pose del marcador
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 5, camera_matrix, dist_coeffs)
            (rvec - tvec).any()  # Evita un bug en OpenCV
           
            # Dibuja el marcador en la imagen
            cv2.aruco.drawDetectedMarkers(frame, corners)
           
            # Calcula la proyección de los puntos del cubo
            imgpts, _ = cv2.projectPoints(axis, rvec, tvec, camera_matrix, dist_coeffs)
            frame = draw_cube(frame, corner, imgpts)
   
    # Muestra la imagen con el cubo dibujado
    cv2.imshow('AR Cube', frame)
 
    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
