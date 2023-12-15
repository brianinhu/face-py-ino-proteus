import cv2
import serial
import os

dataPath = '../face-py-ino-proteus/Data/Users'
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Leyendo el modelo
arduino = serial.Serial('COM2', 9600)

# Leyendo el modelo
face_recognizer.read('../face-py-ino-proteus/model/modeloLBPHFace.xml')

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

faceClassif = cv2.CascadeClassifier(
    cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

consecutive_frames_with_face = 0
required_consecutive_frames = 40

flag = "0"

while flag == "0":
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassif.detectMultiScale(gray, 1.2, 4, minSize=(100, 100))

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        cv2.putText(frame, '{}'.format(result), (x, y-5),
                    1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

        # LBPHFace
        if result[1] < 70:
            cv2.putText(frame, '{}'.format(
                imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if len(faces) == 0:
                consecutive_frames_with_face = 0
                arduino.write(b'0')
            else:
                consecutive_frames_with_face += 1
                print(consecutive_frames_with_face)

                if consecutive_frames_with_face >= required_consecutive_frames:
                    print(
                        f"Se han detectado {consecutive_frames_with_face} fotogramas consecutivos con rostro del usuario {imagePaths[result[0]]}")
                    print("Acceso permitido")
                    arduino.write(b'1')
                    flag = "1"  # Sale del bucle si se detectan suficientes fotogramas consecutivos con rostro

        else:
            cv2.putText(frame, 'Desconocido', (x, y-20), 2,
                        0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            consecutive_frames_with_face = 0
            arduino.write(b'0')

    cv2.imshow('Reconocimiento facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break # Sale del bucle si se presiona la tecla 'q'

cap.release()
cv2.destroyAllWindows()
