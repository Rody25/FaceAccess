from picamera2 import Picamera2
import cv2
import pickle
import numpy as np
from time import sleep
from led_control import led_success, led_fail

#Her lastes inn treningsdata
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

with open("labels.pkl", "rb") as f:
    label_map=pickle.load(f)

#Laster inn Haar Cascade
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#Starter Picamera2
picam2=Picamera2()
picam2.preview_configuration.main.size=(640, 480)
picam2.preview_configuration.main.format="RGB888"
picam2.configure("preview")
picam2.start()

sleep(2)

print("[INFO] Gjenkjenning starter. Trykk CTRL+C for å stoppe.")

try:
    while True:
        frame=picam2.capture_array()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi)

            if conf<70:
                name=label_map.get(id_, "Ukjent")
                print(f"[INFO] Gjenkjent: {name} (Konfidens: {round(conf,2)})")
                led_success()
            else:
                print("[INFO] Ukjent ansikt.")
                led_fail()

        
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #Vis bilde
        cv2.imshow("FaceAccess", frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

except KeyboardInterrupt:
    print("\n[INFO] Avslutter...")

picam2.close()
cv2.destroyAllWindows()
