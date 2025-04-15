from picamera2 import Picamera2
import cv2
import pickle
import numpy as np
from time import sleep
from threading import Thread
from led_control import led_success, led_fail
from openai_gui import launch_openai_gui

# Last inn modellen
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

with open("labels.pkl", "rb") as f:
    label_map = pickle.load(f)

# Last inn Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Start kamera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

sleep(2)

print("[INFO] Systemet kjører. Trykk CTRL+C for å avslutte.")

# Justerbar grense for gjenkjenning
CONFIDENCE_THRESHOLD = 55

try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi)

            print(f"[DEBUG] Gjenkjent ID: {id_}, konfidens: {conf:.2f}")

            if conf < CONFIDENCE_THRESHOLD:
                name = label_map.get(id_, "Ukjent")
                print(f"[INFO] Gjenkjent som: {name} (konfidens: {conf:.2f})")

                Thread(target=led_success).start()
                launch_openai_gui(name)
            else:
                print(f"[INFO] Ansikt ikke gjenkjent (konfidens: {conf:.2f})")
                Thread(target=led_fail).start()

        # (valgfritt) vis kamera
        cv2.imshow("FaceAccess", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[INFO] Avslutter...")

picam2.close()
cv2.destroyAllWindows()
