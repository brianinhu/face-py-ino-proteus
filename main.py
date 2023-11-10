from serial import Serial
import serial
import cv2

# Carga el clasificador frontal para detectar rostros
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Inicializa la cámara (puedes ajustar el número de la cámara según tu configuración)
cap = cv2.VideoCapture(1)

arduino = serial.Serial('COM2', 9600)

consecutive_frames_with_face = 0
# Número de fotogramas consecutivos con rostro para considerar el acceso permitido
required_consecutive_frames = 30

flag = "0"

while flag == "0":
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Convierte el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostros en el fotograma
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        consecutive_frames_with_face = 0
        arduino.write(b'0')
    else:
        for (x, y, w, h) in faces:
            # Dibuja un rectángulo alrededor del rostro detectado
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        consecutive_frames_with_face += 1
        print(consecutive_frames_with_face)

        if consecutive_frames_with_face >= required_consecutive_frames:
            print(
                f"Se han detectado {consecutive_frames_with_face} fotogramas consecutivos con rostro")
            print("Acceso permitido")
            arduino.write(b'1')
            flag = "1"  # Sale del bucle si se detectan suficientes fotogramas consecutivos con rostro

    # Muestra el fotograma con los rectángulos
    cv2.imshow('Reconocimiento Facial', frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
