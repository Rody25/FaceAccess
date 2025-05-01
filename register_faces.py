import os
import time
import cv2
from picamera2 import Picamera2
from database import lagre_bruker

#Spør brukeren om navn
name=input("Navn på bruker (ingen mellomrom): ")
path=f"dataset/{name}"
os.makedirs(path, exist_ok=True)

#Her starter Picamera2
picam2=Picamera2()
picam2.preview_configuration.main.size=(640, 480)
picam2.preview_configuration.main.format="RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)

print("[INFO] Starter bildeopptak. Trykk CTRL+C for å avbryte.")

count=0
try:
    while count<20:
        frame=picam2.capture_array()
        img_name=f"{path}/{count}.jpg"
        cv2.imwrite(img_name, frame)
        count += 1
        print(f"[INFO] Lagret {img_name}")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("[INFO] Avbrutt av bruker.")

picam2.close()

print(f"[INFO] Ferdig! {count} bilder lagret i '{path}'")
lagre_bruker(name, path)
