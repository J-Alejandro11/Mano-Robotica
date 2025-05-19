import numpy as np
import LogicaMano as hand
import time
import cv2
import serial

print("[INFO] Iniciando script...")

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Ancho
cap.set(4, 480)  # Alto

if not cap.isOpened():
    print("[ERROR] No se pudo abrir la cámara.")
    exit()

# Inicializar detector de manos
detector = hand.handDetector(detectionCon=0.75, maxHands=1)
print("[INFO] Detector de mano inicializado.")

# Configuración de la conexión serial
try:
    serialConnection = serial.Serial("COM3", 9600, timeout=1)
    time.sleep(2)  # Esperar a que se establezca la conexión
    print("[INFO] Conexión serial abierta en COM3.")
except serial.SerialException:
    print("[WARNING] No se pudo abrir COM3. Continuando sin conexión serial.")
    serialConnection = None

# Variables para control de envío serial
lastSent = [0, 0, 0, 0, 0]
sendInterval = 0.1  # Segundos entre envíos
lastTime = 0

while True:
    # Leer imagen de la cámara
    ret, img = cap.read()
    if not ret:
        print("[ERROR] No se pudo leer imagen de la cámara.")
        break

    # Detectar manos
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Determinar qué dedos están levantados
        fingers = detector.fingersUp()
        print(f"[GESTO] Estado de dedos: {fingers}")

        # Enviar datos por serial si hay cambios y ha pasado el intervalo
        currentTime = time.time()
        if (fingers != lastSent or (currentTime - lastTime) > sendInterval) and serialConnection is not None:
            # Formato: "1,0,1,1,0\n" (ejemplo para pulgar abajo, índice arriba, etc.)
            data = f"{fingers[0]},{fingers[1]},{fingers[2]},{fingers[3]},{fingers[4]}\n"
            serialConnection.write(data.encode())
            print(f"[SERIAL] Enviado: {data.strip()}")
            lastSent = fingers.copy()
            lastTime = currentTime

    # Mostrar imagen
    cv2.imshow("Control de Mano Robotica", img)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Salida solicitada por el usuario.")
        break

# Liberar recursos
if serialConnection is not None:
    serialConnection.close()
cap.release()
cv2.destroyAllWindows()
print("[INFO] Programa finalizado.")